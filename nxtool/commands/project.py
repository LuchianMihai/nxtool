"""
Project commands
"""

from enum import Enum, unique

from typing_extensions import Annotated

import typer
from nxtool.commands import NxCmd
from nxtool.workspace import ProjectStore, ProjectInstance


@unique
class Action(Enum):
    ADD = 1


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
    name: Annotated[list[str], typer.Argument()]
       ):
    prj: ProjectCmd = ProjectCmd()
    prj.run(Action.ADD, name)


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

    def _add(self, args: list[str]):
        print(f"adding {args}")
        self.prj.projects.append(
                ProjectInstance(
                    name=args[0],
                    board=args[1],
                    config=args[2]
                )
        )
        self.prj.dump()

    def _rm(self):
        pass

    def run(self, action: Enum | None = None, args: list[str] | None = None):
        if action is not None:
            match action:
                case Action.ADD:
                    if args is not None:
                        self._add(args)
        else:
            if self.status is True:
                self._list_projects()
