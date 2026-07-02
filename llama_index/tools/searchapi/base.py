"""SearchApi.io tool spec for LlamaIndex agents."""

from typing import List

import requests
from llama_index.core.schema import Document
from llama_index.core.tools.tool_spec.base import BaseToolSpec

BASE_URL = "https://www.searchapi.io/api/v1/search"

SUPPORTED_ENGINES = [
    "google",
    "google_news",
    "google_shopping",
    "google_jobs",
    "youtube",
    "bing",
    "baidu",
]


class SearchApiToolSpec(BaseToolSpec):
    """SearchApi.io tool spec for multi-engine web search.

    Supports Google, Google News, Google Shopping, Google Jobs,
    YouTube, Bing, and Baidu through a single unified API.
    """

    spec_functions = ["search"]

    def __init__(
        self,
        api_key: str,
        engine: str = "google",
        num_results: int = 10,
    ) -> None:
        """Initialize with SearchApi credentials and default configuration.

        Args:
            api_key: SearchApi API key (get one at https://www.searchapi.io).
            engine: Default search engine to use.
            num_results: Default number of results to return.
        """
        if engine not in SUPPORTED_ENGINES:
            raise ValueError(
                f"Invalid engine: {engine}. "
                f"Must be one of: {', '.join(SUPPORTED_ENGINES)}"
            )
        self.api_key = api_key
        self.engine = engine
        self.num_results = num_results

    def search(
        self,
        query: str,
        engine: str | None = None,
        num_results: int | None = None,
        location: str | None = None,
        country: str | None = None,
        language: str | None = None,
    ) -> List[Document]:
        """Search the web using SearchApi.io.

        Args:
            query: The search query string.
            engine: Search engine override (google, google_news, youtube, etc.).
            num_results: Number of results to return (overrides default).
            location: Location to perform the search from (e.g., "New York").
            country: Country code for localized results (e.g., "us").
            language: Language code (e.g., "en").

        Returns:
            A list of Document objects containing the search results.
        """
        params: dict[str, str | int] = {
            "engine": engine or self.engine,
            "q": query,
            "num": num_results or self.num_results,
        }

        if location:
            params["location"] = location
        if country:
            params["gl"] = country
        if language:
            params["hl"] = language

        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        results = response.json()

        for key in ["search_metadata", "search_parameters", "pagination"]:
            results.pop(key, None)

        return [Document(text=str(results))]
