import typer
from nxtool.commands import NxCmd
from nxtool.constants import Constants as cst
from nxtool.workspace import ConfigStore, ProjectStore
from typing_extensions import Annotated

import shutil
import os
import sys
import io
import subprocess

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
    init: Init = Init(clone)

    init.run()
    
class Init(NxCmd):
    def __init__(self, 
                 clone: bool = False
                ):
        super().__init__()
        self.clone = clone
        
    def _check_git(self) -> bool:
        ret: bool = False
        
        if shutil.which("git") is not None:
            return True
        
        return ret

    def _run_git_cmd(self, args: list[str]) -> None:
        cmd = ['git'] + args
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, text=True
        ) as proc:
            for line in iter(proc.stdout.readline, ''):
                sys.stdout.write(line)
            stdout, stderr = proc.communicate()
        
    def run(self):
        
        if self._check_git() is False:
            print(f"git executable not found in path. Aborting")
            return
        
        try:
            os.mkdir(cst.NXTOOL_DIR_NAME)
            print(f"{cst.NXTOOL_DIR_NAME} directory created")

            cfg = ConfigStore()
            cfg.dump(f"{cst.NXTOOL_DIR_NAME}/{cst.NXTOOL_CONFIG}")

            prj = ProjectStore()
            prj.dump(f"{cst.NXTOOL_DIR_NAME}/{cst.NXTOOL_PROJECTS}")

        except FileExistsError:
            print(f"Workspace already initialized. Aborting")
        
        if self.clone is True:
            # git clone https://github.com/apache/nuttx nuttx
            self._run_git_cmd(['clone', f'{cfg.nuttx}', 'nuttx'])

            # git clone https://github.com/apache/nuttx-apps apps
            self._run_git_cmd(['clone', f'{cfg.apps}', 'apps'])
        
