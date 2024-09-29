from enum import Enum, unique
from pathlib import Path
from shutil import rmtree
from typing import Any, Optional, Annotated
import typer
from nxtool.commands.nxcmd import NxCmd
from nxtool.workspace import ProjectStore, BoardsStore, Paths
from nxtool.utils.run_cmd import run_cmake_cmd

app = typer.Typer()

@unique
class Actions(Enum):
    CLEAN = 1

@app.callback(invoke_without_command=True)
def cb(
    name: Annotated[
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
    bld: BuildCmd = BuildCmd(
        name=name,
        config=config,
    )
    bld.run()

class BuildCmd(NxCmd):
    def __init__(self,
                 name: str | None = None,
                 config: str | None = None
                ):
        super().__init__()
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()

        self.name: str = self.prj.current.name
        self.config: str | None = self.prj.current.config
        self.rebuild: bool = self.config is None

        if name is not None and self.prj.search(name) is not None:
            self.name = name

        if config is not None and self.brd.search(config) is not None:
            self.rebuild = self.config == config
            self.config = config

        self.build_path = Paths.nxtool_root / Path(f"build_{self.name}")

        if self.config is None:
            # log error, no config present
            pass

        # Handle makefiles separately
        self.make = self.name == 'make'

    def init(self) -> None:
        """
        Initializes the given project build folder if not present or
        if given config differs from stored config
        """
        self.clean()
        self.build_path.mkdir(parents=True, exist_ok=True)

        #TODO: rewrite this as an cmake wrapper class
        run_cmake_cmd([
            f"-S{Paths.nxtool_root / "nuttx"}",
            f"-B{self.build_path}",
            f"-DBOARD_CONFIG={self.config}"
        ])

    def clean(self) -> None:
        """
        Remove the build folder of the given project
        """
        if self.build_path.exists() and self.build_path.is_dir():
            rmtree(self.build_path)

    def run(self, action: Enum | None = None, args: list[Any] | None = None) -> None:


        if self.rebuild is True:
            self.init()
        run_cmake_cmd([
            "--build",
            f"{self.build_path}"
        ])
