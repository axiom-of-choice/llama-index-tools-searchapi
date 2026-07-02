"""Demo: SearchApiToolSpec multi-engine search for LlamaIndex agents.

Run with:
    doppler run --project search --config dev_personal -- python examples/demo.py
"""

import json
import os
import sys

from llama_index.tools.searchapi import SearchApiToolSpec


def print_section(engine: str, query: str) -> None:
    print(f"\n{'='*60}")
    print(f"  Engine: {engine}")
    print(f"  Query:  {query}")
    print("=" * 60)


def main() -> None:
    api_key = os.getenv("SEARCHAPI_API_KEY")
    if not api_key:
        print("SEARCHAPI_API_KEY not set. Run with:")
        print("  doppler run --project search --config dev_personal -- python examples/demo.py")
        sys.exit(1)

    tool_spec = SearchApiToolSpec(api_key=api_key, num_results=3)

    demos = [
        ("google", "LlamaIndex AI agents framework"),
        ("google_news", "artificial intelligence startups 2026"),
        ("google_shopping", "ergonomic mechanical keyboard"),
        ("youtube", "LlamaIndex RAG tutorial"),
    ]

    print("\nSearchApiToolSpec Demo — Multi-Engine Search")
    print("=" * 60)

    for engine, query in demos:
        print_section(engine, query)
        results = tool_spec.search(query, engine=engine)
        text = results[0].text
        parsed = eval(text)

        if engine == "google":
            for r in parsed.get("organic_results", [])[:3]:
                print(f"  [{r.get('position')}] {r.get('title')}")
                print(f"      {r.get('link')}")
                print(f"      {r.get('snippet', '')[:100]}")
                print()

        elif engine == "google_news":
            for r in parsed.get("organic_results", parsed.get("news_results", []))[:3]:
                print(f"  [{r.get('position')}] {r.get('title')}")
                print(f"      Source: {r.get('source', 'N/A')} | {r.get('date', '')}")
                print()

        elif engine == "google_shopping":
            for r in parsed.get("shopping_results", [])[:3]:
                print(f"  {r.get('title', '')[:60]}")
                print(f"      Price: {r.get('price', 'N/A')} | {r.get('source', '')}")
                print()

        elif engine == "youtube":
            for r in parsed.get("video_results", parsed.get("videos", []))[:3]:
                title = r.get("title", "")
                channel = r.get("channel", {})
                ch_name = channel.get("title", "") if isinstance(channel, dict) else str(channel)
                print(f"  {title}")
                print(f"      Channel: {ch_name} | Views: {r.get('views', 'N/A')}")
                print()

    # Show tool list (what an agent sees)
    print("\n" + "=" * 60)
    print("  Agent Tool List")
    print("=" * 60)
    tools = tool_spec.to_tool_list()
    for t in tools:
        print(f"  - {t.metadata.name}: {t.metadata.description[:80]}")

    print(f"\nDone. {len(demos)} engines tested.")


if __name__ == "__main__":
    main()
