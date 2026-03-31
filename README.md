# cc-mini

A lightweight Python implementation of [Claude Code](https://claude.ai/code) for the community — a terminal-based AI coding assistant that runs an agentic tool loop via the Anthropic API.

## Features

- **Interactive REPL** with command history
- **Streaming responses** — text appears as it is generated
- **Agentic tool loop** — multiple tool calls per turn
- **5 built-in tools**: file read, file edit, glob, grep, bash
- **Permission system** — reads auto-approved, writes/bash ask for confirmation

## Requirements

- Python 3.11+
- [Anthropic API key](https://console.anthropic.com/)

## Installation

```bash
cd /path/to/cc-mini
pip install -e ".[dev]"
```

## Usage

### Set API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Custom API base URL (useful for proxies or compatible endpoints):

```bash
export ANTHROPIC_BASE_URL=https://your-gateway.example.com
```

Optional environment variables for runtime defaults:

```bash
export CC_MINI_MODEL=claude-sonnet-4-5
export CC_MINI_MAX_TOKENS=64000
```

### Interactive REPL

```bash
cc-mini
```

```
cc-mini  type 'exit' or Ctrl+C to quit

> list all python files in this project
↳ Glob(**/*.py) ✓
Here are all the .py files...

> read engine.py and explain how the tool loop works
↳ Read(src/core/engine.py) ✓
The submit() method implements an agentic loop...
```

Type `exit` or press `Ctrl+C` to quit.

### One-shot prompt

```bash
cc-mini "what tests exist in this project?"
```

### Non-interactive / scripted mode

Use `-p` to print the response and exit:

```bash
cc-mini -p "summarize this codebase in 3 bullets"
```

Pipe input:

```bash
echo "what does engine.py do?" | cc-mini -p
```

### Auto-approve permissions

Skip permission prompts for all tools (use with care):

```bash
cc-mini --auto-approve
```

### Configure API endpoint and model from CLI

```bash
cc-mini \
  --base-url https://your-gateway.example.com \
  --api-key sk-ant-... \
  --model claude-sonnet-4
```

`max_tokens` follows the selected model by default. Override when you need a tighter cap:

```bash
cc-mini --model claude-3-5-haiku --max-tokens 2048
```

### Configure with a TOML file

Config files are loaded in this order:

1. `~/.config/cc-mini/config.toml`
2. `.cc-mini.toml` in the current working directory

The project-local file overrides the home config. Point to a specific file with `--config`.

Example:

```toml
[anthropic]
api_key = "sk-ant-..."
base_url = "https://your-gateway.example.com"
model = "claude-sonnet-4"
```

Top-level keys are also supported:

```toml
api_key = "sk-ant-..."
base_url = "https://your-gateway.example.com"
model = "claude-3-7-sonnet"
max_tokens = 64000
```

## Tools

| Tool | Name | Permission |
|------|------|------------|
| Read file | `Read` | auto-approved |
| Find files | `Glob` | auto-approved |
| Search content | `Grep` | auto-approved |
| Edit file | `Edit` | requires confirmation |
| Run command | `Bash` | requires confirmation |

### Permission prompt

When the assistant wants to run a write or bash tool, you'll see:

```
Permission required: Bash
  command: pytest tests/ -v

  Allow? [y]es / [n]o / [a]lways:
```

- `y` — allow once
- `n` — deny
- `a` — always allow this tool for the rest of the session

## Project structure

```
src/core/
├── main.py         # CLI entry point + REPL
├── engine.py       # Streaming API loop + tool execution
├── context.py      # System prompt builder (git status, date)
├── permissions.py  # Permission checker
└── tools/
    ├── base.py     # Tool ABC + ToolResult
    ├── file_read.py
    ├── file_edit.py
    ├── glob_tool.py
    ├── grep_tool.py
    └── bash.py
```

## Running tests

```bash
pytest tests/ -v
```

## Tips

- Place a `CLAUDE.md` file in your project root — it will be included in the system prompt automatically
- Use `--auto-approve` when running non-interactively or for trusted tasks
- The REPL keeps conversation history within a session; each new run starts fresh
