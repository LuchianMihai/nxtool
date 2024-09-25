"""
Main module for nxtool
"""

import typer
from nxtool.commands import init_cmd
from nxtool.commands import project_cmd
from nxtool.commands import list_cmd
from nxtool.commands import build_cmd

from nxtool.workspace import Paths

nxcli = typer.Typer()

nxcli.add_typer(init_cmd, name="init")

nxcli.add_typer(project_cmd, name="project")
nxcli.add_typer(list_cmd, name="list")
nxcli.add_typer(build_cmd, name="build")
@nxcli.command(name="topdir")
def print_topdir() -> None:
    print(f"nxtool workspace root: {Paths.nxtool_root}")
