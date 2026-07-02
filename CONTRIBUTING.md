# Contributing to llama-index-tools-searchapi

Thanks for your interest in contributing! This guide covers setup, development workflow, and release process.

## Development Setup

```bash
git clone https://github.com/axiom-of-choice/llama-index-tools-searchapi.git
cd llama-index-tools-searchapi
uv sync --all-groups
uv pip install -e .
```

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable releases. Protected — requires PR review. |
| `develop` | Integration branch for features. |
| `feat/*` | Feature branches (branch from `main` or `develop`) |
| `fix/*` | Bug fix branches |
| `docs/*` | Documentation-only changes |

All changes to `main` go through pull requests with at least one review.

## Development Workflow

1. Create a branch from `main`:
   ```bash
   git checkout main && git checkout -b feat/your-feature
   ```

2. Make changes and run checks:
   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run pytest tests/ -v
   ```

3. Commit with descriptive messages:
   ```bash
   git commit -m "feat: add bing search support"
   ```

4. Push and open a PR against `main`.

## Running Tests

```bash
# All tests (mocked, no API key needed)
uv run pytest tests/ -v

# Live demo (requires SearchApi key)
doppler run --project search --config dev_personal -- uv run python examples/demo.py
```

## Code Style

- **Formatter:** ruff (`uv run ruff format .`)
- **Linter:** ruff (`uv run ruff check .`)
- **Target:** Python 3.10+
- **Type hints:** Required on all public functions

## Adding a New Engine

1. Add the engine name to `SUPPORTED_ENGINES` in `base.py`
2. Add a test case in `tests/test_tools_searchapi.py`
3. Update the README table
4. Test with a live API call

## Release Process

Releases are published to PyPI from the `main` branch.

1. Update version in `pyproject.toml`
2. Commit: `chore: bump version to X.Y.Z`
3. Tag: `git tag vX.Y.Z`
4. Build and publish:
   ```bash
   uv build
   uv publish --token $PYPI_TOKEN
   ```
5. Push tag: `git push origin vX.Y.Z`

### Versioning

Follows [Semantic Versioning](https://semver.org/):
- **Patch** (0.1.x): Bug fixes, dependency updates
- **Minor** (0.x.0): New engines, new parameters, non-breaking additions
- **Major** (x.0.0): Breaking API changes

## Ideas for Contributions

- Add more engines (DuckDuckGo, Amazon, Scholar, etc.)
- Structured result parsing (individual results as separate Documents)
- Async support via `httpx`
- Integration examples with different LlamaIndex agent types
- Caching layer for repeated queries

## Questions?

Open an issue on the [GitHub repo](https://github.com/axiom-of-choice/llama-index-tools-searchapi/issues).
