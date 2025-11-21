"""Status and authentication commands for Obsidian Search Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from obsidian_search_tool.core.client import (
    ObsidianAuthError,
    ObsidianClient,
    ObsidianClientError,
    ObsidianConnectionError,
)
from obsidian_search_tool.logging_config import get_logger, setup_logging
from obsidian_search_tool.utils import (
    format_auth_json,
    format_auth_text,
    format_error_json,
    format_status_json,
    format_status_text,
)

logger = get_logger(__name__)


@click.command()
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
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def status(output_json: bool, output_text: bool, verbose: int) -> None:
    """Check API connectivity.

    Verifies that the Obsidian Local REST API is reachable and responding.
    Use this command to debug connection issues before performing searches.

    \b
    Examples:
        # Check status with JSON output
        obsidian-search-tool status

        # Check status with text output
        obsidian-search-tool status --text

        # Check status with verbose logging
        obsidian-search-tool status --verbose

    \b
    ENVIRONMENT VARIABLES:
        OBSIDIAN_API_KEY - API token (required, from plugin settings)
        OBSIDIAN_BASE_URL - API URL (default: http://127.0.0.1:27123)
        OBSIDIAN_TIMEOUT - Request timeout in seconds (default: 30)

    \b
    COMMON ERRORS & SOLUTIONS:
        Error: "OBSIDIAN_API_KEY environment variable is required"
        Solution: Set OBSIDIAN_API_KEY from Obsidian Local REST API plugin settings

        Error: "Connection failed"
        Solution: Ensure Obsidian is running and Local REST API plugin is enabled

        Error: "Request timeout"
        Solution: Increase OBSIDIAN_TIMEOUT or check network connectivity
    """
    # Setup logging
    setup_logging(verbose)
    logger.info("Status command started")

    # Determine output format (default to JSON if not specified)
    # Note: output_json is passed as parameter but we don't need to reassign it

    try:
        # Create client and check status
        logger.debug("Initializing Obsidian client")
        client = ObsidianClient()
        logger.debug("Checking API status")
        response = client.status()
        logger.info(f"Status check successful: {response.status}")

        # Format and output response
        if output_text:
            logger.debug("Formatting output as text")
            output = format_status_text(response)
        else:  # JSON
            logger.debug("Formatting output as JSON")
            output = format_status_json(response)

        click.echo(output)
        logger.info("Status command completed successfully")

    except ObsidianAuthError as e:
        logger.error(f"Authentication error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "AUTH_ERROR", 401))
        sys.exit(1)
    except ObsidianConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "CONNECTION_ERROR", 503))
        sys.exit(1)
    except ObsidianClientError as e:
        logger.error(f"Client error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "CLIENT_ERROR", 500))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(f"Unexpected error: {e}", "UNKNOWN_ERROR", 500))
        sys.exit(1)


@click.command()
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
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def auth(output_json: bool, output_text: bool, verbose: int) -> None:
    """Validate authentication.

    Verifies that the API key is valid and authentication is working correctly.
    Use this command to test your OBSIDIAN_API_KEY before performing searches.

    \b
    Examples:
        # Check authentication with JSON output
        obsidian-search-tool auth

        # Check authentication with text output
        obsidian-search-tool auth --text

        # Check authentication with verbose logging
        obsidian-search-tool auth --verbose

    \b
    ENVIRONMENT VARIABLES:
        OBSIDIAN_API_KEY - API token (required, from plugin settings)
        OBSIDIAN_BASE_URL - API URL (default: http://127.0.0.1:27123)
        OBSIDIAN_TIMEOUT - Request timeout in seconds (default: 30)

    \b
    GETTING YOUR API KEY:
        1. Open Obsidian
        2. Go to Settings → Community Plugins
        3. Find "Local REST API" plugin
        4. Click plugin settings
        5. Copy the API key from the settings page
        6. Set environment variable: export OBSIDIAN_API_KEY="your-key-here"

    \b
    COMMON ERRORS & SOLUTIONS:
        Error: "OBSIDIAN_API_KEY environment variable is required"
        Solution: Set OBSIDIAN_API_KEY from plugin settings (see above)

        Error: "Authentication failed"
        Solution: Verify API key is correct, regenerate if needed in plugin settings

        Error: "Connection failed"
        Solution: Ensure Obsidian is running and Local REST API plugin is enabled
    """
    # Setup logging
    setup_logging(verbose)
    logger.info("Auth command started")

    # Determine output format (default to JSON if not specified)
    # Note: output_json is passed as parameter but we don't need to reassign it

    try:
        # Create client and check authentication
        logger.debug("Initializing Obsidian client")
        client = ObsidianClient()
        logger.debug("Checking authentication")
        response = client.check_auth()
        logger.info(f"Authentication check successful: {response.status}")

        # Format and output response
        if output_text:
            logger.debug("Formatting output as text")
            output = format_auth_text(response)
        else:  # JSON
            logger.debug("Formatting output as JSON")
            output = format_auth_json(response)

        click.echo(output)
        logger.info("Auth command completed successfully")

    except ObsidianAuthError as e:
        logger.error(f"Authentication error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "AUTH_ERROR", 401))
        sys.exit(1)
    except ObsidianConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "CONNECTION_ERROR", 503))
        sys.exit(1)
    except ObsidianClientError as e:
        logger.error(f"Client error: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(str(e), "CLIENT_ERROR", 500))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        click.echo(format_error_json(f"Unexpected error: {e}", "UNKNOWN_ERROR", 500))
        sys.exit(1)
