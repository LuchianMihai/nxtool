"""
Project commands
"""

from enum import Enum, unique
from typing import Any, Optional
from typing_extensions import Annotated

import typer
from nxtool.commands import NxCmd
from nxtool.workspace import ProjectStore, ProjectInstance, BoardsStore, Paths
from nxtool.utils import run_cmake_cmd


@unique
class Action(Enum):
    ADD = 1
    REMOVE = 2


app = typer.Typer()


@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context
      ):
    if ctx.invoked_subcommand is None:
        prj: ProjectCmd = ProjectCmd(status=True)
        prj.run()


@app.command(name="add")
def add(
    name: Annotated[str, typer.Argument()],
    config: Annotated[
        Optional[str],
        typer.Argument()
    ] = None,

    init: Annotated[
        bool,
        typer.Option(
            "--init",
            "-i",
            help="also initialize the project. run cmake"
        )
    ] = False
       ):
    prj: ProjectCmd = ProjectCmd(init=init)
    args: list[Any] = [name, config]

    prj.run(Action.ADD, args)


@app.command(name="rm")
def remove(
    name: Annotated[str, typer.Argument()],
          ):
    prj: ProjectCmd = ProjectCmd()
    args: list[Any] = [name]

    prj.run(Action.REMOVE, args)


class ProjectCmd(NxCmd):
    def __init__(self,
                 status: bool = False,
                 init: bool = False,
                ):
        super().__init__()
        self.status: bool = status
        self.init: bool = init

        self.brd: BoardsStore = BoardsStore()

        self.prj: ProjectStore = ProjectStore()
        self.prj.load()

    def _list_projects(self):
        print("========")
        print(f"working on {self.prj.current.name} project")

        if self.prj.current.config is not None:
            print(f"board is set to '{self.prj.current.config}'")
        else:
            print("board currently not set")

        print("========")
        print("other projects")

        for p in self.prj.projects:
            print(f"name: {p.name}, config: {p.config}")
            print("--------")

    def _add(self, name: str, config: str | None) -> bool:
        if self.prj.search(name) is not None:
            return False

        if config is None:
            self.prj.projects.add(ProjectInstance(name=name))
            self.prj.dump()
            return True

        cfg: tuple[str, str] | None = self.brd.search(config)
        if cfg is not None:
            self.prj.projects.add(
                ProjectInstance(name=name, config=config)
            )
            self.prj.dump()
            return True

        return False

    def _rm(self, name: str):
        found: ProjectInstance | None = self.prj.search(name)
        if found is not None:
            self.prj.projects.remove(found)
            self.prj.dump()

    def run(self, action: Enum | None = None, args: list[Any] | None = None):
        if action is not None:
            match action:
                case Action.ADD:
                    if args is not None:
                        self._add(args[0], args[1])
                        if self.init is True:
                            pass
                case Action.REMOVE:
                    if args is not None:
                        self._rm(args[0])
        else:
            if self.status is True:
                self._list_projects()
