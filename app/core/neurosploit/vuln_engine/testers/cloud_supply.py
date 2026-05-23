"""
NeuroSploit v3 - Cloud & Supply Chain Vulnerability Testers

Testers for S3 Bucket Misconfiguration, Cloud Metadata Exposure, Subdomain Takeover,
Vulnerable Dependencies, Container Escape, Serverless Misconfiguration.
"""
import re
from typing import Tuple, Dict, Optional
from app.core.neurosploit.vuln_engine.testers.base_tester import BaseTester


class S3BucketMisconfigTester(BaseTester):
    """Tester for S3 Bucket Misconfiguration"""

    def __init__(self):
        super().__init__()
        self.name = "s3_bucket_misconfig"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        public_access_patterns = [
            r"<ListBucketResult>",
            r"<Contents>",
            r"<Key>",
            r"<LastModified>",
            r"<Size>",
            r"<ETag>",
        ]
        for pattern in public_access_patterns:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.9, "S3 bucket misconfig: Public bucket listing enabled"

        if "s3.amazonaws.com" in payload or "s3." in payload:
            if response_status == 200:
                return True, 0.7, "S3 bucket misconfig: Bucket publicly accessible"
            if response_status == 403:
                return True, 0.5, "S3 bucket misconfig: Bucket exists but access denied (enumeration possible)"

        return False, 0.0, None


class CloudMetadataExposureTester(BaseTester):
    """Tester for Cloud Metadata Exposure"""

    def __init__(self):
        super().__init__()
        self.name = "cloud_metadata_exposure"
        self.metadata_endpoints = [
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/user-data/",
            "http://metadata.google.internal/computeMetadata/v1/",
            "http://100.100.100.200/latest/meta-data/",
        ]

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        metadata_indicators = {
            r"ami-id": "AWS AMI ID",
            r"instance-id": "AWS Instance ID",
            r"local-ipv4": "AWS Local IP",
            r"public-ipv4": "AWS Public IP",
            r"hostname": "Cloud hostname",
            r"vm-id": "Azure VM ID",
            r"subscriptionId": "Azure Subscription ID",
            r"tenantId": "Azure Tenant ID",
            r"project-id": "GCP Project ID",
            r"instance/hostname": "GCP Instance hostname",
        }
        for pattern, description in metadata_indicators.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.9, f"Cloud metadata exposed: {description}"

        if response_status == 200:
            if any("169.254" in payload or "metadata" in payload.lower() for _ in [1]):
                return True, 0.7, "Cloud metadata endpoint accessible"

        return False, 0.0, None


class SubdomainTakeoverTester(BaseTester):
    """Tester for Subdomain Takeover"""

    def __init__(self):
        super().__init__()
        self.name = "subdomain_takeover"
        self.takeover_indicators = {
            r"there\s*is\s*no\s*app\s*configured": "Heroku",
            r"no\s*such\s*app": "Heroku",
            r"application\s*not\s*found": "Heroku",
            r"a\s*fast\s*and\s*secure\s*content\s*delivery": "Fastly",
            r"domain\s*not\s*configured": "Pantheon",
            r"this\s*user\s*does\s*not\s*have\s*a\s*github\s*page": "GitHub Pages",
            r"repository\s*not\s*found": "GitHub Pages",
            r"bucket\s*does\s*not\s*exist": "AWS S3",
            r"the\s*specified\s*bucket\s*does\s*not\s*exist": "AWS S3",
            r"no\s*application\s*configured": "App Engine",
            r"cname\s*not\s*found": "Various CDN",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        for pattern, provider in self.takeover_indicators.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.85, f"Subdomain takeover possible: {provider} response"

        if response_status == 404:
            takeover_pages = [
                r"herokuapp\.com", r"fastly\.net", r"cloudfront\.net",
                r"azurewebsites\.net", r"github\.io", r"wpengine\.com",
                r"pantheon\.io", r"appspot\.com",
            ]
            for pattern in takeover_pages:
                if re.search(pattern, response_body, re.IGNORECASE):
                    return True, 0.7, f"Subdomain takeover: Orphaned {pattern} reference"

        return False, 0.0, None


class VulnerableDependencyTester(BaseTester):
    """Tester for Vulnerable Dependency Detection"""

    def __init__(self):
        super().__init__()
        self.name = "vulnerable_dependency"
        self.vulnerable_packages = {
            "lodash:4.17.10": "Prototype pollution",
            "express:4.17.1": "Open redirect",
            "django:3.1": "SQL injection",
            "rails:6.0": "Remote code execution",
            "spring-boot:2.5": "Remote code execution",
            "log4j:2.14": "Log4Shell RCE",
            "jackson-databind:2.9": "Deserialization RCE",
            "requests:2.25": "SSRF bypass",
            "flask:2.0": "Debug mode RCE",
            "axios:0.21": "SSRF",
            "jsonwebtoken:8.5": "JWT bypass",
            "moment:2.29": "ReDoS",
            "minimist:1.2.5": "Prototype pollution",
            "ini:1.3.5": "Prototype pollution",
            "node-forge:0.10": "Signature verification bypass",
            "crypt:0.0.2": "Insecure randomness",
            "xml2js:0.4": "XXE",
            "marked:0.7": "XSS",
            "showdown:1.9": "XSS",
            "serialize-javascript:3.0": "RCE",
        }

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        for package, vulnerability in self.vulnerable_packages.items():
            if package.lower() in response_body.lower():
                return True, 0.7, f"Vulnerable dependency: {package} ({vulnerability})"

        package_files = [
            (r"package\.lock\.json", "Node.js"),
            (r"composer\.lock", "PHP"),
            (r"requirements\.txt", "Python"),
            (r"Gemfile\.lock", "Ruby"),
            (r"pom\.xml", "Java"),
            (r"go\.sum", "Go"),
            (r"Cargo\.lock", "Rust"),
        ]
        for pattern, ecosystem in package_files:
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.5, f"Dependency file exposed: {ecosystem}"

        return False, 0.0, None


class ContainerEscapeTester(BaseTester):
    """Tester for Container Escape vulnerabilities"""

    def __init__(self):
        super().__init__()
        self.name = "container_escape"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        container_indicators = {
            r"\.dockerenv": "Docker container detected",
            r"container=docker": "Docker container environment",
            r"cgroup.*docker": "Docker cgroup",
            r"lxc": "LXC container",
            r"kubepods": "Kubernetes pod",
            r"/var/run/secrets/kubernetes.io": "Kubernetes service account mounted",
            r"/run/secrets/kubernetes.io": "Kubernetes secrets exposed",
            r"/var/run/docker\.sock": "Docker socket mounted",
        }
        for pattern, description in container_indicators.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.8, f"Container escape: {description}"

        if "docker" in payload.lower() or "container" in payload.lower():
            if response_status == 200 and len(response_body) > 200:
                return True, 0.6, "Container escape: Internal container information exposed"

        return False, 0.0, None


class ServerlessMisconfigTester(BaseTester):
    """Tester for Serverless Misconfiguration"""

    def __init__(self):
        super().__init__()
        self.name = "serverless_misconfig"

    def analyze_response(
        self,
        payload: str,
        response_status: int,
        response_headers: Dict,
        response_body: str,
        context: Dict
    ) -> Tuple[bool, float, Optional[str]]:
        serverless_indicators = {
            r"AWS_ACCESS_KEY_ID": "AWS credentials in environment",
            r"AWS_SECRET_ACCESS_KEY": "AWS secret key exposed",
            r"AWS_SESSION_TOKEN": "AWS session token exposed",
            r"function_arn": "Lambda function ARN",
            r"execution_arn": "Lambda execution ARN",
            r"x-amzn-requestid": "AWS Lambda request ID",
            r"FUNCTION_NAME": "Function name exposed",
            r"REGION": "Cloud region exposed",
            r"_HANDLER": "Handler name exposed",
            r"serverless": "Serverless framework indicator",
            r"lambda": "AWS Lambda indicator",
        }
        for pattern, description in serverless_indicators.items():
            if re.search(pattern, response_body, re.IGNORECASE):
                return True, 0.7, f"Serverless misconfig: {description}"

        if response_status == 200:
            if any(x in response_headers for x in [
                "X-Amz-Function-Error", "X-Amzn-Trace-Id"
            ]):
                return True, 0.6, "Serverless misconfig: Lambda headers exposed"

        return False, 0.0, None
