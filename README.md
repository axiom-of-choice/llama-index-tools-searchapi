# LlamaIndex Tools Integration: SearchApi

[![PyPI version](https://img.shields.io/pypi/v/llama-index-tools-searchapi.svg)](https://pypi.org/project/llama-index-tools-searchapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Multi-engine web search tool for [LlamaIndex](https://github.com/run-llama/llama_index) agents powered by [SearchApi.io](https://www.searchapi.io).

## Why

Most LlamaIndex search tools wrap a single provider — one engine, one result format, one use case. Real agent workflows need different search types depending on the task: web results for research, news for recency, shopping for product comparisons, YouTube for tutorials, job boards for recruiting pipelines.

SearchApi provides structured data from 100+ search engines through a single unified API. This integration exposes 7 engines through one `BaseToolSpec` class — your agent picks the right engine per query without needing multiple tools configured.

## What

A single `SearchApiToolSpec` class that gives LlamaIndex agents access to:

| Engine | Use Case |
|--------|----------|
| `google` | General web search (default) |
| `google_news` | Recent news and articles |
| `google_shopping` | Product search with prices |
| `google_jobs` | Job listings |
| `youtube` | Video search |
| `bing` | Alternative web search |
| `baidu` | Chinese language search |

The engine can be set at initialization (for specialized agents) or overridden per-query (for general-purpose agents that pick the right source dynamically).

## Installation

```bash
pip install llama-index-tools-searchapi
```

## Quick Start

Get your API key at [searchapi.io](https://www.searchapi.io) (free tier: 100 searches/month).

```python
from llama_index.tools.searchapi import SearchApiToolSpec
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

tool_spec = SearchApiToolSpec(api_key="your-key")

agent = FunctionAgent(
    tools=tool_spec.to_tool_list(),
    llm=OpenAI(model="gpt-4.1"),
)

response = await agent.run("what's the latest news about AI agents?")
```

## Usage Examples

### News Agent

```python
tool_spec = SearchApiToolSpec(api_key="your-key", engine="google_news")
```

### YouTube Research Agent

```python
tool_spec = SearchApiToolSpec(api_key="your-key", engine="youtube")
```

### Localized Search

```python
tool_spec = SearchApiToolSpec(api_key="your-key", num_results=5)
results = tool_spec.search("coffee shops", location="San Francisco", country="us", language="en")
```

### Per-query Engine Override

An agent with a default engine can still switch engines dynamically:

```python
tool_spec = SearchApiToolSpec(api_key="your-key")
results = tool_spec.search("wireless headphones", engine="google_shopping")
results = tool_spec.search("python async tutorial", engine="youtube")
```

## API Reference

### `SearchApiToolSpec(api_key, engine, num_results)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | required | SearchApi API key |
| `engine` | `str` | `"google"` | Default search engine |
| `num_results` | `int` | `10` | Default number of results |

### `search(query, engine, num_results, location, country, language)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `engine` | `str \| None` | `None` | Override default engine for this query |
| `num_results` | `int \| None` | `None` | Override default result count |
| `location` | `str \| None` | `None` | Location (e.g., `"New York"`) |
| `country` | `str \| None` | `None` | Country code (e.g., `"us"`) |
| `language` | `str \| None` | `None` | Language code (e.g., `"en"`) |

Returns a list of `Document` objects containing the structured search results.

## Contributing

Contributions welcome. To set up the dev environment:

```bash
git clone https://github.com/axiom-of-choice/llama-index-tools-searchapi.git
cd llama-index-tools-searchapi
uv sync --all-groups
uv pip install -e .
uv run pytest tests/ -v
```

Before submitting a PR:
- Run `uv run ruff check .`
- Run `uv run pytest tests/ -v`
- Add tests for any new functionality

### Ideas for contributions
- Add more engines (DuckDuckGo, Amazon, Scholar, etc.)
- Structured result parsing (return individual results as separate Documents)
- Async support via `httpx`
- Integration examples with different LlamaIndex agent types

## Related

- [SearchApi.io Documentation](https://www.searchapi.io/docs/google)
- [LlamaIndex Tools Guide](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/)
- [CrewAI SearchApi Integration](https://github.com/crewAIInc/crewAI/pull/6434)

## License

MIT
