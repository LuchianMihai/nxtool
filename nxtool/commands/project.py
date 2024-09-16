
from enum import Enum, unique
import typer
from nxtool.commands import NxCmd
from nxtool.constants import Constants as cst
from nxtool.workspace import ProjectStore, ProjectInstance
from typing_extensions import Annotated

@unique
class Action(Enum):
    ADD = 1

app = typer.Typer()

@app.callback(invoke_without_command=True)
def cb(ctx: typer.Context
    ):
    if ctx.invoked_subcommand is None:
        prj: ProjectCmd = ProjectCmd(status=True)
        prj.run()
    
@app.command(name="add") 
def add(
        name: Annotated[str, typer.Argument()]
    ):
    prj: ProjectCmd = ProjectCmd(name=name)
    prj.run(Action.ADD)

class ProjectCmd(NxCmd):
    def __init__(self,
                 status: bool = False,
                 name: str = None):
        super().__init__()
        self.status = status
        self.name = name

        self.prj = ProjectStore()
        self.prj.load(f"{cst.NXTOOL_DIR_NAME}/{cst.NXTOOL_PROJECTS}")

    def _list_projects(self):
        print(f"========")
        print(f"working on {self.prj.current.name} project")

        if self.prj.current.board is not None:
            print(f"board is set to '{self.prj.current.board}'")
        else:
            print(f"board currently not set")

        if self.prj.current.config is not None:
            print(f"config is set to '{self.prj.current.config}'")
        else:
            print(f"config currently not set")
            print(f"========")
            print(f"other projects")

            for p in self.prj.projects:
                print(f"name: {p.name}, board: {p.board}, config: {p.config}")
                print(f"--------")

    def _add(self):
        print(f"adding {self.name}")
        self.prj.projects.append(ProjectInstance(name=self.name))
        self.prj.dump(f"{cst.NXTOOL_DIR_NAME}/{cst.NXTOOL_PROJECTS}")


    def run(self, action: Enum = None):
        if action is not None:
            match action:
                case Action.ADD:
                    self._add()
            pass
        else:
            if self.status is True:
                self._list_projects()


