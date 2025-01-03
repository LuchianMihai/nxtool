from typing_extensions import Annotated

import typer

from nxtool.config.configuration import *
from nxtool.cmd.info import InfoCmd
from nxtool.cmd.project import ProjectCmd
from nxtool.cmd.workspace import WorkspaceCmd
from nxtool.cmd.build import BuildCmd

build = typer.Typer()

@build.callback(invoke_without_command=True)
def build_cb(
    ctx: typer.Context,
    reconfig: Annotated[
        bool,
        typer.Option(
            "--reconfig",
            "-r",
            help="rerun configuration"
        )
    ] = False
):
    """
    sub-command to interact with nuttx build systems
    """
    if ctx.invoked_subcommand is None:
        try:
            build: BuildCmd = BuildCmd()
            if reconfig is True:
                build.config()
                return
            build.build()
        except RuntimeError as e:
            print(e)

@build.command(name="change")
def change(
    config: Annotated[
        str,
        typer.Argument()
    ],
) -> None:
    build: BuildCmd = BuildCmd()
    build.config(config)

workspace = typer.Typer()

@workspace.callback(invoke_without_command=True)
def workspace_cb(
    ctx: typer.Context,
):
    """
    sub-command to manage workspace
    """
    if ctx.invoked_subcommand is None:
        # workspace: WorkspaceCmd = WorkspaceCmd()
        pass

@workspace.command(name="init")
def init() -> None:
    cmd: WorkspaceCmd = WorkspaceCmd()
    cmd.init()

@workspace.command(name="update")
def update() -> None:
    cmd: WorkspaceCmd = WorkspaceCmd()
    cmd.update()

info = typer.Typer()

@info.callback()
def info_cb():
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

project = typer.Typer()

@project.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context
):
    """
    sub-command to manage projects
    """
    if ctx.invoked_subcommand is None:
        cmd: ProjectCmd = ProjectCmd()
        print(cmd.prj.current)

@project.command(name="switch")
def switch(
    project: Annotated[
        str,
        typer.Argument()
    ],
):
    cmd: ProjectCmd = ProjectCmd()
    cmd.set_project(project)

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
        cmd.set_project(project)

@project.command(name="rm")
def remove(
    name: Annotated[
        str,
        typer.Argument()
    ],
):
    """
    Remove an existing project by name.
    """
    project: ProjectCmd = ProjectCmd()
    project.remove(name)

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

def configure_typer(cli: typer.Typer) -> None:
    cli.add_typer(workspace, name="workspace")
    cli.add_typer(info, name="info")
    cli.add_typer(project, name="project")
    cli.add_typer(build, name="build")

    @cli.command(name="topdir")
    def show_topdir() -> None:
        print(f"workspace topdir: {PathsStore.nxtool_root}")
    
