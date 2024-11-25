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
from pathlib import Path
from typing import Optional, Annotated, Union
import typer
from nxtool.workspace import ProjectStore, BoardsStore, ProjectInstance
from nxtool.configuration import PathsStore
from nxtool.utils.builders import CMakeBuilder, MakeBuilder, Builder

app = typer.Typer()

def _config_cb(param: typer.CallbackParam, cfg: str | None):
    print(f"Validating param: {param.name}")
    return cfg or '.'

@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    project: Annotated[
        Optional[str],
        typer.Option(
            "--project",
            "-p",
            help="Build specific project"
        )
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--configure",
            "-c",
            callback=lambda a: a or ".",
            is_flag=False
        )
    ] = None
):
    """
    sub-command to interact with nuttx build systems
    """
    print(f"{ctx.args}")
    if ctx.invoked_subcommand is None:
        cmd: BuildCmd = BuildCmd(project)
        if config is not None:
            cmd.configure(config)
        else:
            cmd.build()

class BuildCmd():
    """
    Command handler for interacting with nuttx's build systems.

    The `BuildCmd` class provides functionality to configure, build, clean 
    projects within a workspace.
    """
    def __init__(self,
                 project: str | None = None,
    ):
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()

        # if project option is None, force search function to also return None
        self.inst: ProjectInstance = self.prj.search(project or "") or self.prj.current

        dest_path = PathsStore.nxtool_root / Path(f"build_{self.inst.name}")
        src_path = PathsStore.nxtool_root / Path("nuttx")

        if self.inst != self.prj.make:
            self.builder: Builder = CMakeBuilder(src_path, dest_path)
        else:
            self.builder: Builder = MakeBuilder(src_path, dest_path)

    def __del__(self):
        self.prj.current = self.inst
        self.prj.dump()

    def configure(
        self,
        config: str
    ) -> bool:

        if config == '.':
            self.builder.configure(self.inst.config)
            return True

        if self.brd.search(config) is not None:
            self.inst.config = config
            self.builder.configure(self.inst.config)
            return True

        return False

    def build(self) -> None:
        """
        """
        self.builder.build()
