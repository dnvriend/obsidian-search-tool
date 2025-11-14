# Dataview Data Commands Reference

Data commands refine and manipulate query results in Dataview Query Language (DQL). Commands are executed in order and can be used multiple times in a single query.

## Command Execution Order

Commands execute in the order they appear:
1. FROM - Select source pages
2. WHERE - Filter pages
3. SORT - Sort results
4. GROUP BY - Group results
5. FLATTEN - Expand arrays
6. LIMIT - Restrict result count

You can use multiple instances of the same command (e.g., multiple WHERE blocks).

---

## FROM

Determines which pages are initially collected for the query.

### Syntax

```dataview
FROM <source>
```

### Source Types

**By Tag** (includes subtags):
```dataview
FROM #tag
```

**By Folder** (includes subfolders):
```dataview
FROM "folder"
FROM "path/to/folder"
```

**By Single File**:
```dataview
FROM "path/to/file.md"
```

**By Links**:
```dataview
FROM [[note]]              # Pages linking TO [[note]]
FROM outgoing([[note]])    # Pages linked FROM [[note]]
```

### Combining Sources

Use `and` and `or` to compose filters:

```dataview
# Pages in folder AND with tag
FROM #tag and "folder"

# Pages linking to either note
FROM [[Food]] or [[Exercise]]

# Pages with tag but NOT in folder (negation with -)
FROM #tag and -"folder"

# Complex combinations
FROM (#project or #work) and -"archive"
```

### Examples with obsidian-search-tool

```bash
# From tag
obsidian-search-tool search 'TABLE file.name FROM #project'

# From folder
obsidian-search-tool search 'TABLE file.name FROM "reference/ai-ml"'

# Combined sources
obsidian-search-tool search 'TABLE file.name FROM #study and "reference"'
```

---

## WHERE

Filters pages based on field conditions. Only pages where the clause evaluates to true are included.

### Syntax

```dataview
WHERE <condition>
```

### Examples

**Modified recently**:
```dataview
TABLE file.name
WHERE file.mtime >= date(today) - dur(1 day)
```

**Multiple conditions**:
```dataview
TABLE file.name
FROM #projects
WHERE !completed AND file.ctime <= date(today) - dur(1 month)
```

**Field existence**:
```dataview
TABLE file.name, author
WHERE author
```

**Contains check**:
```dataview
TABLE file.name, author
WHERE contains(author, "Smith")
```

**Comparison**:
```dataview
TABLE file.name, file.size
WHERE file.size > 1000
```

### Examples with obsidian-search-tool

```bash
# Filter by field existence
obsidian-search-tool search 'TABLE file.name, author WHERE author'

# Filter by date
obsidian-search-tool search 'TABLE file.name WHERE file.mtime >= date(today) - dur(7 days)'

# Filter by size
obsidian-search-tool search 'TABLE file.name, file.size WHERE file.size > 5000'

# Multiple conditions
obsidian-search-tool search 'TABLE file.name FROM #project WHERE !completed'
```

---

## SORT

Sorts results by one or more fields.

### Syntax

```dataview
SORT field [ASCENDING/DESCENDING/ASC/DESC]
```

Default is ASCENDING if not specified.

### Multiple Sort Fields

```dataview
SORT field1 [ASC/DESC], field2 [ASC/DESC], field3 [ASC/DESC]
```

Ties are resolved by subsequent sort fields.

### Examples

**Single field**:
```dataview
TABLE file.name, file.mtime
SORT file.mtime DESC
```

**Multiple fields**:
```dataview
TABLE file.name, file.folder, file.mtime
SORT file.folder ASC, file.mtime DESC
```

### Examples with obsidian-search-tool

```bash
# Sort by modification time (descending)
obsidian-search-tool search 'TABLE file.name, file.mtime SORT file.mtime DESC'

# Sort by multiple fields
obsidian-search-tool search 'TABLE file.name, file.folder SORT file.folder ASC, file.name ASC'

# Recent files
obsidian-search-tool search 'TABLE file.name SORT file.mtime DESC LIMIT 10' --table
```

---

## GROUP BY

Groups results by a field value. Yields one row per unique field value with:
- The grouped field
- A `rows` array containing all matching pages

### Syntax

```dataview
GROUP BY field
GROUP BY (computed_field) AS name
```

### Field Swizzling

Access fields from grouped rows using dot notation:
- `rows.file.name` - Gets `file.name` from each row
- `rows.author` - Gets `author` from each row

### Examples

**Group by folder**:
```dataview
TABLE rows.file.name
GROUP BY file.folder
```

**Group with aggregation**:
```dataview
TABLE length(rows) AS "Count"
GROUP BY file.folder
```

**Group by computed field**:
```dataview
TABLE rows.file.link
GROUP BY date(file.ctime).year AS "Year"
```

### Examples with obsidian-search-tool

```bash
# Group by folder
obsidian-search-tool search 'TABLE file.name GROUP BY file.folder'

# Group with row count
obsidian-search-tool search 'TABLE length(rows) AS "Count" GROUP BY file.folder' --table

# Group by custom field
obsidian-search-tool search 'TABLE rows.file.link FROM #project GROUP BY status'
```

---

## FLATTEN

Expands array fields, yielding one row per array element.

### Syntax

```dataview
FLATTEN field
FLATTEN (computed_field) AS name
```

### Examples

**Flatten authors**:
```dataview
TABLE authors
FROM #literature
FLATTEN authors
```

**Flatten tasks**:
```dataview
TABLE T.text AS "Task"
FLATTEN file.tasks AS T
WHERE T.text
```

### Use Cases

- Operating on nested lists (file.tasks, file.lists)
- Expanding multi-value fields
- Simplifying array operations

**Before FLATTEN**:
```
File: Note.md | authors: [Smith, Jones]
```

**After FLATTEN authors**:
```
File: Note.md | authors: Smith
File: Note.md | authors: Jones
```

---

## LIMIT

Restricts results to at most N values.

### Syntax

```dataview
LIMIT N
```

### Important Note

LIMIT is applied **after** all preceding commands. Order matters:

```dataview
# Sorts AFTER limiting (first 5, then sorted)
LIMIT 5
SORT file.mtime DESC

# Limits AFTER sorting (top 5 by date)
SORT file.mtime DESC
LIMIT 5
```

### Examples

**Recent files**:
```dataview
TABLE file.mtime
SORT file.mtime DESC
LIMIT 10
```

**Top results**:
```dataview
TABLE file.size
WHERE file.size > 1000
SORT file.size DESC
LIMIT 20
```

### Examples with obsidian-search-tool

```bash
# Top 10 recent notes
obsidian-search-tool search 'TABLE file.name SORT file.mtime DESC LIMIT 10'

# First 5 from folder
obsidian-search-tool search 'TABLE file.name FROM "study" LIMIT 5'

# Largest files
obsidian-search-tool search 'TABLE file.name, file.size SORT file.size DESC LIMIT 20' --table
```

---

## Combining Commands

Commands can be combined to create powerful queries:

```dataview
# Complex query with all commands
TABLE file.name, file.mtime, file.size
FROM #project and -"archive"
WHERE file.size > 1000 AND file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 10
```

### Real-World Examples

**Recent work notes**:
```bash
obsidian-search-tool search 'TABLE file.name, file.mtime FROM "work" SORT file.mtime DESC LIMIT 10'
```

**Large reference files**:
```bash
obsidian-search-tool search 'TABLE file.name, file.size FROM "reference" WHERE file.size > 10000 SORT file.size DESC'
```

**Grouped by folder**:
```bash
obsidian-search-tool search 'TABLE file.name, file.mtime FROM #study GROUP BY file.folder' --table
```

---

## See Also

- [Dataview Query Types](dataview-ql-query-types.md) - TABLE, LIST, TASK, CALENDAR
- [Dataview Functions](dataview-ql-functions.md) - Available functions for expressions
- [Dataview Page Metadata](dataview-metadata-on-pages.md) - Available file.* fields
- [Dataview Documentation](https://blacksmithgu.github.io/obsidian-dataview/) - Complete official reference
