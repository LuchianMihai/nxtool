import importlib.resources
from pathlib import Path
import shutil
import os

from typing_extensions import Annotated

import typer

from nxtool.utils.git import GitWrapper
from nxtool.configuration import ConfigStore, PathsStore

app = typer.Typer()

@app.callback(invoke_without_command=True)
def cb(
    update: Annotated[
        bool,
        typer.Option(
            "--update",
            "-u",
            help="clone default repositories")
    ] = False
):
    """
    sub-command to manage workspace
    """
    cmd: WorkspaceCmd = WorkspaceCmd()

    if update is True:
        cmd.update()
        return

    cmd.init()

class WorkspaceCmd():
    def __init__(self):
        super().__init__()
        if self._check_git() is False:
            print("git executable not found in path. Aborting")
            return

    def _check_git(self) -> bool:
        if shutil.which("git") is not None:
            return True

        return False

    def init(self):
        """
        Run the workspace initialization.
        """

        try:
            os.mkdir(PathsStore.nxtool_dir_name)
            print(f"{PathsStore.nxtool_dir_name} directory created")

        except FileExistsError:
            print("Workspace already initialized. Aborting")

        data = importlib.resources.files("nxtool.data")

        cfg: Path = Path(str(data), "config.toml")
        shutil.copy(str(cfg), PathsStore.nxtool_config)

        prj: Path = Path(str(data), "projects.toml")
        shutil.copy(str(prj), PathsStore.nxtool_projects)

    def update(self):
        cfg: ConfigStore = ConfigStore()

        # git clone https://github.com/apache/nuttx nuttx
        nuttx_repo:GitWrapper = GitWrapper(f'{cfg.nuttx}')
        nuttx_repo.clone()

        # git clone https://github.com/apache/nuttx-apps apps
        apps_repo:GitWrapper = GitWrapper(f'{cfg.apps}')
        apps_repo.clone()
