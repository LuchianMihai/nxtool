import sys
import subprocess

def _run_cmd(args: list[str]) -> None:
    with subprocess.Popen(
        args, stdout=subprocess.PIPE, text=True
    ) as proc:
        if proc.stdout:
            for line in iter(proc.stdout.readline, ''):
                sys.stdout.write(line)
            proc.communicate()

def run_cmake_cmd(args: list[str]) -> None:
    cmd = ['cmake'] + args
    print(f"{cmd}")
    _run_cmd(cmd)

def run_git_cmd(args: list[str]):
    args = ['git'] + args
    _run_cmd(args)