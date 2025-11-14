# Dataview Query Types Reference

This document explains the four Dataview Query Language (DQL) query types available in the Dataview plugin.

## Important Note

**The Obsidian Local REST API only supports TABLE queries.** The obsidian-search-tool CLI can only use TABLE query type. LIST, TASK, and CALENDAR queries are documented here for reference but cannot be used with this tool.

## Overview

The Query Type determines the output format of a Dataview query and is the only mandatory specification. The four available types are:

1. **TABLE** - Tabular views with columns (✅ supported by this tool)
2. **LIST** - Bullet point lists (❌ not supported via API)
3. **TASK** - Interactive task lists (❌ not supported via API)
4. **CALENDAR** - Calendar views (❌ not supported via API)

Query types also determine the information level:
- **LIST, TABLE, CALENDAR** operate at page level
- **TASK** queries operate at the file.tasks level

All query types can be combined with data commands (FROM, WHERE, SORT, GROUP BY, LIMIT) to refine results.

---

## TABLE Query Type ✅

**Status**: Supported by obsidian-search-tool

TABLE queries render a tabular view of metadata values or calculations. You can specify any number of columns and optional custom headers.

### Basic Syntax

```dataview
TABLE
```

Outputs all files in your vault with default "File" column.

### Specifying Columns

```dataview
TABLE file.name, file.mtime, file.folder
FROM "reference"
```

### Custom Column Headers

Use the `AS` syntax to specify custom headers:

```dataview
TABLE
  file.name AS "Note",
  file.mtime AS "Modified",
  file.folder AS "Location"
FROM #project
```

**Note**: Headers with spaces must be wrapped in double quotes.

### Calculations and Expressions

Columns can contain calculations:

```dataview
TABLE
  file.name,
  file.size / 1000 AS "Size (KB)",
  date(today) - file.ctime AS "Age"
FROM "work"
```

### TABLE WITHOUT ID

Removes the first column (file name or group name):

```dataview
TABLE WITHOUT ID
  file.link AS "Document",
  file.mtime AS "Last Modified"
FROM #meeting
```

This is useful for:
- Renaming the first column for a specific query
- Displaying a different identifying value
- Creating custom table layouts

### Grouping

Grouped tables show group keys in the first column:

```dataview
TABLE file.name, file.mtime
FROM #project
GROUP BY file.folder
```

### Common Patterns

```dataview
# Recent notes
TABLE file.mtime AS "Modified"
SORT file.mtime DESC
LIMIT 10

# Notes by folder
TABLE file.name, file.ctime
GROUP BY file.folder

# Notes with custom fields
TABLE author, status, priority
WHERE author
SORT priority DESC

# Filtered and sorted
TABLE file.name, file.size
FROM "reference"
WHERE file.size > 1000
SORT file.size DESC
LIMIT 20
```

### Available with obsidian-search-tool

```bash
# Basic TABLE query
obsidian-search-tool search 'TABLE file.name FROM #project'

# With multiple columns
obsidian-search-tool search 'TABLE file.name, file.mtime, file.folder FROM "study"'

# With sorting
obsidian-search-tool search 'TABLE file.name SORT file.mtime DESC LIMIT 10'

# With grouping
obsidian-search-tool search 'TABLE file.name GROUP BY file.folder' --table
```

---

## LIST Query Type ❌

**Status**: Not supported by Obsidian Local REST API

LIST queries output bullet point lists of file links. You can specify one additional piece of information to display.

### Basic Syntax

```dataview
LIST
```

### With Additional Information

```dataview
LIST file.folder
FROM #games
```

### Computed Values

```dataview
LIST "Path: " + file.folder + " (created: " + file.cday + ")"
FROM "Games"
```

### LIST WITHOUT ID

Removes the file link from output:

```dataview
LIST WITHOUT ID type
```

### Grouping

```dataview
LIST rows.file.link
GROUP BY type
```

---

## TASK Query Type ❌

**Status**: Not supported by Obsidian Local REST API

TASK queries render interactive task lists. They operate at task level rather than page level, allowing task-specific filtering.

### Basic Syntax

```dataview
TASK
```

### Filtering Tasks

```dataview
TASK
WHERE !completed AND contains(tags, "#shopping")
```

### Grouping by File

```dataview
TASK
WHERE !completed
GROUP BY file.link
```

### Child Tasks

Child tasks (indented tasks) belong to their parent and are included if the parent matches the query, even if the child doesn't match.

---

## CALENDAR Query Type ❌

**Status**: Not supported by Obsidian Local REST API

CALENDAR queries render a monthly calendar view where each result is represented as a dot on a date. Requires a date field.

### Basic Syntax

```dataview
CALENDAR file.ctime
```

### With Filtering

```dataview
CALENDAR due
WHERE typeof(due) = "date"
```

**Note**: SORT and GROUP BY have no effect on CALENDAR queries.

---

## See Also

- [Dataview Data Commands](dataview-ql-data-commands.md) - FROM, WHERE, SORT, GROUP BY, LIMIT
- [Dataview Functions](dataview-ql-functions.md) - Available functions for expressions
- [Dataview Page Metadata](dataview-metadata-on-pages.md) - Available file.* fields
- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/) - Complete official reference
