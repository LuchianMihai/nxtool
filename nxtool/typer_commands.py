from typing_extensions import Annotated, Optional

import typer

from nxtool.configuration import *
from nxtool.utils.git import GitWrapper
from nxtool.commands.info import InfoCmd
from nxtool.commands.project import ProjectCmd
from nxtool.commands.workspace import WorkspaceCmd

info = typer.Typer()
project = typer.Typer()
workspace = typer.Typer()

@workspace.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
):
    """
    sub-command to manage workspace
    """
    if ctx.invoked_subcommand is None:
        cmd: WorkspaceCmd = WorkspaceCmd()

@workspace.command(name="init")
def init():
    cmd: WorkspaceCmd = WorkspaceCmd()
    cmd.init()

@workspace.command(name="update")
def update():
    cmd: WorkspaceCmd = WorkspaceCmd()
    cmd.update()

@info.callback()
def cb():
    """
    sub-command to show workspace and projects info
    """

@info.command(name="boards")
def list_boards():
    """
    list all boards and configurations
    """
    prj: InfoCmd = InfoCmd()
    prj.boards()

@info.command(name="projects")
def list_projectst():
    """
    list all workspace projects
    """
    prj: InfoCmd = InfoCmd()
    prj.projects()

@info.command(name="project")
def list_current_project():
    """
    list current project
    """
    prj: InfoCmd = InfoCmd()
    prj.project()

@info.command(name="tools")
def list_tools():
    """
    list nuttx tools
    """
    prj: InfoCmd = InfoCmd()
    prj.tools()

@project.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    change: Annotated[
        Optional[str],
        typer.Option(
            "--change",
            "-c"
        )
    ] = None
):
    """
    sub-command to manage projects
    """
    if ctx.invoked_subcommand is None:
        cmd: ProjectCmd = ProjectCmd()
        print(cmd.prj.current)

@project.command(name="change")
def change(
    project: Annotated[
        str,
        typer.Argument()
    ],
):
    cmd: ProjectCmd = ProjectCmd()
    cmd.setprj(project)

@project.command(name="add")
def add(
    project: Annotated[
        str,
        typer.Argument()
    ],
    config: Annotated[
        str,
        typer.Argument()
    ],
    change: Annotated[
        bool,
        typer.Option(
            "--change",
            "-c",
            help="Change current project"
        )
    ] = False,
):
    """
    Add a new project with a specified configuration.
    """
    cmd: ProjectCmd = ProjectCmd()
    cmd.add(project, config)

    if change is True:
        cmd.setprj(project)

@project.command(name="rm")
def remove(
    project: Annotated[
        str,
        typer.Argument()
    ],
):
    """
    Remove an existing project by name.
    """
    cmd: ProjectCmd = ProjectCmd()
    cmd.rm(project)

@project.command(name="set")
def setopt(
    opt: Annotated[
        tuple[str, str],
        typer.Argument()
    ],
):
    """
    Set optional project configuration parameters
    """
    cmd: ProjectCmd = ProjectCmd()
    cmd.setopts(opt)

def configure_cli(cli: typer.Typer) -> None:
    cli.add_typer(workspace, name="workspace")
    cli.add_typer(info, name="info")
    cli.add_typer(project, name="project")
    
