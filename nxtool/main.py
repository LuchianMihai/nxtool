import typer
from nxtool.commands.build import app as nx_build
from nxtool.commands.init import app as nx_init

nxcli = typer.Typer()

nxcli.add_typer(nx_build, name="build")
nxcli.add_typer(nx_init, name="init")
