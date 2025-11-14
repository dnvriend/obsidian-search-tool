# Reference Documentation

Curated reference documentation for Obsidian Search Tool.

## Contents

### JsonLogic Search Examples
**File**: [jsonlogic-search-examples.md](jsonlogic-search-examples.md)

Comprehensive JsonLogic query patterns including:
- Tag searches (single, multiple, AND/OR, negation)
- Frontmatter field searches
- File name patterns (startsWith, endsWith)
- Content searches
- Complex combined queries

### Dataview Query Types
**File**: [dataview-ql-query-types.md](dataview-ql-query-types.md)

Reference for all Dataview query types:
- **TABLE** - Tabular views with columns (✅ supported by this tool)
- **LIST** - Bullet point lists (❌ not supported via API)
- **TASK** - Interactive task lists (❌ not supported via API)
- **CALENDAR** - Calendar views (❌ not supported via API)

### Dataview Data Commands
**File**: [dataview-ql-data-commands.md](dataview-ql-data-commands.md)

Reference for data commands in DQL queries:
- **FROM** - Source selection (tags, folders, files, links)
- **WHERE** - Filtering results
- **SORT** - Sorting results
- **GROUP BY** - Grouping results
- **LIMIT** - Restricting result count
- **FLATTEN** - Expanding arrays

### Dataview Functions
**File**: [dataview-ql-functions.md](dataview-ql-functions.md)

Complete function reference organized by category:
- **Constructors** - `object()`, `list()`, `date()`, `dur()`, `number()`, `string()`, `link()`, `typeof()`
- **Numeric Operations** - `round()`, `min()`, `max()`, `sum()`, `average()`, `product()`
- **String Operations** - `replace()`, `split()`, `substring()`, `regextest()`, `contains()`
- **Array/Object Operations** - `filter()`, `map()`, `sort()`, `unique()`, `flatten()`
- **Utility Functions** - `default()`, `choice()`, `dateformat()`, `meta()`

### Dataview Page Metadata
**File**: [dataview-metadata-on-pages.md](dataview-metadata-on-pages.md)

Documentation of implicit fields available on every page:
- **File Info** - `file.name`, `file.path`, `file.folder`, `file.size`, `file.ext`
- **Dates** - `file.ctime`, `file.cday`, `file.mtime`, `file.mday`, `file.day`
- **Links** - `file.inlinks`, `file.outlinks`
- **Tags** - `file.tags`, `file.etags`
- **Content** - `file.tasks`, `file.lists`, `file.frontmatter`
- **Other** - `file.aliases`, `file.starred`

---

## Usage

These files are intended as offline reference material. Consult them when:
- Building complex Dataview DQL TABLE queries
- Understanding available functions and operators
- Learning what metadata fields are available
- Creating JsonLogic queries for programmatic searches

---

## Quick Examples

### Dataview DQL Queries

```bash
# Recent files
obsidian-search-tool search 'TABLE file.name, file.mtime SORT file.mtime DESC LIMIT 10'

# Files in folder
obsidian-search-tool search 'TABLE file.name FROM "reference"'

# With filtering
obsidian-search-tool search 'TABLE file.name WHERE file.size > 10000'

# Grouped results
obsidian-search-tool search 'TABLE file.name GROUP BY file.folder' --table
```

### JsonLogic Queries

```bash
# By tag
obsidian-search-tool search --type jsonlogic '{"in": [{"var": "frontmatter.tags"}, "project"]}'

# By path
obsidian-search-tool search --type jsonlogic '{"startsWith": [{"var": "filename"}, "daily/"]}'

# By content
obsidian-search-tool search --type jsonlogic '{"in": ["AWS", {"var": "content"}]}'
```

---

## Official Documentation

For the most up-to-date information, always consult:
- [Dataview Plugin Documentation](https://blacksmithgu.github.io/obsidian-dataview/)
- [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [JsonLogic Specification](https://jsonlogic.com/)

---

## Note

This documentation was curated during development of Obsidian Search Tool. Files focus on features relevant to TABLE queries and JsonLogic searches supported by the Obsidian Local REST API.
