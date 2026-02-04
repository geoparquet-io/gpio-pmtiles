# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Standalone plugin repository with entry points system for geoparquet-io integration
- Plugin verification step in CI tests
- Attribution option to CLI for customizable data attribution in PMTiles output

### Fixed
- Plugin registration for proper geoparquet-io integration
- CI tests to validate standalone plugin functionality
- Tippecanoe flags to use concise syntax for improved clarity

### Changed
- Updated PMTiles generation settings to production tippecanoe configuration
- Installation documentation now recommends pipx for CLI tool installation

### Documentation
- Updated README with new attribution option and usage examples
- Added comprehensive installation and development instructions

## [0.1.0] - Initial Release

### Added
- PMTiles generation plugin for geoparquet-io
- Efficient conversion of GeoParquet files to PMTiles format
- Streaming integration with tippecanoe for optimal performance
- `gpio pmtiles create` command with customizable options:
  - `--min-zoom` and `--max-zoom` for zoom level configuration
  - `--layer-name` for custom layer naming
  - `--attribution` for data attribution
- CLI interface for easy PMTiles generation
- Python API for programmatic usage
- Comprehensive testing and security validation
- Entry points system for automatic plugin registration
- Installation via uv tool and pip package managers

### Documentation
- Complete README with installation and usage instructions
- Development setup guide
- Python API documentation
- Troubleshooting section
- Examples of CLI usage

[Unreleased]: https://github.com/geoparquet/gpio-pmtiles/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/geoparquet/gpio-pmtiles/releases/tag/v0.1.0
