# JsonLogic Search Examples

This document contains effective JsonLogic search patterns for the Obsidian Search Tool.

## Overview

JsonLogic queries use JSON format to search vault files programmatically. The Obsidian Local REST API processes these queries and returns matching files.

## Available Variables

The JsonLogic context provides access to:
- `filename` - File path relative to vault root
- `frontmatter.*` - YAML frontmatter fields (e.g., `frontmatter.tags`, `frontmatter.type`)
- `content` - Full file content for text search

## Tag Search Patterns

### Single Tag Search
```json
{"in": [{"var": "frontmatter.tags"}, "project"]}
```
Returns files that have the "project" tag.

### Multiple Tags (AND)
```json
{
  "and": [
    {"in": [{"var": "frontmatter.tags"}, "project"]},
    {"in": [{"var": "frontmatter.tags"}, "aws"]}
  ]
}
```
Returns files that have BOTH "project" AND "aws" tags.

### Multiple Tags (OR)
```json
{
  "or": [
    {"in": [{"var": "frontmatter.tags"}, "project"]},
    {"in": [{"var": "frontmatter.tags"}, "aws"]}
  ]
}
```
Returns files that have EITHER "project" OR "aws" tags.

### Exclude Tag (NOT)
```json
{
  "not": {"in": [{"var": "frontmatter.tags"}, "project"]}
}
```
Returns files that do NOT have the "project" tag.

## Frontmatter Field Search

### Files With Any Tags
```json
{"exists": {"var": "frontmatter.tags"}}
```
Returns files that have a tags field in frontmatter.

### Files With Specific Frontmatter Field
```json
{"exists": {"var": "frontmatter.type"}}
```
Returns files that have a "type" field in their frontmatter.

## File Name Patterns

### Files by Path Prefix
```json
{"startsWith": [{"var": "filename"}, "daily/"]}
```
Returns files in the "daily/" folder.

### Files by Extension
```json
{"endsWith": [{"var": "filename"}, ".md"]}
```
Returns Markdown files.

## Content Search

### Files Containing Text
```json
{"in": ["search term", {"var": "content"}]}
```
Returns files containing "search term" in their content.

## Complex Examples

### Project Files from 2024
```json
{
  "and": [
    {"in": [{"var": "frontmatter.tags"}, "project"]},
    {"contains": [{"var": "filename"}, "2024"]}
  ]
}
```

### AWS Study Materials
```json
{
  "and": [
    {"in": [{"var": "frontmatter.tags"}, "aws"]},
    {"in": [{"var": "frontmatter.tags"}, "study"]}
  ]
}
```

### Daily Notes with Specific Tags
```json
{
  "and": [
    {"startsWith": [{"var": "filename"}, "daily/"]},
    {"in": [{"var": "frontmatter.tags"}, "meeting"]}
  ]
}
```

## Usage with obsidian-search-tool

```bash
# Set environment variable
export OBSIDIAN_API_KEY="your-api-key"

# Search for project files
obsidian-search-tool search --type jsonlogic '{"in": [{"var": "frontmatter.tags"}, "project"]}'

# Search for files with multiple tags
obsidian-search-tool search --type jsonlogic '{
  "and": [
    {"in": [{"var": "frontmatter.tags"}, "project"]},
    {"in": [{"var": "frontmatter.tags"}, "aws"]}
  ]
}'

# Search with table output
obsidian-search-tool search --type jsonlogic '{"in": ["AWS", {"var": "content"}]}' --table

# Search from stdin
echo '{"startsWith": [{"var": "filename"}, "daily/"]}' | \
  obsidian-search-tool search --type jsonlogic --stdin
```

## Response Format

The tool returns results in JSON format:

```json
{
  "success": true,
  "data": {
    "query": "{\"in\": [{\"var\": \"frontmatter.tags\"}, \"project\"]}",
    "search_type": "jsonlogic",
    "timestamp": "2025-11-14T17:00:00.000000+00:00",
    "results": [
      {
        "filename": "path/to/file.md",
        "result": true
      }
    ]
  }
}
```

## Notes

- All tag searches are case-sensitive
- Tags must match exactly (no partial matching)
- The `in` operator checks if an element exists in an array
- Frontmatter fields must exist in the YAML frontmatter to be searchable
- JsonLogic provides many operators that can be combined for complex queries
- For more operators, see [JsonLogic specification](https://jsonlogic.com/)

## See Also

- [JsonLogic Official Documentation](https://jsonlogic.com/)
- [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)