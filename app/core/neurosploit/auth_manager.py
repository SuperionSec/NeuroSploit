"""
Authentication Manager for NeuroSploit - handles auth for authenticated scans.

Generates login payloads, manages session cookies, detects auth status,
and handles multi-step multi-factor authentication workflows.
"""

import re
import json
import base64
import hashlib
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

try:
    import aiohttp
except ImportError:
    aiohttp = None


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AuthSession:
    """Persistent authentication state across a scan."""
    cookies: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    tokens: Dict[str, str] = field(default_factory=dict)  # csrf, bearer, etc.
    login_success: bool = False
    login_path: str = ""
    auth_type: str = ""  # form, basic, bearer, oauth, jwt, saml
    mfa_required: bool = False
    mfa_type: str = ""  # totp, sms, email, push
    session_valid: bool = False
    created_at: float = 0.0
    error_message: str = ""


@dataclass
class LoginForm:
    """Parsed login form details."""
    action: str
    method: str
    username_field: str
    password_field: str
    csrf_token: Optional[str] = None
    csrf_field: str = ""
    hidden_fields: Dict[str, str] = field(default_factory=dict)
    extra_fields: List[Dict] = field(default_factory=list)
    has_captcha: bool = False


@dataclass
class MFAChallenge:
    """Multi-factor authentication challenge details."""
    challenge_type: str  # totp, sms, email, push, recovery_code
    challenge_path: str  # URL to submit MFA code
    session_token: str = ""
    csrf_token: Optional[str] = None
    csrf_field: str = ""
    hidden_fields: Dict[str, str] = field(default_factory=dict)
    code_length: int = 6
    resend_path: str = ""
    timeout_seconds: int = 300
    error_message: str = ""


# ---------------------------------------------------------------------------
# Common auth-related patterns
# ---------------------------------------------------------------------------

_RE_FORM = re.compile(
    r"<form[^>]*>.*?</form>", re.DOTALL | re.IGNORECASE)
_RE_ACTION = re.compile(r'action\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
_RE_METHOD = re.compile(r'method\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
_RE_INPUT = re.compile(
    r'<input[^>]*>', re.IGNORECASE)
_RE_NAME = re.compile(r'name\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
_RE_TYPE = re.compile(r'type\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
_RE_VALUE = re.compile(r'value\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
_RE_CSRF = re.compile(
    r'<meta[^>]+name=["\']csrf[^"\']*["\']', re.IGNORECASE)
_RE_CSRF_NAME = re.compile(r'name=["\']([^"\']*)["\']', re.IGNORECASE)
_RE_CSRF_CONTENT = re.compile(r'content=["\']([^"\']*)["\']', re.IGNORECASE)
_RE_BEARER = re.compile(
    r'(?:access[_-]?token|auth[_-]?token|bearer|jwt)\s*[:=]\s*["\']?([^\s"\'&;]+)', re.I)
_RE_OAUTH = re.compile(
    r'(?:oauth|openid[_-]?connect|saml|sso)[^"\']*["\']([^"\']*)["\']', re.I)
_RE_MFA = re.compile(
    r'(?:mfa|two[_-]?factor|2fa|totp|verification[_-]?code|one[_-]?time[_-]?code|otp|sms[_-]?code'
    r'|email[_-]?code|authenticator[_-]?code|security[_-]?code)',
    re.IGNORECASE)
_RE_MFA_INPUT = re.compile(
    r'(?:code|token|pin|otp|verification|challenge)', re.IGNORECASE)
_RE_RECAPTCHA = re.compile(
    r'(?:g-recaptcha|h-captcha|recaptcha|cf-turnstile)', re.IGNORECASE)
_RE_ERROR = re.compile(
    r'(?:incorrect|invalid|wrong|failed|not[_\s]?found|error|denied'
    r'|locked|expired|disabled|blocked|too[_\s]?many)', re.IGNORECASE)
_RE_SUCCESS = re.compile(
    r'(?:welcome|dashboard|success|logout|sign[_\s]?out'
    r'|my[_\s]?account|profile|settings)',
    re.IGNORECASE)

# Common username / password field names
_USERNAME_FIELDS = {
    "username", "user", "login", "email", "mail",
    "account", "userid", "user_id", "name", "uname",
    "log", "login_id", "login_name", "signin", "sign_in", "sign-in",
    "identification", "identifier",
    "auth_user", "auth[username]",
}
_PASSWORD_FIELDS = {
    "password", "pass", "pwd", "passwd",
    "userpassword", "login_password",
    "auth_pass", "auth[password]", "secret",
}
_CSRF_FIELDS = {
    "csrf", "xsrf", "csrf_token", "csrf-token", "xsrf_token",
    "_token", "_csrf", "_xsrf", "authenticity_token", "nonce",
    "__RequestVerificationToken", "csrfmiddlewaretoken", "form_key",
    "_wpnonce", "_wp_http_referer",
}

# Common login endpoints
_COMMON_LOGIN_PATHS = [
    "/login", "/signin", "/sign_in", "/sign-in",
    "/auth/login", "/auth/signin", "/auth",
    "/account/login", "/account/signin",
    "/user/login", "/user/signin",
    "/users/login", "/users/sign_in",
    "/api/login", "/api/auth/login", "/api/v1/login",
    "/auth/login/", "/login/", "/signin/",
    "/admin/login", "/administrator/login", "/wp-login.php",
    "/oauth/login", "/oauth/authorize",
    "/connect/login", "/connect/authorize",
    "/Account/Login", "/Account/SignIn",
    "/identity/login", "/identity/account/login",
    "/realms/master/login-actions/authenticate",
    "/auth/realms/master/login-actions/authenticate",
]

# ---------------------------------------------------------------------------
# AuthManager
# ---------------------------------------------------------------------------

class AuthManager:
    """Manages authentication for authenticated web application scans."""

    def __init__(self, session=None):
        self.session = session
        self._sessions: Dict[str, AuthSession] = {}

    # ── Login form detection & parsing ─────────────────────────────────

    async def detect_login_forms(self, target: str, session=None) -> List[LoginForm]:
        """Discover and parse login forms on the target."""
        sess = session or self.session
        if not sess:
            return []

        forms: List[LoginForm] = []
        seen_actions: Set[str] = set()

        async def _check_url(url: str):
            try:
                async with sess.get(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        ct = resp.headers.get("Content-Type", "")
                        if "text/html" in ct:
                            text = await resp.text()
                            text = text[:500000]

                            for form_html in _RE_FORM.findall(text):
                                form = self._parse_form(url, form_html)
                                if form and form.action not in seen_actions:
                                    seen_actions.add(form.action)
                                    forms.append(form)
            except Exception:
                pass

        # Check common login paths + the homepage
        urls_to_check = {target} | {urljoin(target, p) for p in _COMMON_LOGIN_PATHS}
        for url in urls_to_check:
            await _check_url(url)

        logger.info(f"[AuthManager] Found {len(forms)} login form(s) on {target}")
        return forms

    def _parse_form(self, page_url: str, form_html: str) -> Optional[LoginForm]:
        """Parse a single <form> HTML block into a LoginForm."""
        action = ""
        method = "POST"
        username_field = ""
        password_field = ""
        csrf_token: Optional[str] = None
        csrf_field = ""
        hidden_fields: Dict[str, str] = {}
        extra_fields: List[Dict] = []
        has_captcha = False

        # Extract action
        m = _RE_ACTION.search(form_html)
        if m:
            action = urljoin(page_url, m.group(1))

        # Extract method
        m = _RE_METHOD.search(form_html)
        if m:
            method = m.group(1).upper()

        # Parse inputs
        for input_html in _RE_INPUT.finditer(form_html):
            input_str = input_html.group(0)
            name_m = _RE_NAME.search(input_str)
            if not name_m:
                continue
            name = name_m.group(1).lower().strip()

            type_m = _RE_TYPE.search(input_str)
            itype = (type_m.group(1) if type_m else "text").lower()

            value_m = _RE_VALUE.search(input_str)
            value = value_m.group(1) if value_m else ""

            # Check for CSRF
            if name in _CSRF_FIELDS:
                if value:
                    csrf_token = value
                csrf_field = name if not csrf_field else csrf_field

            # Check for username
            if itype in ("text", "email", "tel") and not username_field:
                if name in _USERNAME_FIELDS:
                    username_field = name

            # Check for password
            if itype == "password" and not password_field:
                password_field = name

            # Hidden fields (store all for replay)
            if itype == "hidden":
                hidden_fields[name] = value

            # Captcha detection
            if _RE_RECAPTCHA.search(input_str):
                has_captcha = True

        # Also check for CSRF in meta tags (common in Django, Laravel, etc.)
        if not csrf_token:
            # Look for CSRF meta tag near the form
            form_start = form_html
            meta_matches = _RE_CSRF.findall(form_start)
            for meta_html in meta_matches:
                name_m = _RE_CSRF_NAME.search(meta_html)
                content_m = _RE_CSRF_CONTENT.search(meta_html)
                if content_m:
                    csrf_token = content_m.group(1)
                    csrf_field = name_m.group(1) if name_m else "csrf_token"
                    break

        # Fallback username/password detection by keywords
        if not username_field or not password_field:
            for input_html in _RE_INPUT.finditer(form_html):
                input_str = input_html.group(0)
                name_m = _RE_NAME.search(input_str)
                if not name_m:
                    continue
                name = name_m.group(1).lower().strip()
                type_m = _RE_TYPE.search(input_str)
                itype = (type_m.group(1) if type_m else "text").lower()

                if not username_field and "user" in name or "login" in name or "email" in name or "mail" in name:
                    if itype in ("text", "email", "tel", ""):
                        username_field = name
                if not password_field and ("pass" in name or "pwd" in name or "secret" in name or "pin" in name):
                    if itype == "password":
                        password_field = name

        # Still no username/password? Take first text + first password
        if not username_field or not password_field:
            for input_html in _RE_INPUT.finditer(form_html):
                input_str = input_html.group(0)
                name_m = _RE_NAME.search(input_str)
                if not name_m:
                    continue
                name = name_m.group(1)
                type_m = _RE_TYPE.search(input_str)
                itype = (type_m.group(1) if type_m else "text").lower()

                if not username_field and itype in ("text", "email", "tel", ""):
                    username_field = name
                    continue
                if not password_field and itype == "password":
                    password_field = name

        # If still no fields found, this isn't a valid login form
        if not username_field and not password_field:
            return None

        return LoginForm(
            action=action,
            method=method,
            username_field=username_field,
            password_field=password_field,
            csrf_token=csrf_token,
            csrf_field=csrf_field,
            hidden_fields=hidden_fields,
            extra_fields=extra_fields,
            has_captcha=has_captcha,
        )

    # ── Login execution ────────────────────────────────────────────────

    async def execute_login(
        self,
        target: str,
        login_form: LoginForm,
        username: str,
        password: str,
        session=None,
        extra_params: Optional[Dict[str, str]] = None,
    ) -> AuthSession:
        """Submit login credentials and capture authentication tokens."""
        sess = session or self.session
        auth = AuthSession(auth_type="form", login_path=login_form.action)

        if not sess:
            auth.error_message = "No HTTP session available"
            return auth

        try:
            # Build form data
            data = dict(login_form.hidden_fields)
            data[login_form.username_field] = username
            data[login_form.password_field] = password

            # Add extra params (e.g., remember_me, redirect_to)
            if extra_params:
                data.update(extra_params)

            # Refresh CSRF if available (GET the login page first)
            if login_form.csrf_field:
                try:
                    async with sess.get(login_form.action.split("?")[0], allow_redirects=True,
                                        timeout=aiohttp.ClientTimeout(total=10)) as pre_resp:
                        pre_text = await pre_resp.text()
                        # Try to extract fresh CSRF token
                        fresh_token = self._extract_csrf_from_page(pre_text, login_form.csrf_field)
                        if fresh_token:
                            data[login_form.csrf_field] = fresh_token
                        # Update cookies from pre-flight
                        for cook in pre_resp.cookies.values():
                            auth.cookies[cook.key] = cook.value
                except Exception:
                    pass

            # Submit login
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": urlparse(login_form.action).netloc or target,
                "Referer": login_form.action,
            }

            if login_form.method == "GET":
                # GET-based login (rare but exists)
                async with sess.get(
                    login_form.action, params=data, headers=headers,
                    allow_redirects=False, timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    auth = await self._process_login_response(resp, auth)
            else:
                async with sess.post(
                    login_form.action, data=data, headers=headers,
                    allow_redirects=False, timeout=aiohttp.ClientTimeout(total=15),
                ) as resp:
                    auth = await self._process_login_response(resp, auth)

            # Follow redirect if needed
            if auth.login_success or not auth.error_message:
                try:
                    redirect_url = login_form.action  # fallback
                    async with sess.get(redirect_url, allow_redirects=True,
                                        timeout=aiohttp.ClientTimeout(total=10)) as final_resp:
                        final_text = await final_resp.text()
                        # Check for MFA challenge on final page
                        auth.mfa_required = bool(_RE_MFA.search(final_text[:50000]))
                        if auth.mfa_required:
                            auth.mfa_type = self._detect_mfa_type(final_text[:50000])
                except Exception:
                    pass

            # Check for bearer tokens in response bodies
            self._extract_bearer_tokens(auth)

            auth.session_valid = auth.login_success
            auth.created_at = __import__("time").time()

        except Exception as e:
            auth.error_message = str(e)
            logger.error(f"[AuthManager] Login failed: {e}")

        return auth

    async def _process_login_response(self, resp, auth: AuthSession) -> AuthSession:
        """Process HTTP response after login submission."""
        # Extract cookies
        for c in resp.cookies.values():
            auth.cookies[c.key] = c.value

        # Extract headers that might contain auth info
        for auth_header in ("Authorization", "X-Auth-Token", "X-CSRF-Token"):
            val = resp.headers.get(auth_header, "")
            if val:
                auth.headers[auth_header] = val

        # Check Set-Cookie for session cookies
        set_cookie = resp.headers.get("Set-Cookie", "")
        if set_cookie:
            for cookie_str in set_cookie.split(","):
                cookie_str = cookie_str.strip()
                if "session" in cookie_str.lower() or "auth" in cookie_str.lower():
                    # Already captured above, just mark success if session cookie present
                    auth.login_success = True

        # Check redirect for success indicator
        location = resp.headers.get("Location", "")
        if location:
            auth.login_success = True  # Redirect usually means success
            if _RE_ERROR.search(location):
                auth.login_success = False
                auth.error_message = "Login failed — redirected to error page"

        # Parse response body
        text = ""
        try:
            text = await resp.text()
            text = text[:100000]
        except Exception:
            pass

        # Detect login status from body
        if _RE_ERROR.search(text[:5000]):
            auth.login_success = False
            auth.error_message = self._extract_error_message(text[:5000])

        if _RE_SUCCESS.search(text[:5000]):
            auth.login_success = True

        # Detect CSRF tokens in body
        csrf_token = self._extract_csrf_from_page(text)
        if csrf_token:
            auth.tokens["csrf"] = csrf_token

        # Check status code
        if resp.status in (401, 403):
            auth.login_success = False
            auth.error_message = f"Login rejected (HTTP {resp.status})"

        return auth

    # ── MFA Support ────────────────────────────────────────────────────

    async def detect_mfa(self, target: str, auth_session: AuthSession,
                         session=None) -> Optional[MFAChallenge]:
        """Detect MFA challenge after login."""
        sess = session or self.session
        if not sess or not auth_session.login_success:
            return None

        try:
            # Check if we're on an MFA page
            cookies = auth_session.cookies
            async with sess.get(target, cookies=cookies, allow_redirects=True,
                                timeout=aiohttp.ClientTimeout(total=10)) as resp:
                text = await resp.text()
                text = text[:100000]

            if not _RE_MFA.search(text):
                return None

            # Found MFA — parse the challenge form
            form_match = _RE_FORM.search(text)
            if not form_match:
                return None

            form_html = form_match.group(0)
            action_m = _RE_ACTION.search(form_html)
            mfa_path = urljoin(target, action_m.group(1)) if action_m else target

            # Extract inputs for MFA code
            has_code_input = False
            csrf_token = None
            csrf_field = ""
            hidden_fields = {}

            for input_html in _RE_INPUT.finditer(form_html):
                input_str = input_html.group(0)
                name_m = _RE_NAME.search(input_str)
                if not name_m:
                    continue
                name = name_m.group(1).lower()
                type_m = _RE_TYPE.search(input_str)
                itype = (type_m.group(1) if type_m else "text").lower()

                if itype == "hidden":
                    val_m = _RE_VALUE.search(input_str)
                    hidden_fields[name] = val_m.group(1) if val_m else ""

                if name in _CSRF_FIELDS:
                    val_m = _RE_VALUE.search(input_str)
                    csrf_token = val_m.group(1) if val_m else csrf_token
                    csrf_field = name

                if _RE_MFA_INPUT.search(name) and itype in ("text", "number", "tel", ""):
                    has_code_input = True

            if has_code_input:
                return MFAChallenge(
                    challenge_type=self._detect_mfa_type(text),
                    challenge_path=mfa_path,
                    session_token=auth_session.tokens.get("csrf", ""),
                    csrf_token=csrf_token,
                    csrf_field=csrf_field,
                    hidden_fields=hidden_fields,
                )
        except Exception as e:
            logger.warning(f"[AuthManager] MFA detection error: {e}")

        return None

    async def submit_mfa(self, mfa_challenge: MFAChallenge, mfa_code: str,
                         auth_session: AuthSession, session=None) -> bool:
        """Submit MFA code and update auth session."""
        sess = session or self.session
        if not sess:
            return False

        try:
            data = dict(mfa_challenge.hidden_fields)
            # Find the code input field name
            code_field = "code"
            for name in ("code", "token", "otp", "pin", "verification_code", "totp", "mfa_code"):
                data[name] = mfa_code

            if mfa_challenge.csrf_field and mfa_challenge.csrf_token:
                data[mfa_challenge.csrf_field] = mfa_challenge.csrf_token

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            cookies = auth_session.cookies

            async with sess.post(mfa_challenge.challenge_path, data=data, headers=headers,
                                 cookies=cookies, allow_redirects=True,
                                 timeout=aiohttp.ClientTimeout(total=15)) as resp:
                text = await resp.text()
                text = text[:50000]

                # Update cookies
                for c in resp.cookies.values():
                    auth_session.cookies[c.key] = c.value

                # Check success
                if _RE_SUCCESS.search(text[:5000]):
                    auth_session.mfa_required = False
                    auth_session.session_valid = True
                    return True
                elif resp.status < 400 and not _RE_ERROR.search(text[:5000]):
                    auth_session.mfa_required = False
                    auth_session.session_valid = True
                    return True

        except Exception as e:
            logger.error(f"[AuthManager] MFA submission error: {e}")

        return False

    # ── Basic / Digest / Bearer / OAuth ────────────────────────────────

    async def authenticate_basic(
        self, username: str, password: str,
    ) -> AuthSession:
        """Create a Basic Auth session."""
        auth_string = base64.b64encode(
            f"{username}:{password}".encode()).decode()
        return AuthSession(
            headers={"Authorization": f"Basic {auth_string}"},
            auth_type="basic",
            login_success=True,
            session_valid=True,
            created_at=__import__("time").time(),
        )

    def authenticate_bearer(self, token: str) -> AuthSession:
        """Create a Bearer token session."""
        return AuthSession(
            headers={"Authorization": f"Bearer {token}"},
            auth_type="bearer",
            login_success=True,
            session_valid=True,
            created_at=__import__("time").time(),
        )

    def authenticate_jwt(self, token: str) -> AuthSession:
        """Create a JWT token session."""
        return self.authenticate_bearer(token)

    # ── Session management ─────────────────────────────────────────────

    def save_session(self, session_id: str, auth_session: AuthSession):
        """Store session for reuse during scan."""
        self._sessions[session_id] = auth_session

    def get_session(self, session_id: str) -> Optional[AuthSession]:
        """Retrieve a stored session."""
        return self._sessions.get(session_id)

    def remove_session(self, session_id: str):
        """Remove a stored session."""
        self._sessions.pop(session_id, None)

    def get_auth_headers(self, auth_session: AuthSession) -> Dict[str, str]:
        """Get headers for authenticated requests."""
        headers = dict(auth_session.headers)
        if auth_session.tokens.get("csrf"):
            headers["X-CSRF-Token"] = auth_session.tokens["csrf"]
        return headers

    def get_auth_cookies(self, auth_session: AuthSession) -> Dict[str, str]:
        """Get cookies for authenticated requests."""
        return dict(auth_session.cookies)

    # ── Bulk credential testing ────────────────────────────────────────

    async def test_credentials(
        self, target: str, login_form: LoginForm,
        credentials: List[Tuple[str, str]], session=None,
    ) -> List[Tuple[str, str, bool, str]]:
        """Test multiple username/password combinations. Returns (user, pass, success, error)."""
        results: List[Tuple[str, str, bool, str]] = []

        for username, password in credentials[:50]:  # Cap at 50
            auth = await self.execute_login(
                target, login_form, username, password, session,
            )
            results.append((
                username, password, auth.login_success, auth.error_message,
            ))
            if auth.login_success:
                break  # Stop on first success

        return results

    # ── Internal helpers ───────────────────────────────────────────────

    @staticmethod
    def _extract_csrf_from_page(html: str, field_name: str = "") -> Optional[str]:
        """Extract CSRF token from HTML page."""
        # Meta tag approach
        for meta_m in _RE_CSRF.finditer(html):
            if not field_name:
                content_m = _RE_CSRF_CONTENT.search(meta_m.group(0))
                if content_m:
                    return content_m.group(1)
            name_m = _RE_CSRF_NAME.search(meta_m.group(0))
            if name_m and name_m.group(1) == field_name:
                content_m = _RE_CSRF_CONTENT.search(meta_m.group(0))
                if content_m:
                    return content_m.group(1)

        # Hidden form input approach
        for input_m in _RE_INPUT.finditer(html):
            input_str = input_m.group(0)
            name_m = _RE_NAME.search(input_str)
            if not name_m:
                continue
            name = name_m.group(1)

            type_m = _RE_TYPE.search(input_str)
            if type_m and type_m.group(1).lower() != "hidden":
                continue

            if name in _CSRF_FIELDS or (field_name and name == field_name):
                value_m = _RE_VALUE.search(input_str)
                if value_m:
                    return value_m.group(1)

        return None

    @staticmethod
    def _extract_bearer_tokens(auth: AuthSession):
        """Extract bearer/JWT tokens from auth session."""
        for val in list(auth.headers.values()) + list(auth.cookies.values()):
            for pattern in (_RE_BEARER,):
                m = pattern.search(str(val))
                if m:
                    token = m.group(1)
                    auth.tokens["bearer"] = token
                    auth.headers["Authorization"] = f"Bearer {token}"
                    return

    @staticmethod
    def _extract_error_message(text: str) -> str:
        """Extract login error message from response body."""
        # Common error containers
        error_patterns = [
            r'class=["\'][^"\']*error[^"\']*["\'][^>]*>([^<]+)',
            r'<div[^>]*alert[^>]*>([^<]+)',
            r'<span[^>]*error[^>]*>([^<]+)',
        ]
        for pattern in error_patterns:
            m = re.search(pattern, text, re.I)
            if m:
                return m.group(1).strip()[:200]

        # Find sentence containing error keywords
        for line in text.split("\n"):
            if _RE_ERROR.search(line):
                return line.strip()[:200]

        return "Unknown error"

    @staticmethod
    def _detect_mfa_type(text: str) -> str:
        """Detect the type of MFA from page content."""
        text_lower = text.lower()
        if "totp" in text_lower or "authenticator" in text_lower or "google" in text_lower:
            return "totp"
        if "sms" in text_lower or "phone" in text_lower or "mobile" in text_lower:
            return "sms"
        if "email" in text_lower or "mail" in text_lower:
            return "email"
        if "push" in text_lower or "approve" in text_lower or "tap" in text_lower:
            return "push"
        if "recovery" in text_lower or "backup" in text_lower:
            return "recovery_code"
        return "unknown"