---
name: skill-obsidian-search-tool
description: Search Obsidian vault via DQL and JsonLogic
---

# When to use
- Search Obsidian vault from command line
- Query notes with Dataview TABLE queries
- Filter notes with JsonLogic expressions
- Integrate Obsidian search in workflows

# Obsidian Search Tool Skill

## Purpose

A professional CLI tool for searching an Obsidian vault through the Obsidian Local REST API using Dataview Query Language (DQL) TABLE queries and JsonLogic queries. Enables programmatic access to Obsidian notes for automation, scripting, and integration workflows.

## When to Use This Skill

**Use this skill when:**
- You need to search an Obsidian vault from the command line
- You want to query notes using Dataview DQL TABLE syntax
- You need to filter notes with JsonLogic expressions
- You're building automation workflows that interact with Obsidian
- You want to integrate Obsidian search into CI/CD pipelines

**Do NOT use this skill for:**
- Modifying or creating Obsidian notes (read-only tool)
- Searching without Obsidian Local REST API plugin
- Complex queries requiring GROUP BY or FLATTEN (API limitation)

## CLI Tool: obsidian-search-tool

Python CLI tool (version 0.1.0) that interfaces with Obsidian's Local REST API plugin to perform searches using Dataview Query Language and JsonLogic.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/obsidian-search-tool.git
cd obsidian-search-tool

# Install with uv
uv tool install .

# Or install from source
uv sync
uv tool install . --reinstall
```

### Prerequisites

1. **Obsidian** must be running
2. **Local REST API plugin** by Adam Coddington installed and enabled
3. **Dataview plugin** by Michael Brenan installed and enabled
4. **OBSIDIAN_API_KEY** environment variable set with API key from plugin settings

```bash
# Set API key (get from Obsidian → Settings → Community Plugins → Local REST API)
export OBSIDIAN_API_KEY="your-api-key-here"
```

### Quick Start

```bash
# Check API connectivity
obsidian-search-tool status

# Validate authentication
obsidian-search-tool auth

# Search with Dataview DQL
obsidian-search-tool search 'TABLE file.name FROM "daily" LIMIT 5'

# Search with JsonLogic
obsidian-search-tool search --type jsonlogic '{"in": ["keyword", {"var": "content"}]}'
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### status - Check API Connectivity

Verifies that the Obsidian Local REST API is reachable and responding. Use this to debug connection issues before performing searches.

**Usage:**
```bash
obsidian-search-tool status [OPTIONS]
```

**Options:**
- `--json`: JSON output (default, machine-readable)
- `--text` / `-t`: Markdown-formatted text output
- `-v`: INFO level logging (operation status)
- `-vv`: DEBUG level logging (detailed operations)
- `-vvv`: TRACE level logging (full HTTP details + library internals)

**Examples:**
```bash
# Basic status check with JSON output
obsidian-search-tool status

# Human-readable text output
obsidian-search-tool status --text

# With verbose logging for debugging
obsidian-search-tool status -vv

# Trace mode with urllib3 logging
obsidian-search-tool status -vvv
```

**Output (JSON):**
```json
{
  "success": true,
  "data": {
    "status": "connected",
    "api_url": "http://127.0.0.1:27123",
    "timestamp": "2025-11-21T10:00:00+00:00",
    "message": "API is reachable"
  }
}
```

**Common Errors:**
- `Connection failed`: Obsidian not running or plugin disabled
- `OBSIDIAN_API_KEY environment variable is required`: API key not set
- `Request timeout`: Increase OBSIDIAN_TIMEOUT or check network

---

### auth - Validate Authentication

Verifies that the API key is valid and authentication is working correctly. Use this to test your OBSIDIAN_API_KEY before performing searches.

**Usage:**
```bash
obsidian-search-tool auth [OPTIONS]
```

**Options:**
- `--json`: JSON output (default)
- `--text` / `-t`: Markdown-formatted text output
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Examples:**
```bash
# Basic auth check
obsidian-search-tool auth

# With text output
obsidian-search-tool auth --text

# With debug logging
obsidian-search-tool auth -vv
```

**Output (JSON):**
```json
{
  "success": true,
  "data": {
    "status": "authenticated",
    "api_url": "http://127.0.0.1:27123",
    "timestamp": "2025-11-21T10:00:00+00:00",
    "message": "Authentication is valid"
  }
}
```

**Getting Your API Key:**
1. Open Obsidian
2. Go to Settings → Community Plugins
3. Find "Local REST API" plugin
4. Click plugin settings
5. Copy the API key
6. Set environment variable: `export OBSIDIAN_API_KEY="your-key"`

---

### search - Search Vault

Search Obsidian vault using Dataview DQL TABLE queries or JsonLogic queries.

**Usage:**
```bash
obsidian-search-tool search QUERY [OPTIONS]
obsidian-search-tool search --stdin [OPTIONS]
```

**Arguments:**
- `QUERY`: Search query string (required unless --stdin)
- `--type`: Query type - `dataview` (default) or `jsonlogic`
- `--stdin` / `-s`: Read query from stdin (mutually exclusive with positional query)
- `--json`: JSON output (default, machine-readable)
- `--text` / `-t`: Markdown-formatted text output
- `--table`: Pretty-printed table output (best for TABLE results)
- `-v/-vv/-vvv`: Verbosity levels (INFO/DEBUG/TRACE)

**Dataview DQL Examples:**
```bash
# Basic TABLE query with FROM
obsidian-search-tool search 'TABLE file.name FROM "daily" LIMIT 5'

# Recent notes with date functions
obsidian-search-tool search 'TABLE file.name, file.mtime WHERE file.mtime >= date(today) - dur(7 days) SORT file.mtime DESC'

# Folder filtering with contains()
obsidian-search-tool search 'TABLE file.name, file.folder WHERE contains(file.folder, "reference")'

# Large files sorted by size
obsidian-search-tool search 'TABLE file.name, file.size WHERE file.size > 10000 SORT file.size DESC LIMIT 10'

# Complex multi-condition query
obsidian-search-tool search 'TABLE file.name FROM "docs" WHERE file.size > 5000 AND file.mtime >= date(today) - dur(30 days)'
```

**JsonLogic Examples:**
```bash
# Content search
obsidian-search-tool search --type jsonlogic '{"in": ["Claude", {"var": "content"}]}'

# Filename contains
obsidian-search-tool search --type jsonlogic '{"in": ["daily", {"var": "filename"}]}'

# Tag search
obsidian-search-tool search --type jsonlogic '{"in": [{"var": "frontmatter.tags"}, "aws"]}'
```

**Output Formats:**
```bash
# JSON output (default, for scripting)
obsidian-search-tool search 'TABLE file.name'

# Markdown text output (human-readable)
obsidian-search-tool search 'TABLE file.name' --text

# Pretty table output (best for TABLE results)
obsidian-search-tool search 'TABLE file.name, file.size' --table
```

**Stdin Input:**
```bash
# Read query from stdin (useful for piping)
echo 'TABLE file.name FROM #meeting' | obsidian-search-tool search --stdin

# From file
cat query.txt | obsidian-search-tool search --stdin
```

**Output (JSON):**
```json
{
  "success": true,
  "data": {
    "query": "TABLE file.name FROM \"daily\" LIMIT 5",
    "search_type": "dataview",
    "timestamp": "2025-11-21T10:00:00+00:00",
    "results": [
      {"filename": "daily/2025-11/2025-11-21.md", "result": true},
      {"filename": "daily/2025-11/2025-11-20.md", "result": true}
    ]
  }
}
```

---

### completion - Shell Completion

Generate shell completion scripts for bash, zsh, or fish to enable tab completion.

**Usage:**
```bash
obsidian-search-tool completion SHELL
```

**Arguments:**
- `SHELL`: Shell type (`bash`, `zsh`, or `fish`)

**Installation Examples:**
```bash
# Bash (temporary - current session)
eval "$(obsidian-search-tool completion bash)"

# Bash (permanent)
echo 'eval "$(obsidian-search-tool completion bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh (permanent)
echo 'eval "$(obsidian-search-tool completion zsh)"' >> ~/.zshrc
source ~/.zshrc

# Fish (persistent)
mkdir -p ~/.config/fish/completions
obsidian-search-tool completion fish > ~/.config/fish/completions/obsidian-search-tool.fish
```

**What Gets Completed:**
- Command names: `status`, `auth`, `search`, `completion`
- Options: `--json`, `--text`, `--table`, `--verbose`, `-v`, `-vv`, `-vvv`
- Choice values: `--type dataview|jsonlogic`, `bash|zsh|fish`
- File paths where applicable

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Dataview DQL Capabilities

#### Supported Data Commands

Commands refine query results and execute in order:

1. **FROM** - Select source pages (tags, folders, files, links)
   ```dataview
   FROM #tag               # By tag (includes subtags)
   FROM "folder"           # By folder (includes subfolders)
   FROM [[note]]           # Pages linking TO note
   FROM outgoing([[note]]) # Pages linked FROM note
   ```

2. **WHERE** - Filter pages based on conditions
   ```dataview
   WHERE file.size > 1000                          # Comparison
   WHERE contains(file.folder, "ai-ml")            # Contains check
   WHERE file.mtime >= date(today) - dur(7 days)   # Date-based
   ```

3. **SORT** - Sort results by one or more fields
   ```dataview
   SORT file.mtime DESC                            # Single field
   SORT file.folder ASC, file.mtime DESC          # Multiple fields
   ```

4. **LIMIT** - Restrict result count
   ```dataview
   LIMIT 10                                        # Top 10 results
   ```

#### API Limitations

**Not Supported:**
- **GROUP BY**: Returns "TABLE WITHOUT ID queries are not supported"
- **FLATTEN**: Returns "TABLE WITHOUT ID queries are not supported"
- **LIST/TASK/CALENDAR**: Only TABLE queries supported

#### Implicit Fields (file.*)

All pages have automatic metadata:

- **Basic**: `file.name`, `file.path`, `file.folder`, `file.size`, `file.ext`
- **Dates**: `file.ctime`, `file.mtime`, `file.cday`, `file.mday`
- **Links/Tags**: `file.tags`, `file.etags`, `file.inlinks`, `file.outlinks`
- **Content**: `file.tasks`, `file.lists`, `file.frontmatter`

#### Common Functions

- **Constructors**: `date()`, `dur()`, `list()`, `link()`
- **Numeric**: `round()`, `min()`, `max()`, `sum()`, `length()`
- **String**: `contains()`, `lower()`, `upper()`, `split()`, `replace()`
- **Logic**: `all()`, `any()`, `none()`, `choice()`, `default()`
- **Date/Time**: `dateformat()`, `striptime()`

### JsonLogic Capabilities

#### Available Variables

- `filename`: File path relative to vault root
- `frontmatter.*`: YAML frontmatter fields (e.g., `frontmatter.tags`)
- `content`: Full file content (for text search)

#### Supported Operators

- `in`: Substring/membership check (works reliably)
- Standard logic: `and`, `or`, `not`
- Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`

#### Limitations

- `startsWith`/`endsWith`: Not supported by API (returns "Unrecognized operation")
- Use `in` operator for substring matching instead

### Multi-Level Verbosity

Progressive logging detail control:

- **No flag** (default): WARNING level - only errors
- **`-v`**: INFO level - operation status, high-level events
- **`-vv`**: DEBUG level - detailed operations, API calls, validation
- **`-vvv`**: TRACE level - full HTTP requests, urllib3 internals, tracebacks

**Examples:**
```bash
# Quiet mode (warnings only)
obsidian-search-tool status

# Verbose mode (operations)
obsidian-search-tool search 'TABLE file.name' -v

# Debug mode (API details)
obsidian-search-tool search 'TABLE file.name' -vv

# Trace mode (HTTP internals)
obsidian-search-tool search 'TABLE file.name' -vvv
```

### Environment Variables

- `OBSIDIAN_API_KEY` (required): API token from plugin settings
- `OBSIDIAN_BASE_URL` (optional): API URL (default: http://127.0.0.1:27123)
- `OBSIDIAN_TIMEOUT` (optional): Request timeout in seconds (default: 30)

### Output Piping

JSON output goes to stdout, logs to stderr for clean piping:

```bash
# Pipe to jq for processing
obsidian-search-tool search 'TABLE file.name' --json | jq '.data.results[].filename'

# Count results
obsidian-search-tool search 'TABLE file.name' --json | jq '.data.results | length'

# Extract specific fields
obsidian-search-tool search 'TABLE file.name, file.size' --json | jq '.data.results[] | select(.file.size > 10000)'
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: "OBSIDIAN_API_KEY environment variable is required"**
```bash
# Symptom
Error: OBSIDIAN_API_KEY environment variable is required
```

**Solution:**
1. Open Obsidian → Settings → Community Plugins
2. Find "Local REST API" plugin settings
3. Copy the API key
4. Set environment variable: `export OBSIDIAN_API_KEY="your-key-here"`
5. Add to shell profile (~/.bashrc, ~/.zshrc) for persistence

---

**Issue: "Connection failed to http://127.0.0.1:27123"**
```bash
# Symptom
ConnectionRefusedError: [Errno 61] Connection refused
```

**Solution:**
1. Ensure Obsidian is running
2. Verify Local REST API plugin is installed and enabled
3. Check plugin settings show correct port (default: 27123)
4. Try accessing http://127.0.0.1:27123 in browser

---

**Issue: "Only TABLE dataview queries are supported"**
```bash
# Symptom
Error: Only TABLE dataview queries are supported
```

**Solution:**
- Use TABLE queries only, not LIST/TASK/CALENDAR
- Example: `TABLE file.name FROM #tag` instead of `LIST FROM #tag`

---

**Issue: "TABLE WITHOUT ID queries are not supported"**
```bash
# Symptom
Error: TABLE WITHOUT ID queries are not supported
```

**Solution:**
- Don't use GROUP BY or FLATTEN
- Use WHERE with contains() instead for filtering
- Example: `WHERE contains(file.folder, "reference")` instead of GROUP BY

---

**Issue: "Unrecognized operation startsWith"**
```bash
# Symptom with JsonLogic
Error: Unrecognized operation startsWith
```

**Solution:**
- Use `in` operator for substring matching
- Example: `{"in": ["prefix", {"var": "filename"}]}` instead of startsWith

---

**Issue: No results found but files exist**

**Solution:**
- Check query syntax carefully
- Verify folder paths use quotes: `FROM "folder"` not `FROM folder`
- Use contains() for partial matches
- Test with simpler query first

### Getting Help

```bash
# Main help
obsidian-search-tool --help

# Command-specific help
obsidian-search-tool status --help
obsidian-search-tool auth --help
obsidian-search-tool search --help
obsidian-search-tool completion --help

# Version info
obsidian-search-tool --version
```

### Debug Workflow

1. **Check connectivity**: `obsidian-search-tool status -vv`
2. **Verify auth**: `obsidian-search-tool auth -vv`
3. **Test simple query**: `obsidian-search-tool search 'TABLE file.name LIMIT 1' -vv`
4. **Add complexity gradually**

</details>

## Exit Codes

- `0`: Success
- `1`: Client error (authentication, connection, API error)
- `2-255`: Other errors

## Output Formats

**JSON (default)**:
- Machine-readable
- Parseable with jq
- All logging to stderr
- Perfect for scripting

**Text (`--text`)**:
- Human-readable markdown
- File paths with metadata
- Summary statistics
- Good for terminal viewing

**Table (`--table`)**:
- Pretty-printed columns
- Best for TABLE query results
- Aligned columns
- Terminal-optimized

## Best Practices

1. **Start with connectivity**: Always run `status` and `auth` first
2. **Use verbosity wisely**: Start with `-v`, escalate to `-vv` for debugging
3. **Test queries incrementally**: Start simple, add complexity gradually
4. **Pipe JSON output**: Use `--json | jq` for processing results
5. **Save complex queries**: Store in files and use `--stdin`
6. **Check API limitations**: No GROUP BY, FLATTEN, or non-TABLE queries
7. **Use contains() for flexibility**: Better than exact matches for folders/content
8. **Enable completion**: Install shell completion for better UX

## Resources

- **GitHub**: https://github.com/dnvriend/obsidian-search-tool
- **Obsidian Local REST API**: https://github.com/coddingtonbear/obsidian-local-rest-api
- **Dataview Plugin**: https://github.com/blacksmithgu/obsidian-dataview
- **JsonLogic Spec**: https://jsonlogic.com/
