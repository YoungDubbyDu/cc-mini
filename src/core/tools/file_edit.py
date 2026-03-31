from pathlib import Path
from .base import Tool, ToolResult


class FileEditTool(Tool):
    name = "Edit"
    description = (
        "Performs exact string replacement in a file. "
        "old_string must uniquely match — fails if 0 or 2+ occurrences found. "
        "Set replace_all=true to replace every occurrence."
    )
    input_schema = {
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Absolute path to file"},
            "old_string": {"type": "string", "description": "Exact string to replace"},
            "new_string": {"type": "string", "description": "Replacement string"},
            "replace_all": {"type": "boolean", "description": "Replace all occurrences", "default": False},
        },
        "required": ["file_path", "old_string", "new_string"],
    }

    def execute(self, file_path: str, old_string: str, new_string: str,
                replace_all: bool = False) -> ToolResult:
        path = Path(file_path)
        if not path.exists():
            return ToolResult(content=f"Error: File not found: {file_path}", is_error=True)
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            return ToolResult(content=f"Error reading file: {e}", is_error=True)

        count = content.count(old_string)
        if count == 0:
            return ToolResult(content=f"Error: old_string not found in {file_path}", is_error=True)
        if count > 1 and not replace_all:
            return ToolResult(
                content=f"Error: old_string found {count} times. Use replace_all=true or add more context.",
                is_error=True,
            )

        new_content = content.replace(old_string, new_string) if replace_all else content.replace(old_string, new_string, 1)
        try:
            path.write_text(new_content, encoding="utf-8")
        except OSError as e:
            return ToolResult(content=f"Error writing file: {e}", is_error=True)

        replaced = count if replace_all else 1
        return ToolResult(content=f"Successfully replaced {replaced} occurrence(s) in {file_path}")
