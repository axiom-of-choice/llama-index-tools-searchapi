# LlamaIndex Tools Integration: SearchApi

[![PyPI version](https://img.shields.io/pypi/v/llama-index-tools-searchapi.svg)](https://pypi.org/project/llama-index-tools-searchapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Multi-engine web search tool for LlamaIndex agents powered by [SearchApi.io](https://www.searchapi.io).

SearchApi provides structured data from 100+ search engines through a single API. This integration supports Google, Google News, Google Shopping, Google Jobs, YouTube, Bing, and Baidu.

## Installation

```bash
pip install llama-index-tools-searchapi
```

## Setup

Get your API key at [searchapi.io](https://www.searchapi.io) (free tier: 100 searches/month).

## Usage

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

### Google News

```python
tool_spec = SearchApiToolSpec(api_key="your-key", engine="google_news")
```

### YouTube

```python
tool_spec = SearchApiToolSpec(api_key="your-key", engine="youtube")
```

### With Location and Language

```python
tool_spec = SearchApiToolSpec(api_key="your-key", num_results=5)
results = tool_spec.search("coffee shops", location="San Francisco", country="us", language="en")
```

### Per-query Engine Override

```python
tool_spec = SearchApiToolSpec(api_key="your-key")
results = tool_spec.search("wireless headphones", engine="google_shopping")
```

## Supported Engines

| Engine | Description |
|--------|-------------|
| `google` | Google web search (default) |
| `google_news` | Google News |
| `google_shopping` | Google Shopping |
| `google_jobs` | Google Jobs |
| `youtube` | YouTube video search |
| `bing` | Bing web search |
| `baidu` | Baidu search |

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | required | SearchApi API key |
| `engine` | `str` | `"google"` | Default search engine |
| `num_results` | `int` | `10` | Default number of results |
