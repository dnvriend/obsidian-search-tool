# Dataview Page Metadata Reference

This document describes all implicit fields automatically available on every page in Dataview queries.

## Overview

Dataview automatically adds metadata to each page through implicit fields. These fields are available under the `file.` prefix and provide information about the file itself (name, path, dates, links, etc.).

In addition to implicit fields, you can add custom fields via:
- **Frontmatter** - YAML metadata at the top of the file
- **Inline fields** - Using `::` syntax within the content

---

## Implicit Fields

All implicit fields are accessed with the `file.` prefix (e.g., `file.name`, `file.mtime`).

### Basic File Information

| Field | Data Type | Description |
|-------|-----------|-------------|
| `file.name` | Text | File name without extension (as shown in Obsidian sidebar) |
| `file.folder` | Text | Path of the folder containing this file |
| `file.path` | Text | Full file path including the file name |
| `file.ext` | Text | File extension (usually `md`) |
| `file.link` | Link | Link object to the file |
| `file.size` | Number | File size in bytes |

### Date Fields

| Field | Data Type | Description |
|-------|-----------|-------------|
| `file.ctime` | Date with Time | Date and time the file was created |
| `file.cday` | Date | Date the file was created (without time) |
| `file.mtime` | Date with Time | Date and time the file was last modified |
| `file.mday` | Date | Date the file was last modified (without time) |
| `file.day` | Date | Date parsed from filename (format: `yyyy-mm-dd` or `yyyymmdd`) or from Date field |

### Link and Tag Fields

| Field | Data Type | Description |
|-------|-----------|-------------|
| `file.tags` | List | All unique tags with subtags broken down (e.g., `#Tag/1/A` → `[#Tag, #Tag/1, #Tag/1/A]`) |
| `file.etags` | List | Explicit tags without breaking down subtags (e.g., `[#Tag/1/A]`) |
| `file.inlinks` | List | Incoming links (files that link TO this file) |
| `file.outlinks` | List | Outgoing links (links contained IN this file) |
| `file.aliases` | List | All aliases defined in frontmatter |

### Content Fields

| Field | Data Type | Description |
|-------|-----------|-------------|
| `file.tasks` | List | All tasks in the file (format: `- [ ] task text`) |
| `file.lists` | List | All list elements including tasks |
| `file.frontmatter` | List | Raw frontmatter as key-value pairs |

### Other Fields

| Field | Data Type | Description |
|-------|-----------|-------------|
| `file.starred` | Boolean | Whether file is bookmarked (via Obsidian Bookmarks plugin) |

---

## Usage Examples

### Basic File Queries

**List recent files:**
```dataview
TABLE file.name, file.mtime
SORT file.mtime DESC
LIMIT 10
```

**Files by folder:**
```dataview
TABLE file.name, file.size
FROM "reference"
WHERE file.size > 1000
```

**Files with specific extension:**
```dataview
TABLE file.name, file.ext
WHERE file.ext = "md"
```

### Date-Based Queries

**Files created this week:**
```dataview
TABLE file.name, file.ctime
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
```

**Files modified today:**
```dataview
TABLE file.name, file.mtime
WHERE file.mday = date(today)
```

**Files with date in filename:**
```dataview
TABLE file.name, file.day
WHERE file.day
SORT file.day DESC
```

### Tag and Link Queries

**Files with specific tag:**
```dataview
TABLE file.name, file.tags
WHERE contains(file.tags, "#project")
```

**Files linking to a note:**
```dataview
TABLE file.name, file.folder
FROM [[Reference Note]]
```

**Files with outgoing links:**
```dataview
TABLE file.name, length(file.outlinks) AS "Links"
WHERE file.outlinks
SORT length(file.outlinks) DESC
```

### Size-Based Queries

**Largest files:**
```dataview
TABLE file.name, file.size
SORT file.size DESC
LIMIT 20
```

**Files by size category:**
```dataview
TABLE file.name, file.size / 1000 AS "Size (KB)"
WHERE file.size > 10000
GROUP BY file.folder
```

### Combined Queries

**Recent large files:**
```dataview
TABLE file.name, file.size, file.mtime
WHERE file.size > 5000 AND file.mtime >= date(today) - dur(30 days)
SORT file.mtime DESC
```

**Tagged files by folder:**
```dataview
TABLE file.name, file.tags
FROM #project
GROUP BY file.folder
```

---

## Using with obsidian-search-tool

All implicit fields work with the CLI tool:

```bash
# Recent files
obsidian-search-tool search 'TABLE file.name, file.mtime SORT file.mtime DESC LIMIT 10'

# Files in folder
obsidian-search-tool search 'TABLE file.name, file.folder FROM "reference"'

# Large files
obsidian-search-tool search 'TABLE file.name, file.size WHERE file.size > 10000' --table

# Files with tags
obsidian-search-tool search 'TABLE file.name, file.tags WHERE contains(file.tags, "#study")'

# Files by modification date
obsidian-search-tool search 'TABLE file.name WHERE file.mday >= date(today) - dur(7 days)'
```

---

## Example Page

A markdown page with both user-defined fields and implicit fields:

```markdown
---
genre: "action"
reviewed: false
---
# Movie X
#movies

**Thoughts**:: It was decent.
**Rating**:: 6

[mood:: okay] | [length:: 2 hours]
```

**Available fields:**
- User-defined: `genre`, `reviewed`, `Thoughts`, `Rating`, `mood`, `length`
- Implicit: All `file.*` fields listed above
- Tags: `#movies`

**Example query:**
```dataview
TABLE file.ctime, length, Rating, reviewed
FROM #movies
```

---

## See Also

- [Dataview Query Types](dataview-ql-query-types.md) - TABLE, LIST, TASK, CALENDAR
- [Dataview Data Commands](dataview-ql-data-commands.md) - FROM, WHERE, SORT, GROUP BY, LIMIT
- [Dataview Functions](dataview-ql-functions.md) - Available functions for expressions
- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/) - Complete official reference
