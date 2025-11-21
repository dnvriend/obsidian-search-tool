---
description: Validate Obsidian API authentication
---

Verify that the API key is valid and authentication is working.

## Usage

```bash
obsidian-search-tool auth [--json|--text] [-v|-vv|-vvv]
```

## Options

- `--json`: JSON output (default)
- `--text` / `-t`: Markdown text output
- `-v`: INFO level logging
- `-vv`: DEBUG level logging
- `-vvv`: TRACE level with library internals

## Examples

```bash
# Basic auth check
obsidian-search-tool auth

# With text output
obsidian-search-tool auth --text

# With debug logging
obsidian-search-tool auth -vv
```

## Output

Returns authentication status, API URL, timestamp, and message.
