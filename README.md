# gpio-pmtiles

PMTiles generation plugin for [geoparquet-io](https://github.com/geoparquet/geoparquet-io).

## Installation

```bash
uv tool install geoparquet-io --with gpio-pmtiles
# or
pip install geoparquet-io gpio-pmtiles
```

## Usage

Once installed, the `gpio pmtiles` command becomes available:

```bash
# Convert GeoParquet to PMTiles
gpio pmtiles create input.parquet output.pmtiles

# With custom configuration
gpio pmtiles create input.parquet output.pmtiles \
  --min-zoom 0 \
  --max-zoom 14 \
  --layer-name my_layer
```

## Development

```bash
# Clone and install
git clone https://github.com/geoparquet/gpio-pmtiles.git
cd gpio-pmtiles
uv sync --all-extras

# Run tests
uv run pytest

# Format and lint
uv run ruff format .
uv run ruff check --fix .
```

## How it works

This plugin uses the [entry points system](https://packaging.python.org/en/latest/specifications/entry-points/) to register itself with geoparquet-io. When installed, it automatically adds the `pmtiles` command group to the `gpio` CLI.

## License

Apache 2.0
