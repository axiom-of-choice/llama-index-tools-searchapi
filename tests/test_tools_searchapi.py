"""Tests for SearchApi tool spec."""

from unittest.mock import MagicMock, patch

import pytest
from llama_index.core.schema import Document
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.tools.searchapi import SearchApiToolSpec


class TestSearchApiToolSpec:
    """Test initialization and class structure."""

    def test_class_inherits_base_tool_spec(self):
        names_of_base_classes = [b.__name__ for b in SearchApiToolSpec.__mro__]
        assert BaseToolSpec.__name__ in names_of_base_classes

    def test_spec_functions(self):
        assert "search" in SearchApiToolSpec.spec_functions

    def test_initialization(self):
        tool = SearchApiToolSpec(api_key="test_key")
        assert tool.api_key == "test_key"
        assert tool.engine == "google"
        assert tool.num_results == 10

    def test_custom_initialization(self):
        tool = SearchApiToolSpec(api_key="test_key", engine="youtube", num_results=5)
        assert tool.engine == "youtube"
        assert tool.num_results == 5

    def test_invalid_engine_raises(self):
        with pytest.raises(ValueError, match="Invalid engine"):
            SearchApiToolSpec(api_key="test_key", engine="invalid")


class TestSearch:
    """Test the search method."""

    @patch("llama_index.tools.searchapi.base.requests.get")
    def test_search_returns_documents(self, mock_get: MagicMock):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "search_metadata": {"id": "abc"},
            "search_parameters": {"q": "test"},
            "organic_results": [
                {"title": "Result 1", "link": "http://r1.com"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = SearchApiToolSpec(api_key="test_key")
        results = tool.search("test query")

        assert len(results) == 1
        assert isinstance(results[0], Document)
        assert "organic_results" in results[0].text
        assert "search_metadata" not in results[0].text

    @patch("llama_index.tools.searchapi.base.requests.get")
    def test_search_passes_correct_params(self, mock_get: MagicMock):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = SearchApiToolSpec(api_key="test_key", engine="google", num_results=5)
        tool.search("test", location="New York", country="us", language="en")

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["params"]["engine"] == "google"
        assert call_kwargs["params"]["q"] == "test"
        assert call_kwargs["params"]["num"] == 5
        assert call_kwargs["params"]["location"] == "New York"
        assert call_kwargs["params"]["gl"] == "us"
        assert call_kwargs["params"]["hl"] == "en"
        assert call_kwargs["headers"]["Authorization"] == "Bearer test_key"

    @patch("llama_index.tools.searchapi.base.requests.get")
    def test_search_engine_override(self, mock_get: MagicMock):
        mock_response = MagicMock()
        mock_response.json.return_value = {"videos": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = SearchApiToolSpec(api_key="test_key", engine="google")
        tool.search("python tutorial", engine="youtube")

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["params"]["engine"] == "youtube"

    @patch("llama_index.tools.searchapi.base.requests.get")
    def test_search_optional_params_not_sent_when_none(self, mock_get: MagicMock):
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = SearchApiToolSpec(api_key="test_key")
        tool.search("test")

        call_kwargs = mock_get.call_args.kwargs
        assert "location" not in call_kwargs["params"]
        assert "gl" not in call_kwargs["params"]
        assert "hl" not in call_kwargs["params"]

    @patch("llama_index.tools.searchapi.base.requests.get")
    def test_to_tool_list(self, mock_get: MagicMock):
        tool = SearchApiToolSpec(api_key="test_key")
        tools = tool.to_tool_list()
        assert len(tools) >= 1
        tool_names = [t.metadata.name for t in tools]
        assert "search" in tool_names
