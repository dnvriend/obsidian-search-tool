---
description: Check Obsidian API connectivity status
---

Check if the Obsidian Local REST API is reachable and responding.

## Usage

```bash
obsidian-search-tool status [--json|--text] [-v|-vv|-vvv]
```

## Options

- `--json`: JSON output (default)
- `--text` / `-t`: Markdown text output
- `-v`: INFO level logging
- `-vv`: DEBUG level logging
- `-vvv`: TRACE level with library internals

## Examples

```bash
# Basic status check
obsidian-search-tool status

# With text output
obsidian-search-tool status --text

# With verbose logging
obsidian-search-tool status -vv
```

## Output

Returns connection status, API URL, timestamp, and message.
