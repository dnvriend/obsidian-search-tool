"""Search command implementation for Obsidian Search Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from obsidian_search_tool.core.client import (
    ObsidianAPIError,
    ObsidianAuthError,
    ObsidianClient,
    ObsidianClientError,
    ObsidianConnectionError,
)
from obsidian_search_tool.utils import (
    format_error_json,
    format_search_json,
    format_search_table,
    format_search_text,
    setup_logging,
)


@click.command()
@click.argument("query_text", type=str, required=False, default=None)
@click.option(
    "--type",
    "query_type",
    type=click.Choice(["dataview", "jsonlogic"], case_sensitive=False),
    default="dataview",
    help="Query type: dataview (DQL TABLE) or jsonlogic (JSON format). Default: dataview",
)
@click.option(
    "--stdin",
    "-s",
    "use_stdin",
    is_flag=True,
    help="Read query from stdin (mutually exclusive with positional query)",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=True,
    help="Output as JSON (default)",
)
@click.option(
    "--text",
    "-t",
    "output_text",
    is_flag=True,
    help="Output as markdown-formatted text",
)
@click.option(
    "--table",
    "output_table",
    is_flag=True,
    help="Output as pretty-printed table",
)
@click.option(
    "--verbose",
    "-V",
    "verbose",
    is_flag=True,
    help="Enable verbose logging",
)
def search(
    query_text: str | None,
    query_type: str,
    use_stdin: bool,
    output_json: bool,
    output_text: bool,
    output_table: bool,
    verbose: bool,
) -> None:
    """Search Obsidian vault using Dataview DQL or JsonLogic queries.

    Search operations allow you to query your Obsidian vault using either
    Dataview Query Language (DQL) for structured TABLE queries, or JsonLogic
    for programmatic JSON-based queries.

    \b
    QUERY INPUT:
    Provide query using one of these methods (choose one):
    - Positional argument: Query as first argument
    - --stdin: Read query from stdin (for piping)

    \b
    OUTPUT FORMATS:
    - --json: JSON output (default, machine-readable)
    - --text / -t: Markdown-formatted text output
    - --table: Pretty-printed table output (best for TABLE results)

    \b
    DATAVIEW DQL EXAMPLES:
        # Basic query with FROM
        obsidian-search-tool search 'TABLE file.name FROM "daily" LIMIT 5'

        # Recent notes (date functions)
        obsidian-search-tool search \\
            'TABLE file.name WHERE file.mtime >= date(today) - dur(7 days)'

        # With contains() function
        obsidian-search-tool search \\
            'TABLE file.name, file.folder WHERE contains(file.folder, "ai-ml")'

        # Large files sorted
        obsidian-search-tool search 'TABLE file.name WHERE file.size > 10000 SORT file.size DESC'

        # Complex multi-condition
        obsidian-search-tool search \\
            'TABLE file.name FROM "docs" WHERE file.size > 5000 SORT file.mtime DESC LIMIT 10'

        # From stdin
        echo 'TABLE file.name' | obsidian-search-tool search --stdin

    \b
    JSONLOGIC EXAMPLES:
        # Content search
        obsidian-search-tool search --type jsonlogic \\
            '{"in": ["Claude", {"var": "content"}]}'

        # Path contains string
        obsidian-search-tool search --type jsonlogic \\
            '{"in": ["daily", {"var": "filename"}]}'

        # By tag
        obsidian-search-tool search --type jsonlogic \\
            '{"in": [{"var": "frontmatter.tags"}, "aws"]}'

    \b
    OUTPUT FORMATS:
        # JSON output (default)
        obsidian-search-tool search 'TABLE file.name'

        # Markdown text output
        obsidian-search-tool search 'TABLE file.name' --text

        # Pretty table output
        obsidian-search-tool search 'TABLE file.name, author' --table

    \b
    ENVIRONMENT VARIABLES:
        OBSIDIAN_API_KEY - API token (required, from plugin settings)
        OBSIDIAN_BASE_URL - API URL (default: http://127.0.0.1:27123)
        OBSIDIAN_TIMEOUT - Request timeout in seconds (default: 30)
        OBSIDIAN_VERBOSE - Enable verbose logging (true/false)

    \b
    COMMON ERRORS:
        "OBSIDIAN_API_KEY environment variable is required"
        → Set OBSIDIAN_API_KEY from Local REST API plugin settings

        "Connection failed"
        → Ensure Obsidian is running and Local REST API plugin is enabled

        "Only TABLE dataview queries are supported"
        → Use TABLE instead of LIST, TASK, or CALENDAR

        "TABLE WITHOUT ID queries are not supported"
        → GROUP BY and FLATTEN are not supported by the API

        No results for multi-value fields
        → Use contains(): TABLE file.name WHERE contains(author, "Ben")
    """
    # Setup logging
    setup_logging(verbose)

    # Validate query input
    if query_text and use_stdin:
        click.echo(
            format_error_json(
                "Provide query from only one source: positional argument or --stdin",
                "INPUT_ERROR",
                400,
            )
        )
        sys.exit(1)

    if not query_text and not use_stdin:
        click.echo(
            format_error_json(
                "Query is required. Provide as positional argument or via --stdin. "
                "Use 'obsidian-search-tool search --help' for examples.",
                "INPUT_ERROR",
                400,
            )
        )
        sys.exit(1)

    # Read query from stdin if needed
    query = query_text
    if use_stdin:
        query = sys.stdin.read().strip()
        if not query:
            click.echo(
                format_error_json(
                    "Empty query received from stdin",
                    "INPUT_ERROR",
                    400,
                )
            )
            sys.exit(1)

    # Determine output format (default to JSON if none specified)
    # Note: output_json is passed as parameter but we don't need to reassign it

    # At this point, query is guaranteed to be non-None due to validation above
    assert query is not None, "Query should be validated by this point"

    try:
        # Create client and perform search
        client = ObsidianClient()

        if query_type.lower() == "dataview":
            response = client.search_dataview(query)
        else:  # jsonlogic
            response = client.search_jsonlogic(query)

        # Format and output response
        if output_table:
            output = format_search_table(response)
        elif output_text:
            output = format_search_text(response)
        else:  # JSON
            output = format_search_json(response)

        click.echo(output)

        # Exit with error code if search failed
        if not response.success:
            sys.exit(1)

    except ObsidianAuthError as e:
        click.echo(format_error_json(str(e), "AUTH_ERROR", 401))
        sys.exit(1)
    except ObsidianConnectionError as e:
        click.echo(format_error_json(str(e), "CONNECTION_ERROR", 503))
        sys.exit(1)
    except ObsidianAPIError as e:
        click.echo(format_error_json(str(e), e.error_code, e.status_code))
        sys.exit(1)
    except ObsidianClientError as e:
        click.echo(format_error_json(str(e), "CLIENT_ERROR", 500))
        sys.exit(1)
    except Exception as e:
        click.echo(format_error_json(f"Unexpected error: {e}", "UNKNOWN_ERROR", 500))
        sys.exit(1)
