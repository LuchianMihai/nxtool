import importlib.resources
from pathlib import Path
import shutil
import os

from nxtool.config.configuration import ConfigStore, PathsStore
from nxtool.utils.git import GitWrapper

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

            data: Path = importlib.resources.files("nxtool.data")

            cfg: Path = Path(str(data), "config.toml")
            shutil.copy(cfg, PathsStore.nxtool_config)

            prj: Path = Path(str(data), "projects.toml")
            shutil.copy(str(prj), PathsStore.nxtool_projects)

        except FileExistsError:
            print("Workspace already initialized. Aborting")

    def update(self):
        cfg: ConfigStore = ConfigStore()

        for remote in cfg.remotes:
            repo:GitWrapper = GitWrapper(remote[1])
            repo.clone(remote[0])
