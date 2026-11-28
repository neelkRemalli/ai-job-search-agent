# Dependency environment notes

## `pydantic-settings` / PyPI DNS issue

On 2026-11-25, `uv add pydantic-settings` failed while resolving
`https://pypi.org/simple/pydantic-settings/` because DNS could not resolve
PyPI (`Temporary failure in name resolution`). A subsequent offline attempt
also failed: the local uv cache has index metadata but not the package data
needed to resolve and install `pydantic-settings`.

At the time of inspection, `pydantic-settings` was absent from `pyproject.toml`,
`uv.lock`, and `.venv`. No `pydantic_settings` or `BaseSettings` use was found
under `app/` or `tests/`, so the current application does not require this
package to run. Do not use `uv add --frozen` as a workaround; that can leave
the manifest and lockfile out of sync.

When PyPI DNS/network access is available, finish the dependency addition with:

```sh
UV_CACHE_DIR=/tmp/uv-cache uv add pydantic-settings
UV_CACHE_DIR=/tmp/uv-cache uv sync --locked
UV_CACHE_DIR=/tmp/uv-cache uv run python -c "import sys, pydantic_settings; print(sys.version); print(pydantic_settings.__version__)"
```

The project selects Python 3.12 via `.python-version`; use `uv run` or the
project's `.venv/bin/python` for checks. In this Codespaces environment, the
system `python3` was Python 3.14.2, while the project environment was Python
3.12.3. `uv`'s default cache path under `/home/codespace/.cache/uv` was
read-only, so setting `UV_CACHE_DIR=/tmp/uv-cache` avoided that local cache
permission failure.

If DNS fails again, stop after recording the specific failure. Do not repeatedly
retry package operations. Existing dependencies and application files were
left untouched by the failed online and offline attempts.
