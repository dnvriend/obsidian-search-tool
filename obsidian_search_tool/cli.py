"""CLI entry point for obsidian-search-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from obsidian_search_tool.commands import auth, search, status


@click.group()
@click.version_option(version="0.1.0", prog_name="obsidian-search-tool")
def main() -> None:
    """Obsidian Search Tool - Search your Obsidian vault via CLI.

    A command-line tool for searching an Obsidian vault through the Obsidian
    Local REST API using Dataview Query Language (DQL) - TABLE queries only -
    and JsonLogic queries.

    \b
    PREREQUISITES:
        1. Obsidian must be running
        2. "Local REST API" plugin by Adam Coddington must be installed and enabled
        3. "Dataview" plugin by Michael Brenan must be installed and enabled
        4. OBSIDIAN_API_KEY environment variable must be set with API key from plugin settings

    \b
    QUICK START:
        # Set API key (get from Obsidian plugin settings)
        export OBSIDIAN_API_KEY="your-api-key-here"

        # Check connectivity
        obsidian-search-tool status

        # Validate authentication
        obsidian-search-tool auth

        # Search with Dataview DQL (default)
        obsidian-search-tool search --query 'TABLE file.name FROM #project'

        # Search with JsonLogic
        obsidian-search-tool search --type jsonlogic \\
            --query '{"in": [{"var": "frontmatter.tags"}, "project"]}'

    \b
    COMMANDS:
        status    Check API connectivity
        auth      Validate authentication
        search    Search vault with Dataview DQL or JsonLogic

    \b
    ENVIRONMENT VARIABLES:
        OBSIDIAN_API_KEY   - API token (required, from plugin settings)
        OBSIDIAN_BASE_URL  - API URL (default: http://127.0.0.1:27123)
        OBSIDIAN_TIMEOUT   - Request timeout in seconds (default: 30)
        OBSIDIAN_VERBOSE   - Enable verbose logging (true/false)

    \b
    EXAMPLES:
        # Basic status check
        obsidian-search-tool status

        # Search with TABLE query
        obsidian-search-tool search --query 'TABLE file.name, author WHERE author'

        # Search with text output
        obsidian-search-tool search --query 'TABLE file.name' --text

        # Search with table output
        obsidian-search-tool search --query 'TABLE file.name, status' --table

        # Search from stdin
        echo 'TABLE file.name FROM #meeting' | obsidian-search-tool search --stdin

        # JsonLogic search
        obsidian-search-tool search --type jsonlogic \\
            --query '{"in": [{"var": "frontmatter.tags"}, "aws"]}'

    \b
    For detailed help on any command, use:
        obsidian-search-tool COMMAND --help

    \b
    Documentation: https://github.com/dnvriend/obsidian-search-tool
    Obsidian Local REST API: https://github.com/coddingtonbear/obsidian-local-rest-api
    """
    pass


# Register commands
main.add_command(status)
main.add_command(auth)
main.add_command(search)


if __name__ == "__main__":
    main()
