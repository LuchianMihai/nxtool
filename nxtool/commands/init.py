import shutil
import os
from typing import Any

from enum import Enum
from typing_extensions import Annotated

import typer

from nxtool.utils import run_git_cmd

from nxtool.commands import NxCmd
from nxtool.workspace import Paths
from nxtool.workspace import ConfigStore, ProjectStore


app = typer.Typer()


@app.callback(invoke_without_command=True)
def cb(
    clone: Annotated[
        bool,
        typer.Option(
            "--clone",
            "-c",
            help="clone default repositories")
    ] = False
):

    init: InitCmd = InitCmd(clone)

    init.run()


class InitCmd(NxCmd):
    def __init__(
        self,
        clone: bool = False
                ):
        super().__init__()
        self.clone = clone
        self.cfg: ConfigStore = ConfigStore()
        self.prj: ProjectStore = ProjectStore()

    def _check_git(self) -> bool:
        ret: bool = False

        if shutil.which("git") is not None:
            return True

        return ret

    def run(self, action: Enum | None = None, args: list[Any] | None = None):
        if self._check_git() is False:
            print("git executable not found in path. Aborting")
            return

        try:
            os.mkdir(Paths.nxtool_dir_name)
            print(f"{Paths.nxtool_dir_name} directory created")

            self.cfg.dump()
            self.prj.dump()

        except FileExistsError:
            print("Workspace already initialized. Aborting")

        if self.clone is True:
            # git clone https://github.com/apache/nuttx nuttx
            run_git_cmd(['clone', f'{self.cfg.nuttx}', 'nuttx'])

            # git clone https://github.com/apache/nuttx-apps apps
            run_git_cmd(['clone', f'{self.cfg.apps}', 'apps'])
