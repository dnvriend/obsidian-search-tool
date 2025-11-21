---
description: Search vault with Dataview DQL or JsonLogic
argument-hint: query
---

Search Obsidian vault using Dataview DQL TABLE queries or JsonLogic.

## Usage

```bash
obsidian-search-tool search QUERY [--type dataview|jsonlogic] [--json|--text|--table] [-v|-vv|-vvv]
obsidian-search-tool search --stdin [OPTIONS]
```

## Arguments

- `QUERY`: Search query (required, or use --stdin)
- `--type`: Query type - dataview (default) or jsonlogic
- `--stdin` / `-s`: Read query from stdin
- `--json`: JSON output (default)
- `--text` / `-t`: Markdown text output
- `--table`: Pretty-printed table output
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)

## Examples

```bash
# Dataview TABLE query
obsidian-search-tool search 'TABLE file.name FROM "daily" LIMIT 5'

# JsonLogic content search
obsidian-search-tool search --type jsonlogic '{"in": ["Claude", {"var": "content"}]}'

# From stdin
echo 'TABLE file.name WHERE file.size > 1000' | obsidian-search-tool search --stdin

# With table output
obsidian-search-tool search 'TABLE file.name, file.size' --table
```

## Output

Returns query, search type, timestamp, result count, and matching files.
