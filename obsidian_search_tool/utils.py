"""Utility functions for obsidian-search-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import logging
import sys
from typing import Any

from rich.console import Console
from rich.table import Table

from obsidian_search_tool.core.models import AuthResponse, SearchResponse, StatusResponse

console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application.

    Args:
        verbose: Enable verbose (DEBUG) logging if True, otherwise WARNING
    """
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )


def format_json(data: dict[str, Any]) -> str:
    """Format data as JSON string.

    Args:
        data: Dictionary to serialize as JSON

    Returns:
        Formatted JSON string with 2-space indentation
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_status_json(response: StatusResponse) -> str:
    """Format status response as JSON.

    Args:
        response: StatusResponse object

    Returns:
        JSON string representation
    """
    data = {
        "success": True,
        "data": {
            "status": response.status,
            "api_url": response.api_url,
            "timestamp": response.timestamp,
            "message": response.message,
        },
    }
    return format_json(data)


def format_auth_json(response: AuthResponse) -> str:
    """Format auth response as JSON.

    Args:
        response: AuthResponse object

    Returns:
        JSON string representation
    """
    data = {
        "success": True,
        "data": {
            "status": response.status,
            "api_url": response.api_url,
            "timestamp": response.timestamp,
            "message": response.message,
        },
    }
    return format_json(data)


def format_search_json(response: SearchResponse) -> str:
    """Format search response as JSON.

    Args:
        response: SearchResponse object

    Returns:
        JSON string representation
    """
    if response.success:
        data = {"success": True, "data": response.data}
    else:
        data = {"success": False, "error": response.error}
    return format_json(data)


def format_status_text(response: StatusResponse) -> str:
    """Format status response as markdown text.

    Args:
        response: StatusResponse object

    Returns:
        Markdown-formatted string
    """
    return f"""# API Status

**Status:** {response.status}
**API URL:** {response.api_url}
**Timestamp:** {response.timestamp}

{response.message}
"""


def format_auth_text(response: AuthResponse) -> str:
    """Format auth response as markdown text.

    Args:
        response: AuthResponse object

    Returns:
        Markdown-formatted string
    """
    return f"""# Authentication Status

**Status:** {response.status}
**API URL:** {response.api_url}
**Timestamp:** {response.timestamp}

{response.message}
"""


def format_search_text(response: SearchResponse) -> str:
    """Format search response as markdown text.

    Shows query metadata, result count summary, and file paths with
    clickable links (if terminal supports OSC 8).

    Args:
        response: SearchResponse object

    Returns:
        Markdown-formatted string
    """
    if not response.success:
        error = response.error or {}
        return f"""# Search Error

**Error Code:** {error.get("code", "UNKNOWN")}
**Status Code:** {error.get("status_code", "N/A")}

{error.get("message", "Unknown error occurred")}
"""

    lines = ["# Search Results", ""]
    lines.append(f"**Query Type:** {response.search_type.capitalize()}")
    lines.append(f"**Query:** {response.query}")
    lines.append(f"**Timestamp:** {response.timestamp}")
    lines.append(f"**Results Found:** {response.result_count} notes")
    lines.append("")

    if response.result_count == 0:
        lines.append("No results found.")
        return "\n".join(lines)

    lines.append("## Files")
    lines.append("")

    # Format results as list with clickable links
    for result in response.results:
        if isinstance(result, dict):
            # Try to extract filename from result
            filename = result.get("filename", result.get("file", result.get("path", "Unknown")))
            # Create clickable link using OSC 8 (supported by some terminals)
            # Format: \x1b]8;;file://path\x1b\\text\x1b]8;;\x1b\\
            lines.append(f"- {filename}")
        else:
            lines.append(f"- {result}")

    return "\n".join(lines)


def format_search_table(response: SearchResponse) -> str:
    """Format search response as pretty-printed table.

    Args:
        response: SearchResponse object

    Returns:
        Rich table formatted as string
    """
    if not response.success:
        error = response.error or {}
        return f"Error: {error.get('message', 'Unknown error')}"

    if response.result_count == 0:
        return "No results found."

    # Create Rich table
    table = Table(title=f"Search Results ({response.result_count} found)")

    # Add columns based on first result
    if response.results and isinstance(response.results[0], dict):
        first_result = response.results[0]
        for key in first_result.keys():
            table.add_column(key.capitalize(), overflow="fold")

        # Add rows
        for result in response.results:
            if isinstance(result, dict):
                row_values = [str(result.get(key, "")) for key in first_result.keys()]
                table.add_row(*row_values)
    else:
        # Fallback for non-dict results
        table.add_column("Result")
        for result in response.results:
            table.add_row(str(result))

    # Capture table output as string
    from io import StringIO

    output = StringIO()
    temp_console = Console(file=output, force_terminal=True)
    temp_console.print(table)
    return output.getvalue()


def format_error_json(message: str, code: str = "ERROR", status_code: int = 500) -> str:
    """Format error as JSON response.

    Args:
        message: Error message
        code: Error code
        status_code: HTTP status code

    Returns:
        JSON string representation
    """
    data = {
        "success": False,
        "error": {
            "message": message,
            "code": code,
            "status_code": status_code,
        },
    }
    return format_json(data)
