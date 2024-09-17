"""
Project commands
"""

from enum import Enum, unique
from typing import Any, Optional

from typing_extensions import Annotated

import typer
from nxtool.commands import NxCmd
from nxtool.workspace import ProjectStore, ProjectInstance


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
    board: Annotated[
        Optional[str],
        typer.Option(
            "--board",
            "-b"
        )
    ] = None,
    config: Annotated[
        Optional[str],
        typer.Option(
            "--config",
            "-c"
        )
    ] = None
       ):
    prj: ProjectCmd = ProjectCmd()
    args: list[Any] = [name, board, config]

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
                ):
        super().__init__()
        self.status: bool = status

        self.prj = ProjectStore()
        self.prj.load()

    def _list_projects(self):
        print("========")
        print(f"working on {self.prj.current.name} project")

        if self.prj.current.board is not None:
            print("board is set to '{self.prj.current.board}'")
        else:
            print("board currently not set")

        if self.prj.current.config is not None:
            print(f"config is set to '{self.prj.current.config}'")
        else:
            print("config currently not set")
            print("========")
            print("other projects")

            for p in self.prj.projects:
                print(f"name: {p.name}, board: {p.board}, config: {p.config}")
                print("--------")

    def _add(self, name: str, board: str | None, config: str | None):
        print(f"adding {name} {board} {config}")
        found: list[ProjectInstance] = [
            p for p in self.prj.projects if p.name == name
        ]
        if not found:
            self.prj.projects.append(
                ProjectInstance(name=name, board=board, config=config)
            )
            self.prj.dump()

    def _rm(self, name: str):
        found: list[ProjectInstance] = [
            p for p in self.prj.projects if p.name == name
        ]
        if found:
            self.prj.projects.remove(found[0])
            self.prj.dump()

    def run(self, action: Enum | None = None, args: list[Any] | None = None):
        if action is not None:
            match action:
                case Action.ADD:
                    if args is not None:
                        self._add(args[0], args[1], args[2])
                case Action.REMOVE:
                    if args is not None:
                        self._rm(args[0])
        else:
            if self.status is True:
                self._list_projects()
