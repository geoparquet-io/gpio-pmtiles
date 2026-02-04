# gpio-pmtiles

[![Tests](https://github.com/geoparquet/gpio-pmtiles/actions/workflows/tests.yml/badge.svg)](https://github.com/geoparquet/gpio-pmtiles/actions/workflows/tests.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://github.com/geoparquet/gpio-pmtiles)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/geoparquet/gpio-pmtiles/blob/main/LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

PMTiles generation plugin for [geoparquet-io](https://github.com/geoparquet/geoparquet-io).

## Overview

This plugin provides integrated PMTiles generation from GeoParquet files by orchestrating a streaming pipeline:

```
GeoParquet → [reproject] → [filter] → [convert to GeoJSON] → [tippecanoe] → PMTiles
```

All filtering, reprojection, and conversion happens in-memory through Unix pipes—no intermediate files needed.

**Why use this plugin instead of manual piping?**

- **Simpler API**: Single command handles the entire pipeline with sensible defaults
- **Built-in CRS handling**: Automatically reprojects to WGS84 if needed
- **Better error messages**: Clear guidance for common issues (tippecanoe missing, invalid paths)
- **Quality defaults**: Pre-configured tippecanoe settings for production use

## Installation

```bash
# As a CLI tool
uv tool install geoparquet-io --with gpio-pmtiles

# For Python library use
pip install geoparquet-io gpio-pmtiles
```

**Requirements:**
- [tippecanoe](https://github.com/felt/tippecanoe) must be installed and available in PATH
  - macOS: `brew install tippecanoe`
  - Ubuntu: `sudo apt install tippecanoe`

## Quick Start

```bash
# Basic conversion
gpio pmtiles create buildings.parquet buildings.pmtiles

# With spatial filtering
gpio pmtiles create data.parquet filtered.pmtiles \
  --bbox "-122.5,37.5,-122.0,38.0"

# With attribute filtering and column selection
gpio pmtiles create data.parquet cities.pmtiles \
  --where "population > 10000" \
  --include-cols name,population,area

# With CRS override (if metadata is incorrect)
gpio pmtiles create data.parquet tiles.pmtiles --src-crs EPSG:3857

# From S3 with AWS profile
gpio pmtiles create s3://bucket/data.parquet tiles.pmtiles --profile my-aws-profile
```

## Python API

The plugin also provides a Python API:

```python
from gpio_pmtiles import create_pmtiles_from_geoparquet

# Basic usage
create_pmtiles_from_geoparquet(
    input_path="buildings.parquet",
    output_path="buildings.pmtiles"
)

# With filtering
create_pmtiles_from_geoparquet(
    input_path="data.parquet",
    output_path="tiles.pmtiles",
    bbox="-122.5,37.5,-122.0,38.0",
    where="population > 10000",
    include_cols="name,type,height",
    min_zoom=0,
    max_zoom=14
)

# With CRS override
create_pmtiles_from_geoparquet(
    input_path="data.parquet",
    output_path="tiles.pmtiles",
    src_crs="EPSG:3857"  # Reproject from EPSG:3857 to WGS84
)
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--layer`, `-l` | Layer name in PMTiles (defaults to output filename) |
| `--min-zoom` | Minimum zoom level (use with `--max-zoom` or auto-detect) |
| `--max-zoom` | Maximum zoom level (auto-detected if not specified) |
| `--bbox` | Bounding box filter: `minx,miny,maxx,maxy` |
| `--where` | SQL WHERE clause for filtering rows |
| `--include-cols` | Comma-separated list of columns to include |
| `--precision` | Coordinate decimal precision (default: 6 for ~10cm accuracy) |
| `--src-crs` | Source CRS if metadata is incorrect (will reproject to WGS84) |
| `--attribution` | Attribution HTML for tiles (defaults to geoparquet-io link) |
| `--profile` | AWS profile name for S3 files |
| `--verbose`, `-v` | Show progress and commands being executed |

## How It Works

### Plugin System

This plugin uses the [entry points system](https://packaging.python.org/en/latest/specifications/entry-points/) to register itself with geoparquet-io. When installed, it automatically adds the `pmtiles` command group to the `gpio` CLI.

### Pipeline Architecture

The plugin orchestrates a subprocess pipeline:

1. **Reprojection** (if `--src-crs` specified): `gpio convert reproject`
2. **Filtering** (if bbox/where/include-cols specified): `gpio extract`
3. **GeoJSON conversion**: `gpio convert geojson` with streaming output
4. **Tile generation**: `tippecanoe` with production-quality settings

All stages communicate through Unix pipes for memory efficiency. No intermediate files are created.

### Manual Pipeline Alternative

If you prefer manual control, you can achieve the same result with pipe commands:

```bash
# Plugin version (simple)
gpio pmtiles create data.parquet tiles.pmtiles --bbox "-122,37,-121,38"

# Equivalent manual pipeline
gpio extract data.parquet --bbox "-122,37,-121,38" | \
  gpio convert geojson - | \
  tippecanoe -P -o tiles.pmtiles -zg --simplify-only-low-zooms
```

The plugin provides better defaults and error handling, but manual piping offers more flexibility.

## Coordinate Precision

The `--precision` option controls decimal places for coordinates:

| Precision | Accuracy | Use Case |
|-----------|----------|----------|
| 7 | ~1cm | High accuracy applications |
| 6 (default) | ~10cm | Most mapping use cases |
| 5 | ~1m | City-level visualization |
| 4 | ~10m | Regional maps |

```bash
# Reduce precision for smaller files
gpio pmtiles create data.parquet output.pmtiles --precision 5
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

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines including:
- TDD workflow
- Git conventions
- Code quality standards
- Testing strategy
- Security best practices

## Related Documentation

- **[geoparquet-io Documentation](https://geoparquet.io/)** - Full user guide and API reference
- **[GeoJSON Conversion Guide](https://github.com/geoparquet/geoparquet-io/blob/main/docs/guide/geojson.md)** - Detailed streaming and conversion options
- [tippecanoe documentation](https://github.com/felt/tippecanoe) - Tile generation options
- [PMTiles specification](https://github.com/protomaps/PMTiles) - PMTiles format details

## Contributing

Contributions are welcome! See [CLAUDE.md](CLAUDE.md) for development guidelines including:
- Research-first workflow
- Test-driven development (TDD)
- Git conventions and commit standards
- Code quality and complexity limits
- Security best practices

## Links

- **PyPI**: [https://pypi.org/project/gpio-pmtiles/](https://pypi.org/project/gpio-pmtiles/)
- **Issues**: [https://github.com/geoparquet/gpio-pmtiles/issues](https://github.com/geoparquet/gpio-pmtiles/issues)
- **Parent Project**: [https://github.com/geoparquet/geoparquet-io](https://github.com/geoparquet/geoparquet-io)

## License

Apache 2.0
