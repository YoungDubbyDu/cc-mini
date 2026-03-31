import subprocess
from .base import Tool, ToolResult

_DEFAULT_TIMEOUT = 120


class BashTool(Tool):
    name = "Bash"
    description = (
        "Execute a bash command. Returns stdout + stderr. "
        "Timeout defaults to 120s. Avoid interactive commands."
    )
    input_schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The bash command to execute"},
            "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 120},
        },
        "required": ["command"],
    }

    def execute(self, command: str, timeout: int = _DEFAULT_TIMEOUT) -> ToolResult:
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=timeout
            )
            parts = []
            if result.stdout:
                parts.append(result.stdout.rstrip())
            if result.stderr:
                parts.append(f"[stderr]\n{result.stderr.rstrip()}")
            if result.returncode != 0:
                parts.append(f"[exit code: {result.returncode}]")
            return ToolResult(content="\n".join(parts) if parts else "(no output)")
        except subprocess.TimeoutExpired:
            return ToolResult(content=f"Error: Command timed out after {timeout}s", is_error=True)
        except Exception as e:
            return ToolResult(content=f"Error: {e}", is_error=True)
