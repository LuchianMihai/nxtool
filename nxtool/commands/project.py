"""
Project commands
"""

from enum import Enum, unique
from typing import Any, Optional
from typing_extensions import Annotated

import typer
from nxtool.workspace import ProjectStore, ProjectInstance, BoardsStore

app = typer.Typer()


@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context
      ):
    if ctx.invoked_subcommand is None:
        prj: ProjectCmd = ProjectCmd()


@app.command(name="add")
def add(
    project: Annotated[
        str,
        typer.Argument()
    ],
    config: Annotated[
        Optional[str],
        typer.Argument()
    ] = None
):
    prj: ProjectCmd = ProjectCmd()
    prj.add(project, config)



@app.command(name="rm")
def remove(
    project: Annotated[str, typer.Argument()],
          ):
    prj: ProjectCmd = ProjectCmd()
    prj.rm(project)



class ProjectCmd():
    def __init__(self):
        self.brd: BoardsStore = BoardsStore()
        self.prj: ProjectStore = ProjectStore()

    def add(self, project: str, config: str | None) -> bool:
        if self.prj.search(project) is not None:
            return False

        if config is None:
            self.prj.projects.add(ProjectInstance(name=project))
            self.prj.dump()
            return True

        cfg: tuple[str, str] | None = self.brd.search(config)
        if cfg is not None:
            self.prj.projects.add(
                ProjectInstance(name=project, config=config)
            )
            self.prj.dump()
            return True

        return False

    def rm(self, project: str) -> bool:
        found: ProjectInstance | None = self.prj.search(project)
        if found is None:
            return False

        self.prj.projects.remove(found)
        self.prj.dump()
        return True

    def set(self) -> bool:
        return False

    def unset(self) -> bool:
        return False
