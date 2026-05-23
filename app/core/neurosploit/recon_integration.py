"""
NeuroSploit v3 - Recon Data Integration

Integrates recon data from HTTP-based tools for comprehensive reconnaissance.
Feeds enriched recon data into agent streams for intelligent testing.

Tools integration includes:
- Subdomain Enumeration: subfinder, amass, assetfinder
- DNS Resolution: dnsx, dig
- HTTP Probing: httpx, curl
- URL Discovery: gau, waybackurls, katana, gospider
- Port Scanning: nmap, naabu
- Tech Detection: whatweb
- Fuzzing: ffuf, gobuster
- Vulnerability Scanning: nuclei, nikto
- Parameter Discovery: arjun

All tools run via subprocess (no Docker dependency). Graceful fallback on missing tools.
"""
import asyncio
import subprocess
import json
import os
import shutil
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
from pathlib import Path

# Optional aiohttp
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    aiohttp = None


class ReconIntegration:
    """Full reconnaissance integration with security tools.

    Automatically uses available tools and skips missing ones.
    No Docker/Kali dependency — tools run natively via subprocess.
    """

    def __init__(self, scan_id: str, log_callback: Optional[Callable] = None,
                 progress_callback: Optional[Callable] = None):
        self.scan_id = scan_id
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.results_path = Path("/app/data/recon") if Path("/app").exists() else Path("data/recon")
        self.results_path.mkdir(parents=True, exist_ok=True)
        self.wordlists_path = Path("/opt/wordlists")
        self.available_tools: Dict[str, bool] = {}

    async def log(self, level: str, message: str):
        if self.log_callback:
            try:
                await self.log_callback(level, message)
            except Exception:
                pass

    async def _progress(self, pct: int, phase: str):
        if self.progress_callback:
            try:
                await self.progress_callback(pct, phase)
            except Exception:
                pass

    def _tool_exists(self, tool: str) -> bool:
        if tool not in self.available_tools:
            self.available_tools[tool] = shutil.which(tool) is not None
        return self.available_tools[tool]

    async def _run_command(self, cmd: List[str], timeout: int = 120) -> str:
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )
            return stdout.decode('utf-8', errors='ignore')
        except asyncio.TimeoutError:
            try:
                process.kill()
            except Exception:
                pass
            return ""
        except Exception:
            return ""

    async def run_full_recon(self, target: str, depth: str = "medium") -> Dict[str, Any]:
        await self.log("info", f"Starting FULL reconnaissance on {target}")
        await self.log("info", f"Depth level: {depth}")
        await self._progress(5, "Initializing reconnaissance...")

        await self._check_tools()

        results = {
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "depth": depth,
            "subdomains": [],
            "live_hosts": [],
            "urls": [],
            "endpoints": [],
            "ports": [],
            "technologies": [],
            "vulnerabilities": [],
            "js_files": [],
            "parameters": [],
            "interesting_paths": [],
            "dns_records": [],
            "screenshots": [],
            "secrets": [],
        }

        domain = self._extract_domain(target)
        base_url = target if target.startswith("http") else f"https://{target}"

        phases = self._get_phases(depth)
        total_phases = len(phases)

        for i, (phase_name, phase_func) in enumerate(phases):
            try:
                progress = 5 + int((i / total_phases) * 35)
                await self._progress(progress, f"Recon: {phase_name}")
                await self.log("info", f"Running {phase_name}...")

                phase_results = await phase_func(domain, base_url)
                results = self._merge_results(results, phase_results)

                await self.log("info", f"{phase_name} complete")
            except Exception as e:
                await self.log("warning", f"{phase_name} failed: {str(e)}")

        await self.log("info", f"Reconnaissance Summary:")
        await self.log("info", f"  Subdomains: {len(results['subdomains'])}")
        await self.log("info", f"  Live hosts: {len(results['live_hosts'])}")
        await self.log("info", f"  URLs: {len(results['urls'])}")
        await self.log("info", f"  Endpoints: {len(results['endpoints'])}")
        await self.log("info", f"  Open ports: {len(results['ports'])}")
        await self.log("info", f"  JS files: {len(results['js_files'])}")

        return results

    async def _check_tools(self):
        essential_tools = [
            "subfinder", "httpx", "nuclei", "nmap", "katana", "gau",
            "waybackurls", "ffuf", "gobuster", "amass", "naabu",
        ]
        available = [t for t in essential_tools if self._tool_exists(t)]
        missing = [t for t in essential_tools if not self._tool_exists(t)]
        await self.log("info", f"Tools available: {', '.join(available)}")
        if missing:
            await self.log("debug", f"Missing tools: {', '.join(missing)}")

    def _extract_domain(self, target: str) -> str:
        domain = target.replace("https://", "").replace("http://", "")
        domain = domain.split("/")[0]
        domain = domain.split(":")[0]
        return domain

    def _get_phases(self, depth: str) -> List[tuple]:
        quick_phases = [
            ("DNS Resolution", self._dns_resolution),
            ("HTTP Probing", self._http_probe),
            ("Basic Path Discovery", self._basic_paths),
        ]

        medium_phases = quick_phases + [
            ("Subdomain Enumeration", self._subdomain_enum),
            ("URL Collection", self._url_collection),
            ("Port Scan", self._port_scan_quick),
            ("Technology Detection", self._tech_detection),
            ("Web Crawling", self._web_crawl),
        ]

        full_phases = medium_phases + [
            ("Full Port Scan", self._port_scan_full),
            ("Parameter Discovery", self._param_discovery),
            ("JavaScript Analysis", self._js_analysis),
            ("Directory Fuzzing", self._directory_fuzz),
            ("Nuclei Vulnerability Scan", self._nuclei_scan),
        ]

        return {
            "quick": quick_phases,
            "medium": medium_phases,
            "full": full_phases,
        }.get(depth, medium_phases)

    async def _dns_resolution(self, domain: str, base_url: str) -> Dict:
        results = {"dns_records": [], "subdomains": []}
        if self._tool_exists("dnsx"):
            output = await self._run_command(
                ["dnsx", "-d", domain, "-a", "-aaaa", "-cname", "-mx", "-ns", "-txt", "-silent"],
                timeout=60,
            )
            if output:
                for line in output.strip().split("\n"):
                    if line:
                        results["dns_records"].append(line)
        if not results["dns_records"]:
            for record_type in ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]:
                output = await self._run_command(["dig", domain, record_type, "+short"], timeout=10)
                if output:
                    for line in output.strip().split("\n"):
                        if line:
                            results["dns_records"].append(f"{record_type}: {line}")
        return results

    async def _http_probe(self, domain: str, base_url: str) -> Dict:
        results = {"live_hosts": [], "endpoints": []}
        if self._tool_exists("httpx"):
            output = await self._run_command(
                ["httpx", "-u", domain, "-silent", "-status-code", "-title",
                 "-tech-detect", "-content-length", "-web-server"],
                timeout=60,
            )
            if output:
                for line in output.strip().split("\n"):
                    if line:
                        results["live_hosts"].append(line)
                        parts = line.split()
                        url = parts[0] if parts else f"https://{domain}"
                        results["endpoints"].append({
                            "url": url,
                            "method": "GET",
                            "path": "/",
                            "status": int(parts[1].strip("[]")) if len(parts) > 1 and parts[1].strip("[]").isdigit() else 200,
                            "source": "httpx",
                        })
        if not results["live_hosts"]:
            for proto in ["https", "http"]:
                url = f"{proto}://{domain}"
                output = await self._run_command(
                    ["curl", "-sI", "-m", "10", "-o", "/dev/null", "-w", "%{http_code}", url],
                    timeout=15,
                )
                if output and output.strip() not in ["000", ""]:
                    results["live_hosts"].append(f"{url} [{output.strip()}]")
                    results["endpoints"].append({
                        "url": url,
                        "status": int(output.strip()) if output.strip().isdigit() else 0,
                        "source": "curl",
                    })
        return results

    async def _basic_paths(self, domain: str, base_url: str) -> Dict:
        results = {"endpoints": [], "interesting_paths": []}
        common_paths = [
            "/", "/robots.txt", "/sitemap.xml", "/.git/config", "/.env",
            "/api", "/api/v1", "/api/v2", "/graphql", "/swagger", "/api-docs",
            "/swagger.json", "/openapi.json", "/.well-known/security.txt",
            "/admin", "/login", "/register", "/dashboard",
            "/wp-admin", "/wp-login.php", "/phpmyadmin",
            "/actuator", "/actuator/health", "/actuator/env", "/metrics",
            "/server-status", "/server-info",
            "/backup", "/config", "/config.php", "/config.json",
            "/uploads", "/files", "/static", "/assets",
            "/test", "/dev", "/staging",
            "/.git/HEAD", "/.svn/entries", "/.DS_Store",
            "/info.php", "/phpinfo.php", "/test.php",
            "/elmah.axd", "/trace.axd", "/web.config",
        ]

        if HAS_AIOHTTP:
            connector = aiohttp.TCPConnector(ssl=False, limit=20)
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = [self._check_path(session, base_url, path, results) for path in common_paths]
                await asyncio.gather(*tasks, return_exceptions=True)
        else:
            for path in common_paths:
                await self._check_path_sync(base_url, path, results)

        return results

    async def _check_path(self, session, base_url: str, path: str, results: Dict):
        try:
            url = f"{base_url.rstrip('/')}{path}"
            async with session.get(url, allow_redirects=False) as response:
                if response.status < 404:
                    endpoint = {
                        "url": url,
                        "path": path,
                        "status": response.status,
                        "content_type": response.headers.get("Content-Type", ""),
                        "content_length": response.headers.get("Content-Length", ""),
                        "source": "path_check",
                    }
                    results["endpoints"].append(endpoint)
                    sensitive_paths = ["/.git", "/.env", "/debug", "/actuator",
                                      "/backup", "/config", "/.htaccess", "/phpinfo"]
                    if any(s in path for s in sensitive_paths):
                        results["interesting_paths"].append({
                            "path": path,
                            "status": response.status,
                            "risk": "high",
                            "reason": "Potentially sensitive file/endpoint",
                        })
        except Exception:
            pass

    async def _check_path_sync(self, base_url: str, path: str, results: Dict):
        try:
            url = f"{base_url.rstrip('/')}{path}"
            output = await self._run_command(
                ["curl", "-sI", "-m", "5", "-w", "%{http_code}", "-o", "/dev/null", url],
                timeout=10,
            )
            if output and output.strip().isdigit():
                status = int(output.strip())
                if status < 404:
                    results["endpoints"].append({
                        "url": url,
                        "path": path,
                        "status": status,
                        "source": "path_check",
                    })
        except Exception:
            pass

    async def _subdomain_enum(self, domain: str, base_url: str) -> Dict:
        results = {"subdomains": []}
        found_subs = set()
        await self.log("info", f"Enumerating subdomains for {domain}")

        if self._tool_exists("subfinder"):
            output = await self._run_command(
                ["subfinder", "-d", domain, "-silent", "-all"],
                timeout=180,
            )
            if output:
                for sub in output.strip().split("\n"):
                    if sub and sub not in found_subs:
                        found_subs.add(sub)

        if self._tool_exists("amass"):
            output = await self._run_command(
                ["amass", "enum", "-passive", "-d", domain, "-timeout", "3"],
                timeout=240,
            )
            if output:
                for sub in output.strip().split("\n"):
                    if sub and sub not in found_subs:
                        found_subs.add(sub)

        if self._tool_exists("assetfinder"):
            output = await self._run_command(
                ["assetfinder", "--subs-only", domain],
                timeout=60,
            )
            if output:
                for sub in output.strip().split("\n"):
                    if sub and sub not in found_subs:
                        found_subs.add(sub)

        results["subdomains"] = list(found_subs)
        await self.log("info", f"Found {len(found_subs)} subdomains")
        return results

    async def _url_collection(self, domain: str, base_url: str) -> Dict:
        results = {"urls": [], "parameters": [], "js_files": []}
        found_urls = set()
        await self.log("info", f"Collecting URLs for {domain}")

        if self._tool_exists("gau"):
            output = await self._run_command(
                ["gau", "--threads", "5", "--subs", domain],
                timeout=180,
            )
            if output:
                for url in output.strip().split("\n")[:1000]:
                    if url and url not in found_urls:
                        found_urls.add(url)
                        if url.endswith(".js"):
                            results["js_files"].append(url)
                        if "?" in url:
                            results["parameters"].append(url)

        if self._tool_exists("waybackurls"):
            output = await self._run_command(
                ["waybackurls", domain],
                timeout=120,
            )
            if output:
                for url in output.strip().split("\n")[:1000]:
                    if url and url not in found_urls:
                        found_urls.add(url)
                        if url.endswith(".js"):
                            results["js_files"].append(url)
                        if "?" in url:
                            results["parameters"].append(url)

        results["urls"] = list(found_urls)
        await self.log("info", f"Collected {len(found_urls)} URLs, {len(results['parameters'])} with parameters")
        return results

    async def _port_scan_quick(self, domain: str, base_url: str) -> Dict:
        results = {"ports": []}
        await self.log("info", f"Port scanning {domain}")

        if self._tool_exists("naabu"):
            output = await self._run_command(
                ["naabu", "-host", domain, "-top-ports", "100", "-silent"],
                timeout=120,
            )
            if output:
                for line in output.strip().split("\n"):
                    if line:
                        results["ports"].append(line)
        elif self._tool_exists("nmap"):
            output = await self._run_command(
                ["nmap", "-sT", "-T4", "--top-ports", "100", "-oG", "-", domain],
                timeout=180,
            )
            if output:
                for line in output.split("\n"):
                    if "Ports:" in line:
                        ports_part = line.split("Ports:")[1]
                        for port_info in ports_part.split(","):
                            if "/open/" in port_info:
                                port = port_info.strip().split("/")[0]
                                results["ports"].append(f"{domain}:{port}")
        return results

    async def _port_scan_full(self, domain: str, base_url: str) -> Dict:
        results = {"ports": []}
        if self._tool_exists("naabu"):
            output = await self._run_command(
                ["naabu", "-host", domain, "-p", "-", "-silent"],
                timeout=600,
            )
            if output:
                for line in output.strip().split("\n"):
                    if line:
                        results["ports"].append(line)
        return results

    async def _tech_detection(self, domain: str, base_url: str) -> Dict:
        results = {"technologies": []}
        await self.log("info", f"Detecting technologies on {base_url}")

        if self._tool_exists("whatweb"):
            output = await self._run_command(
                ["whatweb", "-q", "-a", "3", "--color=never", base_url],
                timeout=60,
            )
            if output:
                results["technologies"].append({"source": "whatweb", "data": output.strip()})

        if self._tool_exists("wafw00f"):
            output = await self._run_command(
                ["wafw00f", base_url, "-o", "-"],
                timeout=60,
            )
            if output and "No WAF" not in output:
                results["technologies"].append({"source": "wafw00f", "data": output.strip()})

        return results

    async def _web_crawl(self, domain: str, base_url: str) -> Dict:
        results = {"endpoints": [], "js_files": [], "urls": []}
        await self.log("info", f"Crawling {base_url}")

        if self._tool_exists("katana"):
            output = await self._run_command(
                ["katana", "-u", base_url, "-d", "3", "-silent", "-jc", "-kf", "all"],
                timeout=180,
            )
            if output:
                for url in output.strip().split("\n"):
                    if url:
                        if url.endswith(".js"):
                            results["js_files"].append(url)
                        results["endpoints"].append({"url": url, "source": "katana"})
                        results["urls"].append(url)

        if self._tool_exists("gospider"):
            output = await self._run_command(
                ["gospider", "-s", base_url, "-d", "2", "-t", "5", "--no-redirect", "-q"],
                timeout=180,
            )
            if output:
                for line in output.strip().split("\n"):
                    if "[" in line and "]" in line:
                        parts = line.split(" - ")
                        if len(parts) > 1:
                            url = parts[-1].strip()
                            if url and url.startswith("http") and url not in results["urls"]:
                                results["urls"].append(url)
                                results["endpoints"].append({"url": url, "source": "gospider"})

        await self.log("info", f"Crawled {len(results['endpoints'])} endpoints, {len(results['js_files'])} JS files")
        return results

    async def _param_discovery(self, domain: str, base_url: str) -> Dict:
        results = {"parameters": []}
        await self.log("info", f"Discovering parameters for {domain}")

        if self._tool_exists("arjun"):
            output = await self._run_command(
                ["arjun", "-u", base_url, "--stable", "-oT", "/dev/stdout"],
                timeout=180,
            )
            if output:
                for line in output.strip().split("\n"):
                    if ":" in line and line not in results["parameters"]:
                        results["parameters"].append(line)
        return results

    async def _js_analysis(self, domain: str, base_url: str) -> Dict:
        results = {"secrets": [], "endpoints": [], "js_files": []}
        await self.log("info", f"Analyzing JavaScript files")
        return results

    async def _directory_fuzz(self, domain: str, base_url: str) -> Dict:
        results = {"endpoints": []}
        wordlist = self.wordlists_path / "common.txt"
        if not wordlist.exists():
            return results

        await self.log("info", f"Fuzzing directories on {base_url}")

        if self._tool_exists("ffuf"):
            output = await self._run_command(
                ["ffuf", "-u", f"{base_url}/FUZZ", "-w", str(wordlist),
                 "-mc", "200,201,204,301,302,307,401,403,405",
                 "-t", "50", "-o", "-", "-of", "json"],
                timeout=180,
            )
            if output:
                try:
                    data = json.loads(output)
                    for r_data in data.get("results", []):
                        results["endpoints"].append({
                            "url": r_data.get("url", ""),
                            "status": r_data.get("status", 0),
                            "length": r_data.get("length", 0),
                            "source": "ffuf",
                        })
                except Exception:
                    pass
        elif self._tool_exists("gobuster"):
            output = await self._run_command(
                ["gobuster", "dir", "-u", base_url, "-w", str(wordlist),
                 "-t", "50", "-q", "--no-error"],
                timeout=180,
            )
            if output:
                for line in output.strip().split("\n"):
                    if line and "(Status:" in line:
                        parts = line.split()
                        if parts:
                            path = parts[0]
                            results["endpoints"].append({
                                "url": f"{base_url}{path}",
                                "path": path,
                                "source": "gobuster",
                            })
        return results

    async def _nuclei_scan(self, domain: str, base_url: str) -> Dict:
        results = {"vulnerabilities": []}
        if not self._tool_exists("nuclei"):
            return results

        await self.log("info", f"Running Nuclei scan on {base_url}")
        output = await self._run_command(
            ["nuclei", "-u", base_url, "-severity", "critical,high,medium",
             "-silent", "-json", "-c", "25"],
            timeout=600,
        )

        if output:
            for line in output.strip().split("\n"):
                if line:
                    try:
                        vuln = json.loads(line)
                        results["vulnerabilities"].append({
                            "name": vuln.get("info", {}).get("name", "Unknown"),
                            "severity": vuln.get("info", {}).get("severity", "unknown"),
                            "url": vuln.get("matched-at", ""),
                            "template": vuln.get("template-id", ""),
                            "description": vuln.get("info", {}).get("description", ""),
                            "matcher_name": vuln.get("matcher-name", ""),
                        })
                        severity = vuln.get("info", {}).get("severity", "unknown").upper()
                        await self.log("warning", f"NUCLEI [{severity}]: {vuln.get('info', {}).get('name')}")
                    except Exception:
                        pass

        await self.log("info", f"Nuclei found {len(results['vulnerabilities'])} issues")
        return results

    def _merge_results(self, base: Dict, new: Dict) -> Dict:
        for key, value in new.items():
            if key in base:
                if isinstance(value, list):
                    existing = set(str(x) for x in base[key])
                    for item in value:
                        if str(item) not in existing:
                            base[key].append(item)
                            existing.add(str(item))
                elif isinstance(value, dict):
                    base[key].update(value)
            else:
                base[key] = value
        return base


async def check_tools_installed() -> Dict[str, bool]:
    tools = [
        "subfinder", "amass", "assetfinder",
        "dnsx", "httpx",
        "gau", "waybackurls", "katana", "gospider",
        "nmap", "naabu",
        "whatweb", "wafw00f",
        "ffuf", "gobuster", "dirb", "dirsearch", "wfuzz",
        "arjun",
        "nuclei", "nikto", "sqlmap", "dalfox",
        "curl", "wget", "dig", "whois",
    ]
    results = {}
    for tool in tools:
        results[tool] = shutil.which(tool) is not None
    return results