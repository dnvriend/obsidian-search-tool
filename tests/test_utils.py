"""Tests for obsidian_search_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json

from obsidian_search_tool.core.models import AuthResponse, SearchResponse, StatusResponse
from obsidian_search_tool.utils import (
    format_auth_json,
    format_auth_text,
    format_error_json,
    format_json,
    format_search_json,
    format_search_text,
    format_status_json,
    format_status_text,
)


def test_format_json() -> None:
    """Test that format_json returns formatted JSON string."""
    data = {"key": "value", "number": 42}
    result = format_json(data)
    assert isinstance(result, str)
    # Verify it's valid JSON
    parsed = json.loads(result)
    assert parsed == data


def test_format_status_json() -> None:
    """Test that format_status_json returns correct JSON structure."""
    response = StatusResponse(
        status="connected",
        api_url="http://127.0.0.1:27123",
        timestamp="2025-01-01T00:00:00Z",
        message="API is reachable",
    )
    result = format_status_json(response)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed["success"] is True
    assert parsed["data"]["status"] == "connected"
    assert parsed["data"]["api_url"] == "http://127.0.0.1:27123"


def test_format_auth_json() -> None:
    """Test that format_auth_json returns correct JSON structure."""
    response = AuthResponse(
        status="authenticated",
        api_url="http://127.0.0.1:27123",
        timestamp="2025-01-01T00:00:00Z",
        message="Authentication is valid",
    )
    result = format_auth_json(response)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed["success"] is True
    assert parsed["data"]["status"] == "authenticated"


def test_format_search_json_success() -> None:
    """Test that format_search_json returns correct JSON for successful search."""
    response = SearchResponse(
        success=True,
        data={
            "query": "TABLE file.name",
            "search_type": "dataview",
            "timestamp": "2025-01-01T00:00:00Z",
            "results": [{"filename": "test.md"}],
        },
        error=None,
    )
    result = format_search_json(response)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed["success"] is True
    assert "data" in parsed
    assert parsed["data"]["search_type"] == "dataview"


def test_format_search_json_error() -> None:
    """Test that format_search_json returns correct JSON for failed search."""
    response = SearchResponse(
        success=False,
        data=None,
        error={"message": "Test error", "code": "TEST_ERROR", "status_code": 400},
    )
    result = format_search_json(response)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed["success"] is False
    assert "error" in parsed
    assert parsed["error"]["code"] == "TEST_ERROR"


def test_format_status_text() -> None:
    """Test that format_status_text returns markdown formatted text."""
    response = StatusResponse(
        status="connected",
        api_url="http://127.0.0.1:27123",
        timestamp="2025-01-01T00:00:00Z",
        message="API is reachable",
    )
    result = format_status_text(response)
    assert isinstance(result, str)
    assert "# API Status" in result
    assert "connected" in result
    assert "http://127.0.0.1:27123" in result


def test_format_auth_text() -> None:
    """Test that format_auth_text returns markdown formatted text."""
    response = AuthResponse(
        status="authenticated",
        api_url="http://127.0.0.1:27123",
        timestamp="2025-01-01T00:00:00Z",
        message="Authentication is valid",
    )
    result = format_auth_text(response)
    assert isinstance(result, str)
    assert "# Authentication Status" in result
    assert "authenticated" in result


def test_format_search_text_success() -> None:
    """Test that format_search_text returns markdown formatted text for success."""
    response = SearchResponse(
        success=True,
        data={
            "query": "TABLE file.name",
            "search_type": "dataview",
            "timestamp": "2025-01-01T00:00:00Z",
            "results": [{"filename": "test.md"}, {"filename": "test2.md"}],
        },
        error=None,
    )
    result = format_search_text(response)
    assert isinstance(result, str)
    assert "# Search Results" in result
    assert "Dataview" in result
    assert "2 notes" in result
    assert "test.md" in result


def test_format_search_text_error() -> None:
    """Test that format_search_text returns markdown formatted text for error."""
    response = SearchResponse(
        success=False,
        data=None,
        error={"message": "Test error", "code": "TEST_ERROR", "status_code": 400},
    )
    result = format_search_text(response)
    assert isinstance(result, str)
    assert "# Search Error" in result
    assert "TEST_ERROR" in result
    assert "Test error" in result


def test_format_error_json() -> None:
    """Test that format_error_json returns correct JSON structure."""
    result = format_error_json("Test error", "TEST_ERROR", 400)
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed["success"] is False
    assert parsed["error"]["message"] == "Test error"
    assert parsed["error"]["code"] == "TEST_ERROR"
    assert parsed["error"]["status_code"] == 400


def test_search_response_properties() -> None:
    """Test SearchResponse property methods."""
    response = SearchResponse(
        success=True,
        data={
            "query": "TABLE file.name",
            "search_type": "dataview",
            "timestamp": "2025-01-01T00:00:00Z",
            "results": [{"filename": "test.md"}, {"filename": "test2.md"}],
        },
        error=None,
    )
    assert response.query == "TABLE file.name"
    assert response.search_type == "dataview"
    assert response.timestamp == "2025-01-01T00:00:00Z"
    assert response.result_count == 2
    assert len(response.results) == 2
