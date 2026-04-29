"""PMTiles generation plugin for geoparquet-io."""

import warnings

from gpio_pmtiles.core import create_pmtiles_from_geoparquet

warnings.warn(
    "gpio-pmtiles is deprecated. PMTiles is now built into geoparquet-io.\n"
    "Use: gpio pmtiles create (CLI) or geoparquet_io.api.ops.create_pmtiles (Python)\n"
    "This package will receive no further updates.",
    DeprecationWarning,
    stacklevel=2,
)

__version__ = "0.2.0"

__all__ = ["create_pmtiles_from_geoparquet"]
