"""
Project commands module.

This module provides command-line commands for managing projects within a workspace,
including adding, removing, and setting active projects. The commands are implemented
using Typer for an intuitive CLI interface, and they interact with the `ProjectStore`
and `BoardsStore` classes to handle project data and configurations.

Classes:
    ProjectCmd:
        A command handler for managing projects, allowing for adding,
        removing, and setting active projects, as well as managing configurations.

Functions:
    cb(name: str): Callback for setting the active project when no command is specified.
    add(project: str, config: str): Adds a new project with a specified configuration.
    remove(project: str): Removes an existing project by name.

Dependencies:
    - Typer for command-line interface functionality.
    - ProjectStore, ProjectInstance, and BoardsStore from `nxtool.workspace`.

Usage Example:
    Run `python script_name.py add <project_name> <config>` to add a project,
    or `python script_name.py rm <project_name>` to remove a project.
"""

from typing import Tuple
from typing_extensions import Annotated, Optional

import typer
from nxtool.workspace import ProjectStore, ProjectInstance, BoardsStore

app = typer.Typer()

@app.callback(invoke_without_command=True)
def cb(
    ctx: typer.Context,
    name: Annotated[
        Optional[str],
        typer.Option(
            "--project",
            "-p"
        )
    ] = None
):
    if ctx.invoked_subcommand is None:
        cmd: ProjectCmd = ProjectCmd()
        if name is not None:
            cmd.setprj(name)
        else:
            print(cmd.prj.current)

@app.command(name="add")
def add(
    project: Annotated[
        str,
        typer.Argument()
    ],
    config: Annotated[
        str,
        typer.Argument()
    ]
):
    """
    Add a new project with a specified configuration.

    :param project: The name of the project to add.
    :type project: str
    :param config: The configuration identifier for the project.
    :type config: str
    """
    cmd: ProjectCmd = ProjectCmd()
    cmd.add(project, config)

@app.command(name="rm")
def remove(
    project: Annotated[str, typer.Argument()],
):
    """
    Remove an existing project by name.

    :param project: The name of the project to remove.
    :type project: str
    """
    cmd: ProjectCmd = ProjectCmd()
    cmd.rm(project)

@app.command(name="set")
def setopt(
    opt: Annotated[
        Tuple[str, str],
        typer.Argument()
    ],
):
    cmd: ProjectCmd = ProjectCmd()
    cmd.setopts(opt)

class ProjectCmd():
    '''
    class docstrings
    '''
    def __init__(self):
        """
        Initialize the ProjectCmd instance.

        Sets up project and board stores for handling project data.
        """
        self.brd: BoardsStore = BoardsStore()
        self.prj: ProjectStore = ProjectStore()

    def add(self, project: str, config: str) -> bool:
        """
        Add a new project to the workspace.

        This method adds a new project to the current workspace if it doesn't
        already exist. If `config` is provided, it verifies its validity
        before adding. The store is updated after each addition.

        :param project: The name of the project to add.
        :type project: str
        :param config: The configuration identifier for the project. If `None`,
                       the project is added without configuration.
        :type config: str | None
        :return: `True` if the project was successfully added, `False` if the
                 project already exists or if the specified configuration is invalid.
        :rtype: bool
        """
        if self.prj.search(project) is not None:
            return False

        cfg: tuple[str, str] | None = self.brd.search(config)
        if cfg is not None:
            self.prj.projects.add(ProjectInstance(name=project, config=config))
            self.prj.dump()
            return True

        return False

    def rm(self, project: str) -> bool:
        """
        Remove an existing project from the workspace.

        Checks if the project is the current active project before removal.
        If it is, the removal is aborted. Updates the store if successful.

        :param project: The name of the project to remove.
        :type project: str
        :return: `True` if the project was successfully removed, `False` if
                 the project is active or doesn't exist.
        :rtype: bool
        """
        found: ProjectInstance | None = self.prj.search(project)
        if found is None:
            return False

        # Should handle this better
        if self.prj.current is found.name:
            return False

        self.prj.projects.remove(found)
        self.prj.dump()
        return True

    def setprj(self, project: str) -> bool:
        """
        Set the specified project as the active project.

        Searches for the project in the store and sets it as active if found.

        :param project: The name of the project to set as active.
        :type project: str
        :return: `True` if the project was found and set as active, `False` otherwise.
        :rtype: bool
        """
        project_instance: ProjectInstance | None = self.prj.search(project)

        if project_instance is not None:
            self.prj.current = project_instance
            self.prj.dump()
            return True

        return False

    def setopts(self, opt: Tuple[str, str]) -> bool:
        """
        Unset project options.

        Placeholder for unsetting specific options for the active project.

        :param opt: Option key and value as a tuple.
        :type opt: Tuple[str, str]
        :return: `False` as this is a placeholder method.
        :rtype: bool
        """
        return False

    def unsetopts(self, opt: Tuple[str, str]) -> bool:
        """
        Unset project options.

        Placeholder for unsetting specific options for the active project.

        :param opt: Option key and value as a tuple.
        :type opt: Tuple[str, str]
        :return: `False` as this is a placeholder method.
        :rtype: bool
        """
        return False
