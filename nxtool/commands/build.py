from enum import Enum, unique
import subprocess
import sys
from typing import Any, Optional, Annotated
import typer
from nxtool.commands import NxCmd
from nxtool.workspace import ProjectInstance, ProjectStore

@unique
class Action(Enum):
    ADD = 1

app = typer.Typer()

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
    )] = None,
    args: Annotated[
        Optional[str],
        typer.Option(
            "--",
            help="arguments passed directly to cmake"
        )
    ] = None
):

    print(f"{name} {args}")

    bld: BuildCmd = BuildCmd(
        name=name,
        config=config,
        args=args
    )
    bld.run()

class BuildCmd(NxCmd):
    def __init__(self,
                 name: str | None = None,
                 config: str | None = None,
                 args: str | None = None
                ):
        super().__init__()
        self.prj: ProjectStore = ProjectStore()
        if name is not None:
            # If you intended to write the if statement across multiple lines,
            # you can wrap the expression in parentheses
            self.project_name = (
                name if self.prj.search(name) is not None
                else self.prj.current.name
            )

        if config is not None:
            self.config = config

        self.cmake_agrs = args

    def _check_project(self) -> bool:
        return False

    def _run_cmake_cmd(self, args: list[str]) -> None:
        cmd = ['git'] + args
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, text=True
        ) as proc:
            if proc.stdout:
                for line in iter(proc.stdout.readline, ''):
                    sys.stdout.write(line)
                proc.communicate()

    def run(self, action: Enum | None = None, args: list[Any] | None = None):
        self._run_cmake_cmd(["./nuttx"])

