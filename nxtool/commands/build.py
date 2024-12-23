"""
Build commands module.

This module provides command-line commands for interacting with nuttx's build systems,
providing functionality to configure, build, clean projects within a workspace.

Classes:
    BuildCmd:
        Command handler for managing configuration, building, cleaning 
        projects within a workspace.

Functions:
    cb(name: str): Callback, acts as base build command
"""
from enum import Enum
from pathlib import Path
from typing import Optional, Annotated
import typer
from nxtool.configuration import PathsStore, ProjectStore, BoardsStore, ProjectInstance
from nxtool.utils.builders import CMakeBuilder, MakeBuilder, Builder

app = typer.Typer()

@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    reconfig: Annotated[
        bool,
        typer.Option(
            "--reconfig",
            "-r",
            help="rerun configuration"
        )
    ] = False,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--config",
            "-c",
            help="change project configuration"
        )
    ] = None,
    tool: Annotated[
        Optional[str],
        typer.Option(
            "--tool",
            "-t",
            help="select tool for building"
        )
    ] = None,
):
    """
    sub-command to interact with nuttx build systems
    """
    if ctx.invoked_subcommand is None:
        cfg = config
        cmd: BuildCmd = BuildCmd()
        if config is not None:
            cmd.config(config)
            return
        if reconfig is True:
            cmd.config()
            return
        cmd.build()

class BuildCmd():
    """
    Command handler for interacting with nuttx's cmake build system.

    The `BuildCmd` class provides functionality to configure, build, clean 
    cmake projects in a workspace.
    """
    def __init__(self):
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()
        self.inst: ProjectInstance = self.prj.current

        dest_path = PathsStore.nxtool_root / Path(f"build_{self.inst.name}")
        src_path = PathsStore.nxtool_root / Path("nuttx")

        self.builder: Builder = CMakeBuilder(src_path, dest_path)

    def __del__(self):
        self.prj.current = self.inst
        self.prj.dump()
    
    def config(self, opt: str | None) -> None:
        """
        run project configuration
        """
        if config is None and self.brd.search(config) is not None:
            self.inst.config = config
        self.builder.configure(self.inst.config)

    def build(self) -> None:
        """
        run project build
        """
        self.builder.build()

    def clean(self, full: bool = False) -> None:
        """
        run project full clean
        """
        if full is True:
            self.builder.fullclean()
            return

        self.builder.clean()

