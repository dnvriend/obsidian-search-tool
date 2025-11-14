"""Obsidian API client for search operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import os
from datetime import UTC, datetime
from typing import Any

import requests

from obsidian_search_tool.core.models import AuthResponse, SearchResponse, StatusResponse

logger = logging.getLogger(__name__)


class ObsidianClientError(Exception):
    """Base exception for Obsidian client errors."""

    pass


class ObsidianAuthError(ObsidianClientError):
    """Authentication error."""

    pass


class ObsidianConnectionError(ObsidianClientError):
    """Connection error."""

    pass


class ObsidianAPIError(ObsidianClientError):
    """API error with status code and message."""

    def __init__(self, message: str, status_code: int, error_code: str = "API_ERROR") -> None:
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: API error code
        """
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code


class ObsidianClient:
    """Client for interacting with Obsidian Local REST API.

    This client provides search-only operations for querying an Obsidian vault
    using Dataview DQL (TABLE queries) and JsonLogic queries.

    Attributes:
        base_url: API base URL (from OBSIDIAN_BASE_URL env var)
        api_key: API authentication token (from OBSIDIAN_API_KEY env var)
        timeout: Request timeout in seconds (from OBSIDIAN_TIMEOUT env var)
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int | None = None,
    ) -> None:
        """Initialize Obsidian client.

        Args:
            base_url: API base URL (default: from OBSIDIAN_BASE_URL or http://127.0.0.1:27123)
            api_key: API key (default: from OBSIDIAN_API_KEY env var)
            timeout: Request timeout in seconds (default: from OBSIDIAN_TIMEOUT or 30)

        Raises:
            ObsidianAuthError: If API key is not provided or found in environment
        """
        resolved_base_url = (
            base_url if base_url else os.getenv("OBSIDIAN_BASE_URL", "http://127.0.0.1:27123")
        )
        self.base_url = resolved_base_url.rstrip("/")
        self.api_key = api_key if api_key else os.getenv("OBSIDIAN_API_KEY", "")
        self.timeout = timeout if timeout else int(os.getenv("OBSIDIAN_TIMEOUT", "30"))

        if not self.api_key:
            raise ObsidianAuthError(
                "OBSIDIAN_API_KEY environment variable is required. "
                "Get the API key from Obsidian Local REST API plugin settings."
            )

        logger.debug(f"Initialized ObsidianClient with base_url={self.base_url}")

    def _get_headers(self, content_type: str = "application/json") -> dict[str, str]:
        """Build HTTP headers for API requests.

        Args:
            content_type: Content-Type header value

        Returns:
            Dictionary of HTTP headers
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": content_type,
            "Accept": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: str | None = None,
        content_type: str = "application/json",
    ) -> dict[str, Any]:
        """Make HTTP request to Obsidian API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            content_type: Content-Type header value

        Returns:
            Parsed JSON response

        Raises:
            ObsidianConnectionError: If network error occurs
            ObsidianAPIError: If API returns error response
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(content_type)

        logger.debug(f"API Request: {method} {url}")
        if data:
            logger.debug(f"Request data: {data[:200]}...")

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data.encode("utf-8") if data else None,
                timeout=self.timeout,
            )

            logger.debug(f"API Response Status: {response.status_code}")

            # Handle error responses
            if response.status_code >= 400:
                self._handle_error_response(response)

            # Parse JSON response
            return response.json() if response.text else {}

        except requests.exceptions.Timeout as e:
            raise ObsidianConnectionError(
                f"Request timeout after {self.timeout}s. "
                "Ensure Obsidian is running and the Local REST API plugin is enabled."
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise ObsidianConnectionError(
                f"Connection failed to {self.base_url}. "
                "Ensure Obsidian is running and the Local REST API plugin is enabled."
            ) from e
        except requests.exceptions.RequestException as e:
            raise ObsidianConnectionError(f"Network error: {e}") from e

    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle HTTP error responses.

        Args:
            response: HTTP response object

        Raises:
            ObsidianAuthError: If authentication fails (401)
            ObsidianAPIError: For other API errors
        """
        status_code = response.status_code
        error_message = "Unknown error"
        error_code = "API_ERROR"

        # Try to parse JSON error response
        try:
            body = response.json()
            error_message = body.get("message", body.get("error", "Unknown error"))
            error_code = body.get("errorCode", body.get("error_code", "API_ERROR"))
        except Exception:
            error_message = response.text or "Unknown error"

        # Special handling for common HTTP errors
        if status_code == 401:
            raise ObsidianAuthError(
                "Authentication failed. Check your OBSIDIAN_API_KEY. "
                "Get the API key from Obsidian Local REST API plugin settings."
            )
        elif status_code == 403:
            error_message = "Access forbidden. You may not have permission for this operation."
        elif status_code == 404:
            error_message = "Resource not found."
        elif status_code == 422:
            error_message = f"Invalid request: {error_message}"
            error_code = "VALIDATION_ERROR"
        elif status_code >= 500:
            error_message = f"Internal server error: {error_message}"
            error_code = "SERVER_ERROR"

        raise ObsidianAPIError(error_message, status_code, error_code)

    def status(self) -> StatusResponse:
        """Check API connectivity.

        Returns:
            StatusResponse with connection status

        Raises:
            ObsidianConnectionError: If connection fails
            ObsidianAPIError: If API returns error
        """
        logger.info("Checking API status")
        self._make_request("GET", "/")

        return StatusResponse(
            status="connected",
            api_url=self.base_url,
            timestamp=datetime.now(UTC).isoformat(),
            message="API is reachable",
        )

    def check_auth(self) -> AuthResponse:
        """Validate authentication.

        Returns:
            AuthResponse with authentication status

        Raises:
            ObsidianAuthError: If authentication fails
            ObsidianConnectionError: If connection fails
            ObsidianAPIError: If API returns error
        """
        logger.info("Checking authentication")
        self._make_request("GET", "/")

        return AuthResponse(
            status="authenticated",
            api_url=self.base_url,
            timestamp=datetime.now(UTC).isoformat(),
            message="Authentication is valid",
        )

    def search_dataview(self, query: str) -> SearchResponse:
        """Search vault using Dataview DQL query.

        Dataview queries use the Dataview Query Language (DQL) to search vault files.
        Only TABLE queries are supported by the API.

        Args:
            query: Dataview DQL query string (e.g., "TABLE file.name FROM #project")

        Returns:
            SearchResponse with search results

        Raises:
            ObsidianConnectionError: If connection fails
            ObsidianAPIError: If API returns error

        Examples:
            >>> client.search_dataview('TABLE file.name, author WHERE author')
            >>> client.search_dataview('TABLE file.name FROM #meeting SORT file.mtime DESC')
        """
        logger.info(f"Dataview DQL search: query='{query}'")

        endpoint = "/search/"
        content_type = "application/vnd.olrapi.dataview.dql+txt"

        try:
            response_data = self._make_request("POST", endpoint, query, content_type)

            # Build successful response
            data = {
                "query": query,
                "search_type": "dataview",
                "timestamp": datetime.now(UTC).isoformat(),
                "results": response_data,
            }

            return SearchResponse(success=True, data=data, error=None)

        except ObsidianAPIError as e:
            logger.error(f"Dataview search failed: {e}")
            error = {
                "message": str(e),
                "code": e.error_code,
                "status_code": e.status_code,
            }
            return SearchResponse(success=False, data=None, error=error)

    def search_jsonlogic(self, query: str) -> SearchResponse:
        """Search vault using JsonLogic query.

        JsonLogic queries use JSON format to search vault files. Available variables:
        - filename: File path relative to vault root
        - frontmatter.*: YAML frontmatter fields (e.g., frontmatter.tags)
        - content: Full file content (for text search)

        Args:
            query: JsonLogic query in JSON format

        Returns:
            SearchResponse with search results

        Raises:
            ObsidianConnectionError: If connection fails
            ObsidianAPIError: If API returns error

        Examples:
            >>> client.search_jsonlogic('{"in": [{"var": "frontmatter.tags"}, "project"]}')
            >>> client.search_jsonlogic('{"startsWith": [{"var": "filename"}, "daily/"]}')
        """
        logger.info(f"JsonLogic search: query='{query}'")

        endpoint = "/search/"
        content_type = "application/vnd.olrapi.jsonlogic+json"

        try:
            response_data = self._make_request("POST", endpoint, query, content_type)

            # Build successful response
            data = {
                "query": query,
                "search_type": "jsonlogic",
                "timestamp": datetime.now(UTC).isoformat(),
                "results": response_data,
            }

            return SearchResponse(success=True, data=data, error=None)

        except ObsidianAPIError as e:
            logger.error(f"JsonLogic search failed: {e}")
            error = {
                "message": str(e),
                "code": e.error_code,
                "status_code": e.status_code,
            }
            return SearchResponse(success=False, data=None, error=error)
