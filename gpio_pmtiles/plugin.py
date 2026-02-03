"""Plugin registration for geoparquet-io."""
import click
from gpio_pmtiles.cli import pmtiles


def register_commands(cli_group):
    """Register plugin commands with the main CLI group.

    Args:
        cli_group: The Click group to register commands with
    """
    cli_group.add_command(pmtiles)
