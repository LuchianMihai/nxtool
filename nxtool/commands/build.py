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

class BuildOpt(str, Enum):
    """
    Build command choices
    """
    BUILD = "build"
    CLEANBUILD = "clean-build"
    CONFIG = "config"
    CLEAN = "clean"
    FULLCLEAN = "full-clean"

@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    project: Annotated[
        Optional[str],
        typer.Option(
            "--project",
            "-p",
            help="Select project"
        )
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--config",
            "-c",
            help="Select configuration"
        )
    ] = None,
    tool: Annotated[
        Optional[str],
        typer.Option(
            "--tool",
            "-t",
            help="Select configuration"
        )
    ] = None,
    opt: Annotated[
        BuildOpt,
        typer.Argument(
            help="Select configuration"
        )
    ] = BuildOpt.BUILD
):
    """
    sub-command to interact with nuttx build systems
    """
    if ctx.invoked_subcommand is None:
        if tool is not None and project is not None:
            typer.echo(
                "[ERROR] -t/--tool and -p/--project are mutualy exclusive",
                err=True
            )
            raise typer.Exit(code=1)
        cmd: BuildCmd = BuildCmd(project, config)
        cmd.run(opt)

class BuildCmd():
    """
    Command handler for interacting with nuttx's build systems.

    The `BuildCmd` class provides functionality to configure, build, clean 
    projects within a workspace.
    """
    def __init__(self,
                 project: str | None = None,
                 config: str | None = None,
    ):
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()

        # if project option is None, force search function to also return None
        self.inst: ProjectInstance = self.prj.search(project or "") or self.prj.current

        if config is not None and self.brd.search(config) is not None:
            self.inst.config = config

        dest_path = PathsStore.nxtool_root / Path(f"build_{self.inst.name}")
        src_path = PathsStore.nxtool_root / Path("nuttx")

        if self.inst != self.prj.make:
            self.builder: Builder = CMakeBuilder(src_path, dest_path)
        else:
            self.builder: Builder = MakeBuilder(src_path, dest_path)

    def __del__(self):
        self.prj.current = self.inst
        self.prj.dump()

    def run(self, opt: BuildOpt) -> None:
        """
        """
        print(f"executing {opt.value}")
        match opt:
            case BuildOpt.CONFIG:
                self.builder.configure(self.inst.config)
            case BuildOpt.CLEANBUILD:
                self.builder.clean()
                self.builder.build()
            case BuildOpt.BUILD:
                self.builder.build()
            case BuildOpt.CLEAN:
                self.builder.clean()
            case BuildOpt.FULLCLEAN:
                self.builder.fullclean()
