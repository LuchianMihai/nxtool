import sys
import subprocess

class GitWrapper():
    def __init__(
        self,
        repo: str
    ) -> None:
        self.repo = repo

    def _run_git_cmd(self, args: list[str]) -> None:
        cmd = ['git'] + args
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, text=True
        ) as proc:
            if proc.stdout:
                for line in iter(proc.stdout.readline, ''):
                    sys.stdout.write(line)
                proc.communicate()

    def clone(self):
        self._run_git_cmd(['clone', self.repo])
