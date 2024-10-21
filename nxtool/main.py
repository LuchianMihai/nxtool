"""
Main module for nxtool
"""
from pathlib import Path

import typer

from nxtool.commands import *

from nxtool.configuration import PathsStore, ConfigStore
from nxtool.utils.topdir import topdir


class NxApp():
    def __init__(self) -> None:
        self.nxcli: typer.Typer = typer.Typer()
        self.config: ConfigStore = ConfigStore()

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

        self._configure_cli()

    def _configure_cli(self):
        self.nxcli.add_typer(init_cmd, name="init")
        self.nxcli.add_typer(project_cmd, name="prj")

    def start(self):
        self.nxcli()
