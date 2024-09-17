"""
Main module for nxtool
"""


import typer
from nxtool.commands import init
from nxtool.commands import project

nxcli = typer.Typer()

nxcli.add_typer(init, name="init")
nxcli.add_typer(project, name="project")
