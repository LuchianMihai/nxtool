import shutil
import os

from typing_extensions import Annotated

import typer

from nxtool.utils.git import GitWrapper

from nxtool.workspace import ProjectStore
from nxtool.configuration import ConfigStore, PathsStore

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

class InitCmd():
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

    def run(self):
        """
        Run the workspace initialization.
        If -c flag is set, default repositories are also cloned
        """
        if self._check_git() is False:
            print("git executable not found in path. Aborting")
            return

        try:
            os.mkdir(PathsStore.nxtool_dir_name)
            print(f"{PathsStore.nxtool_dir_name} directory created")

            self.cfg.dump()
            self.prj.dump()

        except FileExistsError:
            print("Workspace already initialized. Aborting")

        if self.clone is True:
            # git clone https://github.com/apache/nuttx nuttx
            nuttx_repo:GitWrapper = GitWrapper(f'{self.cfg.nuttx}')
            nuttx_repo.clone()

            # git clone https://github.com/apache/nuttx-apps apps
            apps_repo:GitWrapper = GitWrapper(f'{self.cfg.apps}')
            apps_repo.clone()
