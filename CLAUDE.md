# Obsidian Search Tool - Developer Guide

## Overview

`obsidian-search-tool` is a professional Python CLI tool for searching Obsidian vaults through the Obsidian Local REST API. Built with Python 3.14+, uv, Click, and modern Python tooling.

**Tech Stack**: Python 3.14+, uv, mise, Click, requests, rich, mypy, ruff, pytest

## Architecture

### Project Structure

```
obsidian-search-tool/
├── obsidian_search_tool/
│   ├── __init__.py          # Public API exports, version=0.1.0
│   ├── cli.py              # CLI entry point (Click group)
│   ├── core/               # Core library (importable, CLI-independent)
│   │   ├── __init__.py
│   │   ├── client.py       # ObsidianClient class (API communication)
│   │   └── models.py       # Data models (StatusResponse, AuthResponse, SearchResponse)
│   ├── commands/           # CLI command implementations
│   │   ├── __init__.py
│   │   ├── search_commands.py  # Search command with Click decorators
│   │   └── status_commands.py  # Status/auth commands
│   └── utils.py            # Output formatters and logging
├── tests/
│   ├── __init__.py
│   └── test_utils.py       # Tests for formatters and models
├── pyproject.toml          # Dependencies: click, requests, rich
├── Makefile                # Development commands
├── README.md               # User documentation
└── CLAUDE.md               # This file
```

### Key Design Principles

1. **Separation of Concerns**: Core library (`core/`) is independent of CLI
2. **Exception-Based Errors**: Core raises exceptions (NOT sys.exit), CLI handles formatting/exit codes
3. **Composable Output**: JSON to stdout, logs to stderr for piping
4. **Agent-Friendly**: Structured commands, clear errors with solutions, parseable output for ReAct loops
5. **Type Safety**: Strict mypy, comprehensive type hints
6. **Importable Library**: Public API via `__init__.py` for programmatic use

## Development Commands

### Quick Start

```bash
# Install dependencies
make install

# Run all quality checks
make check

# Format, check, build, and install globally
make pipeline
```

### Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies with `uv sync` |
| `make format` | Auto-format code with ruff |
| `make lint` | Run linting with ruff |
| `make typecheck` | Type check with mypy (strict mode) |
| `make test` | Run pytest test suite |
| `make check` | Run lint + typecheck + test |
| `make pipeline` | Full workflow: format + check + build + install-global |
| `make build` | Build package with `uv build` |
| `make install-global` | Install globally with `uv tool install . --reinstall` |
| `make clean` | Remove build artifacts and cache |

## Code Standards

- **Python Version**: 3.14+
- **Type Hints**: Required for all functions, strict mypy
- **Line Length**: 100 characters
- **Formatting**: ruff (PEP 8 compliant)
- **Docstrings**: Required for all public functions with Args, Returns, Raises sections
- **Module Docstrings**: Acknowledge AI-generated code:
  ```python
  """
  Module description.

  Note: This code was generated with assistance from AI coding tools
  and has been reviewed and tested by a human.
  """
  ```

## CLI Commands

### Command Structure

**Main CLI**: `obsidian-search-tool` (Click group)

**Global Options:**
- `--help / -h` - Show help
- `--version` - Show version (0.1.0)

### Available Commands

#### 1. `status` - Check API Connectivity

```bash
obsidian-search-tool status [--json|--text] [--verbose]
```

**Purpose**: Verify Obsidian Local REST API is reachable
**Output**: JSON (default) or markdown text
**Returns**: Connection status, API URL, timestamp, message

#### 2. `auth` - Validate Authentication

```bash
obsidian-search-tool auth [--json|--text] [--verbose]
```

**Purpose**: Validate API key is correct
**Output**: JSON (default) or markdown text
**Returns**: Authentication status, API URL, timestamp, message

#### 3. `search` - Search Vault

```bash
obsidian-search-tool search [QUERY_TEXT] [--type dataview|jsonlogic] [--stdin] [--json|--text|--table] [--verbose]
```

**Purpose**: Search vault with Dataview DQL (TABLE) or JsonLogic queries
**Query Input**: Positional `QUERY_TEXT` argument or `--stdin` (from stdin, mutually exclusive)
**Query Types**:
- `dataview` (default) - Dataview DQL TABLE queries only
- `jsonlogic` - JSON-based programmatic queries
**Output Formats**:
- `--json` - JSON (default, machine-readable)
- `--text / -t` - Markdown formatted text
- `--table` - Pretty-printed table (best for TABLE results)

**Examples:**

```bash
# Dataview DQL TABLE query
obsidian-search-tool search 'TABLE file.name FROM #project'

# With WHERE and SORT
obsidian-search-tool search 'TABLE file.name, author WHERE author SORT file.mtime DESC'

# JsonLogic query
obsidian-search-tool search --type jsonlogic '{"in": [{"var": "frontmatter.tags"}, "project"]}'

# From stdin
echo 'TABLE file.name FROM #meeting' | obsidian-search-tool search --stdin

# Text output
obsidian-search-tool search 'TABLE file.name' --text

# Table output
obsidian-search-tool search 'TABLE file.name, status' --table
```

## Library Usage

### Public API

Import from `obsidian_search_tool`:

```python
from obsidian_search_tool import (
    # Client
    ObsidianClient,
    # Exceptions
    ObsidianClientError,
    ObsidianAuthError,
    ObsidianConnectionError,
    ObsidianAPIError,
    # Models
    StatusResponse,
    AuthResponse,
    SearchResponse,
)
```

### ObsidianClient

```python
client = ObsidianClient(
    base_url="http://127.0.0.1:27123",  # Optional, default from env
    api_key="your-api-key",              # Optional, default from env
    timeout=30                           # Optional, default from env
)

# Status check
status: StatusResponse = client.status()

# Authentication check
auth: AuthResponse = client.check_auth()

# Dataview DQL search
response: SearchResponse = client.search_dataview('TABLE file.name FROM #project')

# JsonLogic search
response: SearchResponse = client.search_jsonlogic('{"in": [{"var": "frontmatter.tags"}, "aws"]}')
```

### Error Handling

```python
try:
    client = ObsidianClient()  # May raise ObsidianAuthError
    response = client.search_dataview('TABLE file.name')
except ObsidianAuthError as e:
    # Handle authentication errors (401)
    print(f"Auth error: {e}")
except ObsidianConnectionError as e:
    # Handle connection errors (timeout, network)
    print(f"Connection error: {e}")
except ObsidianAPIError as e:
    # Handle API errors (4xx, 5xx)
    print(f"API error [{e.status_code}]: {e.error_code} - {e}")
except ObsidianClientError as e:
    # Handle other client errors
    print(f"Client error: {e}")
```

## Testing

### Run Tests

```bash
# All tests
make test

# With verbose output
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_utils.py

# With coverage
uv run pytest tests/ --cov=obsidian_search_tool
```

### Test Structure

- **tests/test_utils.py**: Tests for formatters, models, and utility functions
- Tests use standard pytest conventions
- Mock external dependencies (requests) where appropriate
- Tests cover: JSON formatting, text formatting, error handling, SearchResponse properties

## Important Notes

### Core Dependencies

- **[Click](https://click.palletsprojects.com/)** - CLI framework with decorators
- **[Requests](https://requests.readthedocs.io/)** - HTTP client for API calls
- **[Rich](https://rich.readthedocs.io/)** - Terminal formatting and tables

### Environment Variables

- `OBSIDIAN_API_KEY` (required) - API token from Obsidian Local REST API plugin settings
- `OBSIDIAN_BASE_URL` (optional, default: http://127.0.0.1:27123) - API base URL
- `OBSIDIAN_TIMEOUT` (optional, default: 30) - Request timeout in seconds
- `OBSIDIAN_VERBOSE` (optional, default: false) - Enable verbose logging

### ObsidianClient Implementation

- **Base URL Resolution**: Strips trailing slash, uses env var or default
- **API Key Validation**: Raises `ObsidianAuthError` if missing
- **Timeout Handling**: Configurable via env var or constructor parameter
- **Error Handling**: Maps HTTP status codes to specific exceptions
- **Request Method**: Uses requests library with Bearer token authentication

### CLI-Specific Behaviors

- **Query Input Validation**: Mutually exclusive positional `QUERY_TEXT` argument and `--stdin`
- **Output Format Selection**: JSON default, text/table override, only one can be active
- **Exit Codes**: 0 for success, 1 for errors
- **Error Output**: JSON format on stdout with error details
- **Verbose Logging**: Logs to stderr, does not interfere with stdout

### Search Operations

- **Dataview DQL**: Only TABLE queries supported by API (LIST/TASK/CALENDAR will error)
- **GROUP BY/FLATTEN Not Supported**: API returns "TABLE WITHOUT ID queries are not supported" error
- **Supported Data Commands**: FROM, WHERE, SORT, LIMIT work correctly
- **JsonLogic Variables**: `filename`, `frontmatter.*`, `content`
- **JsonLogic Operators**: `in` operator works, `startsWith`/`endsWith` not supported by API
- **No Max Results Option**: Removed per user request, returns all results from API
- **Query Validation**: No client-side validation, pass queries directly to API

### Dataview DQL Capabilities

#### Data Commands (Execute in Order)

Commands refine query results and execute in the order they appear.

**Supported by API:**

1. **FROM** - Select source pages (tags, folders, files, links)
   ```dataview
   FROM #tag               # By tag (includes subtags)
   FROM "folder"          # By folder (includes subfolders)
   FROM [[note]]          # Pages linking TO note
   FROM outgoing([[note]]) # Pages linked FROM note
   ```

2. **WHERE** - Filter pages based on conditions
   ```dataview
   WHERE author                                    # Field exists
   WHERE contains(author, "Smith")                 # Contains check
   WHERE file.size > 1000                         # Comparison
   WHERE file.mtime >= date(today) - dur(7 days) # Date-based
   WHERE contains(file.folder, "ai-ml")           # Folder contains
   ```

3. **SORT** - Sort results by one or more fields
   ```dataview
   SORT file.mtime DESC                    # Single field
   SORT file.folder ASC, file.mtime DESC  # Multiple fields
   ```

4. **LIMIT** - Restrict result count (applied after all other commands)
   ```dataview
   SORT file.mtime DESC
   LIMIT 10                       # Top 10 by date
   ```

**Not Supported by API (will error):**

- **GROUP BY** - Returns "TABLE WITHOUT ID queries are not supported"
- **FLATTEN** - Returns "TABLE WITHOUT ID queries are not supported"

#### Implicit Fields (file.*)

All pages have automatic metadata accessible via `file.` prefix:

- **Basic**: `file.name`, `file.path`, `file.folder`, `file.size`, `file.ext`, `file.link`
- **Dates**: `file.ctime`, `file.cday`, `file.mtime`, `file.mday`, `file.day`
- **Links/Tags**: `file.tags`, `file.etags`, `file.inlinks`, `file.outlinks`, `file.aliases`
- **Content**: `file.tasks`, `file.lists`, `file.frontmatter`
- **Other**: `file.starred`

See [references/dataview-metadata-on-pages.md](references/dataview-metadata-on-pages.md) for complete reference.

#### Common Functions

- **Constructors**: `date()`, `dur()`, `list()`, `object()`, `link()`
- **Numeric**: `round()`, `min()`, `max()`, `sum()`, `average()`, `length()`
- **String**: `contains()`, `lower()`, `upper()`, `split()`, `replace()`, `startswith()`, `endswith()`
- **Array**: `filter()`, `map()`, `sort()`, `unique()`, `flat()`, `join()`
- **Logic**: `all()`, `any()`, `none()`, `choice()`, `default()`
- **Date/Time**: `dateformat()`, `striptime()`

See [references/dataview-ql-functions.md](references/dataview-ql-functions.md) for complete function reference.

#### Query Examples

```bash
# Basic query with FROM
obsidian-search-tool search 'TABLE file.name FROM "daily" LIMIT 5'

# Recent notes with date functions
obsidian-search-tool search 'TABLE file.name, file.mtime WHERE file.mtime >= date(today) - dur(7 days) SORT file.mtime DESC'

# Files in specific folder with contains()
obsidian-search-tool search 'TABLE file.name, file.folder WHERE contains(file.folder, "ai-ml") LIMIT 5'

# Complex multi-condition query
obsidian-search-tool search 'TABLE file.name, file.size FROM "reference" WHERE file.size > 5000 SORT file.mtime DESC LIMIT 10'

# JsonLogic content search
obsidian-search-tool search --type jsonlogic '{"in": ["Claude", {"var": "content"}]}'
```

### Version Synchronization

**CRITICAL**: Keep version consistent across three files:
1. `pyproject.toml` - `[project] version = "0.1.0"`
2. `obsidian_search_tool/cli.py` - `@click.version_option(version="0.1.0")`
3. `obsidian_search_tool/__init__.py` - `__version__ = "0.1.0"`

## Testing and Validation

This section documents comprehensive testing performed on 2025-11-14 against a live Obsidian instance with Local REST API plugin.

### Test Environment

- **Obsidian**: Running with Local REST API plugin enabled
- **Vault Size**: 2000+ notes across multiple folders
- **Test Date**: 2025-11-14
- **Tool Version**: 0.1.0

### ✅ Tested and Verified Features

#### Dataview DQL - Data Commands

| Command | Status | Test Query | Results |
|---------|--------|------------|---------|
| FROM | ✅ Works | `TABLE file.name FROM "daily" LIMIT 5` | Retrieved 5 files from daily folder |
| WHERE | ✅ Works | `TABLE file.name WHERE file.size > 1000` | Filtered by file size correctly |
| SORT | ✅ Works | `TABLE file.name SORT file.mtime DESC` | Sorted by modification time |
| LIMIT | ✅ Works | `TABLE file.name LIMIT 10` | Limited to 10 results |
| GROUP BY | ❌ Fails | `TABLE file.name GROUP BY file.folder` | Error: "TABLE WITHOUT ID queries are not supported" |
| FLATTEN | ❌ Fails | `TABLE file.name FLATTEN authors` | Error: "TABLE WITHOUT ID queries are not supported" |

#### Dataview DQL - Functions

| Function | Status | Test Query | Results |
|----------|--------|------------|---------|
| date() | ✅ Works | `WHERE file.mtime >= date(today)` | Date parsing works |
| dur() | ✅ Works | `WHERE file.mtime >= date(today) - dur(7 days)` | Found 188 files modified in last 7 days |
| contains() | ✅ Works | `WHERE contains(file.folder, "ai-ml")` | Found 5 files in ai-ml folders |
| Comparison operators | ✅ Works | `WHERE file.size > 5000` | Filtered 10 large files |
| Date arithmetic | ✅ Works | `date(today) - dur(7 days)` | Calculated date correctly |

#### Dataview DQL - Implicit Fields

| Field Category | Status | Test Query | Results |
|----------------|--------|------------|---------|
| Basic fields | ✅ Works | `TABLE file.name, file.size, file.folder` | All basic fields returned |
| Date fields | ✅ Works | `TABLE file.mtime, file.ctime` | Timestamps returned correctly |
| Tags fields | ✅ Works | `TABLE file.tags` | Tag arrays returned |
| Size field | ✅ Works | `WHERE file.size > 10000` | Size filtering works |

#### JsonLogic Queries

| Operator | Status | Test Query | Results |
|----------|--------|------------|---------|
| in (content) | ✅ Works | `{"in": ["Claude", {"var": "content"}]}` | Found 77 files containing "Claude" |
| in (filename) | ✅ Works | `{"in": ["daily", {"var": "filename"}]}` | Substring matching works |
| in (tags) | ✅ Works | `{"in": [{"var": "frontmatter.tags"}, "project"]}` | Tag search works |
| startsWith | ❌ Fails | `{"startsWith": [{"var": "filename"}, "daily/"]}` | Error: "Unrecognized operation startsWith" |
| endsWith | ❌ Not tested | - | Expected to fail like startsWith |

#### Output Formats

| Format | Status | Test Command | Results |
|--------|--------|--------------|---------|
| JSON | ✅ Works | `search 'TABLE file.name' --json` | Valid JSON output |
| Text | ✅ Works | `search 'TABLE file.name' --text` | Markdown formatted output |
| Table | ✅ Works | `search 'TABLE file.name' --table` | Rich table output |

#### Input Methods

| Method | Status | Test Command | Results |
|--------|--------|--------------|---------|
| Positional argument | ✅ Works | `search 'TABLE file.name'` | Query accepted |
| Stdin | ✅ Works | `echo 'TABLE file.name' \| search --stdin` | Query read from stdin |

### ❌ Known API Limitations

#### Critical Limitations

1. **GROUP BY Not Supported**
   - Error: "TABLE WITHOUT ID queries are not supported"
   - Impact: Cannot group results by any field
   - No field swizzling (`rows.*`) available
   - Workaround: Use WHERE with contains() to filter by folder

2. **FLATTEN Not Supported**
   - Error: "TABLE WITHOUT ID queries are not supported"
   - Impact: Cannot expand array fields
   - Workaround: None available

3. **JsonLogic startsWith/endsWith Not Supported**
   - Error: "Unrecognized operation startsWith"
   - Impact: Cannot do prefix/suffix matching
   - Workaround: Use `in` operator for substring matching

4. **Only TABLE Queries Supported**
   - LIST, TASK, CALENDAR queries return errors
   - Impact: Limited to tabular output only
   - Workaround: None, TABLE queries only

### 💡 Recommended Patterns

Based on testing, these patterns work reliably:

```bash
# Date-based filtering (works well)
obsidian-search-tool search \
    'TABLE file.name, file.mtime WHERE file.mtime >= date(today) - dur(7 days) SORT file.mtime DESC'

# Folder filtering (use contains, not GROUP BY)
obsidian-search-tool search \
    'TABLE file.name, file.folder WHERE contains(file.folder, "reference") LIMIT 10'

# Size filtering with sorting
obsidian-search-tool search \
    'TABLE file.name, file.size WHERE file.size > 5000 SORT file.size DESC'

# Complex multi-condition queries
obsidian-search-tool search \
    'TABLE file.name FROM "docs" WHERE file.size > 1000 AND file.mtime >= date(today) - dur(30 days) SORT file.mtime DESC LIMIT 20'

# JsonLogic content search (most reliable)
obsidian-search-tool search --type jsonlogic \
    '{"in": ["keyword", {"var": "content"}]}'
```

### 🔧 Testing Methodology

Testing was performed using:
1. `obsidian-search-tool status` - Verified API connectivity
2. Live queries against 2000+ note vault
3. All examples from documentation tested
4. Error cases deliberately triggered
5. All output formats tested
6. Stdin input tested

All successful tests confirmed with actual result counts and data inspection.

## Resources

### Official Documentation

- [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) - Plugin documentation
- [Dataview Plugin](https://github.com/blacksmithgu/obsidian-dataview) - Query language reference
- [JsonLogic](https://jsonlogic.com/) - JSON logic format specification

### Related Tools

- [Python Obsidian REST SDK](https://github.com/coddingtonbear/python-obsidian-rest) - Official Python client

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes following code standards
4. Run `make check` to verify quality
5. Run `make pipeline` to build and test
6. Commit changes with descriptive message
7. Push and open Pull Request

### Commit Message Format

Follow conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Build/tooling changes

---

**Note**: This code was developed with assistance from Claude Code and has been reviewed and tested by a human.
