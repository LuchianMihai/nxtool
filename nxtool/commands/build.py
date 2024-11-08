from pathlib import Path
from typing import Optional, Annotated
import typer
from nxtool.workspace import ProjectStore, BoardsStore, ProjectInstance
from nxtool.configuration import PathsStore
from nxtool.utils.builders import CMakeBuilder, MakeBuilder, Builder

app = typer.Typer()

@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    project: Annotated[
        Optional[str],
        typer.Option(
            "--project",
            "-p",
            help="build specific project")
    ] = None,
    config: Annotated[
        Optional[str],
    typer.Option(
        "-c",
        "--config",
        help="new config for project"
    )] = None
):
    if ctx.invoked_subcommand is None:
        bld: BuildCmd = BuildCmd(project, config)
        bld.build()

class BuildCmd():
    def __init__(self,
                 project: str | None = None,
                 config: str | None = None
                ):

        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()

        # if project option is None, force search function to also return None
        self.inst: ProjectInstance = self.prj.search(project or "") or self.prj.current

        self.rebuild: bool = self.inst.config != config
        if config is not None:
            self.inst.config = config

        dest_path = PathsStore.nxtool_root / Path(f"build_{self.inst.name}")
        src_path = PathsStore.nxtool_root / Path("nuttx")

        if self.inst.name != "make":
            self.builder: Builder = CMakeBuilder(src_path, dest_path)
        else:
            self.builder: Builder = MakeBuilder(src_path, dest_path)

    def build(self) -> None:
        if self.rebuild is True:
            self.builder.configure(self.inst.config)
        self.builder.build()
