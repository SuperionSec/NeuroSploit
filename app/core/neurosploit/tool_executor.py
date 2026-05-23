"""
NeuroSploit v3 - Tool Execution Coordinator

HTTP-based tool execution coordinator that replaces Docker sandbox.
Keeps all HTTP-based tools, removes Docker container dependency.
Supports graceful degradation when tools are unavailable.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """Result from a tool execution."""
    tool: str
    command: str = ""
    exit_code: int = -1
    stdout: str = ""
    stderr: str = ""
    duration: float = 0.0
    findings: List[Dict] = field(default_factory=list)
    success: bool = False


class ToolExecutor:
    """Execute security tools via subprocess with graceful degradation.

    No Docker dependency. Tools run directly if available on the system PATH.
    """

    DEFAULT_TIMEOUT = 120
    MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB max output

    TOOL_DEFINITIONS = {
        "nuclei": {"cmd": ["nuclei"], "timeout": 600},
        "nmap": {"cmd": ["nmap"], "timeout": 300},
        "nikto": {"cmd": ["nikto"], "timeout": 300},
        "sqlmap": {"cmd": ["sqlmap"], "timeout": 600},
        "ffuf": {"cmd": ["ffuf"], "timeout": 300},
        "gobuster": {"cmd": ["gobuster"], "timeout": 300},
        "curl": {"cmd": ["curl"], "timeout": 60},
        "python3": {"cmd": ["python3"], "timeout": 120},
        "whatweb": {"cmd": ["whatweb"], "timeout": 120},
        "wafw00f": {"cmd": ["wafw00f"], "timeout": 60},
        "httpx": {"cmd": ["httpx"], "timeout": 60},
        "katana": {"cmd": ["katana"], "timeout": 180},
        "subfinder": {"cmd": ["subfinder"], "timeout": 180},
        "dalfox": {"cmd": ["dalfox"], "timeout": 180},
        "naabu": {"cmd": ["naabu"], "timeout": 120},
        "dnsx": {"cmd": ["dnsx"], "timeout": 60},
    }

    def __init__(self):
        self._initialized = True
        self._available_tools: Dict[str, bool] = {}

    def is_available(self) -> bool:
        return self._initialized

    def _tool_exists(self, tool: str) -> bool:
        """Check if a tool exists on PATH."""
        if tool not in self._available_tools:
            try:
                result = subprocess.run(
                    ["which", tool],
                    capture_output=True, text=True, timeout=5
                )
                self._available_tools[tool] = result.returncode == 0
            except Exception:
                self._available_tools[tool] = False
        return self._available_tools[tool]

    async def run(self, tool: str, command: str, timeout: Optional[int] = None) -> ToolResult:
        """Execute a tool command asynchronously."""
        tool_def = self.TOOL_DEFINITIONS.get(tool.lower(), {})
        effective_timeout = timeout or tool_def.get("timeout", self.DEFAULT_TIMEOUT)
        effective_timeout = min(effective_timeout, 600)

        start_time = time.time()
        result = ToolResult(tool=tool, command=command)

        if not self._tool_exists(tool.lower()):
            result.exit_code = -1
            result.stderr = f"Tool '{tool}' not available (graceful degradation)"
            result.success = False
            result.duration = time.time() - start_time
            return result

        try:
            # Build command safely
            if tool.lower() != "raw" and tool.lower() in self.TOOL_DEFINITIONS:
                base_cmd = self.TOOL_DEFINITIONS[tool.lower()]["cmd"]
                extra_args = command.split()
                full_cmd = base_cmd + extra_args if extra_args else []
            else:
                full_cmd = command.split()

            process = await asyncio.create_subprocess_exec(
                *full_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=effective_timeout,
                )

                result.exit_code = process.returncode or 0
                result.stdout = stdout.decode('utf-8', errors='replace')[:self.MAX_OUTPUT_SIZE] if stdout else ""
                result.stderr = stderr.decode('utf-8', errors='replace')[:self.MAX_OUTPUT_SIZE // 2] if stderr else ""
                result.success = result.exit_code == 0

            except asyncio.TimeoutError:
                try:
                    process.kill()
                except Exception:
                    pass
                result.exit_code = -1
                result.stderr = f"Tool execution timed out after {effective_timeout}s"
                result.success = False

        except Exception as e:
            result.exit_code = -1
            result.stderr = str(e)
            result.success = False

        result.duration = time.time() - start_time
        return result

    def parse_output(self, tool: str, output: str, target: str) -> List[Dict]:
        """Parse tool output into findings using regex-based parsers."""
        parsers = {
            "nuclei": self._parse_nuclei,
            "nmap": self._parse_nmap,
            "nikto": self._parse_nikto,
            "ffuf": self._parse_ffuf,
            "gobuster": self._parse_gobuster,
        }
        parser = parsers.get(tool.lower())
        if parser:
            return parser(output, target)
        return []

    def _parse_nuclei(self, output: str, target: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                findings.append({
                    "title": data.get('info', {}).get('name', 'Unknown'),
                    "severity": data.get('info', {}).get('severity', 'info'),
                    "vulnerability_type": data.get('info', {}).get('tags', ['vulnerability'])[0]
                        if data.get('info', {}).get('tags') else 'vulnerability',
                    "description": data.get('info', {}).get('description', ''),
                    "affected_endpoint": data.get('matched-at', target),
                    "evidence": data.get('matcher-name', ''),
                    "remediation": data.get('info', {}).get('remediation', 'Review and fix'),
                    "references": data.get('info', {}).get('reference', []),
                })
            except json.JSONDecodeError:
                continue
        return findings

    def _parse_nmap(self, output: str, target: str) -> List[Dict]:
        findings = []
        port_pattern = r'(\d+)/tcp\s+open\s+(\S+)\s*(.*)?'
        for match in re.finditer(port_pattern, output):
            port = match.group(1)
            service = match.group(2)
            version = match.group(3) or ''
            severity = "medium" if service in ['telnet', 'ftp'] else "info"
            findings.append({
                "title": f"Open Port: {port}/{service}",
                "severity": severity,
                "vulnerability_type": "Open Port",
                "description": f"Port {port} is open running {service} {version}".strip(),
                "affected_endpoint": f"{target}:{port}",
                "evidence": f"Service: {service}, Version: {version}",
                "remediation": "Review if this port should be exposed",
            })
        return findings

    def _parse_nikto(self, output: str, target: str) -> List[Dict]:
        findings = []
        vuln_pattern = r'\+\s+(\S+):\s+(.+)'
        for match in re.finditer(vuln_pattern, output):
            ref = match.group(1)
            desc = match.group(2)
            severity = "high" if any(x in desc.lower() for x in ['sql', 'injection', 'xss']) else "info"
            findings.append({
                "title": f"Nikto: {desc[:50]}...",
                "severity": severity,
                "vulnerability_type": "Web Vulnerability",
                "description": desc,
                "affected_endpoint": target,
                "evidence": ref,
                "remediation": "Review and address the finding",
            })
        return findings

    def _parse_ffuf(self, output: str, target: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for result in data.get('results', []):
                url = result.get('url', '')
                status = result.get('status', 0)
                length = result.get('length', 0)
                findings.append({
                    "title": f"Found: {url.split('/')[-1]}",
                    "severity": "info",
                    "vulnerability_type": "Content Discovery",
                    "description": f"Discovered: {url}",
                    "affected_endpoint": url,
                    "evidence": f"HTTP {status}, Length: {length}",
                    "remediation": "Review if endpoint should be accessible",
                })
        except json.JSONDecodeError:
            pass
        return findings

    def _parse_gobuster(self, output: str, target: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            match = re.search(r'(/[^\s]+)\s+\(Status:\s*(\d+)\)', line)
            if match:
                path = match.group(1)
                status = match.group(2)
                url = target.rstrip('/') + path
                findings.append({
                    "title": f"Found: {path}",
                    "severity": "info",
                    "vulnerability_type": "Content Discovery",
                    "description": f"Discovered endpoint at {url}",
                    "affected_endpoint": url,
                    "evidence": f"HTTP {status}",
                    "remediation": "Review endpoint accessibility",
                })
        return findings


# Global executor instance
_executor: Optional[ToolExecutor] = None


def get_tool_executor() -> ToolExecutor:
    global _executor
    if _executor is None:
        _executor = ToolExecutor()
    return _executor