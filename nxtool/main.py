"""
Main module for nxtool
"""
from pathlib import Path

import typer

from nxtool.commands import * # pylint: disable=W0401

from nxtool.configuration import PathsStore
from nxtool.utils.topdir import topdir
from nxtool.typer_commands import configure_cli


class NxApp():
    def __init__(self) -> None:
        self.nxcli: typer.Typer = typer.Typer()

        # Init PathsStore data attributes to correct values
        try:
            PathsStore.nxtool_dir_name = Path(".nxtool")
            nxroot: Path = topdir(PathsStore.nxtool_dir_name)
        except FileNotFoundError:
            print("Workspace root not found")
            PathsStore.nxtool_root = Path(".")
        else:
            PathsStore.nxtool_root = nxroot

        PathsStore.nxtool_config = (
            PathsStore.nxtool_root / PathsStore.nxtool_dir_name / "config.toml"
        )
        PathsStore.nxtool_projects = (
            PathsStore.nxtool_root / PathsStore.nxtool_dir_name / "projects.toml"
        )
        PathsStore.nxtool_build_dir = (
            PathsStore.nxtool_root / PathsStore.nxtool_dir_name / "build"
        )
        PathsStore.nxtool_bin_dir = (
            PathsStore.nxtool_root / PathsStore.nxtool_dir_name / "bin"
        )

        self._configure_cli()
        configure_cli(self.nxcli)


    def _configure_cli(self):
        self.nxcli.add_typer(build_cmd, name="build")

    def start(self):
        self.nxcli()
