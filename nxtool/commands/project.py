"""
Project commands module.

This module provides command-line commands for managing projects within a workspace,
including adding, removing, and setting active projects.

Classes:
    ProjectCmd:
        Command handler for managing projects and board configurations, 
        providing functionality to add, remove, and manage 
        projects within a workspace.

Functions:
    cb(name: str): Callback, acts as base project command
    add(project: str, config: str): Adds a new project with a specified configuration.
    remove(project: str): Removes an existing project by name.
"""

from nxtool.configuration import BoardsStore, ProjectStore

class ProjectCmd():
    """
    Command handler for managing projects and board configurations.

    The `ProjectCmd` class provides functionality to add, remove, and manage 
    projects within a workspace.
    """
    def __init__(self):
        """
        Initialize the ProjectCmd instance.

        Sets up instances for handling the `BoardsStore` and `ProjectStore`,
        establishing the foundation for managing projects and configurations.
        """
        self.brd: BoardsStore = BoardsStore()
        self.prj: ProjectStore = ProjectStore()

    def __del__(self):
        self.prj.dump()


    def add(self, project: str, config: str) -> bool:
        """
        Add a new project to the workspace.

        This method adds a new project to the current workspace if it doesn't
        already exist. The store is updated after each addition.

        :param str project: The name of the project to add.
        :param str | None config: The configuration identifier for the project.
        :return: `True` if the project was successfully added, `False` otherwise
        :rtype: bool
        """
        if self.prj.search(project) is not None:
            return False

        cfg: tuple[str, str] | None = self.brd.search(config)
        if cfg is not None:
            inst: ProjectInstance = ProjectInstance(name=project, config=config)
            self.prj.projects.add(inst)
            if self.prj.current is None:
                self.prj.current = inst
            return True

        return False

    def rm(self, project: str) -> bool:
        """
        Remove an existing project from the workspace.

        If sucessfully removed, updates the store accordingly.

        :param str project: The name of the project to remove.
        :return: `True` if the project was successfully removed, `False` otherwise
        :rtype: bool
        """
        found: ProjectInstance | None = self.prj.search(project)
        if found is None:
            return False

        if found is self.prj.make:
            return False

        # Should handle this better
        if self.prj.current is found.name:
            return False

        self.prj.projects.remove(found)
        return True

    def setprj(self, project: str) -> bool:
        """
        Set the specified project as the active project.

        Searches for the project in the store and sets it as active if found.

        :param str project: The name of the project to set as active.
        :return: `True` if the project was changes sucessfully, `False` otherwise.
        :rtype: bool
        """
        project_instance: ProjectInstance | None = self.prj.search(project)

        if project_instance is not None:
            self.prj.current = project_instance
            return True

        return False

    def setopts(self, opt: tuple[str, str]) -> bool:
        """
        Unset project options.

        Placeholder for unsetting specific options for the active project.

        :param Tuple[str, str] opt: Option key and value as a tuple.
        :return: `False` as this is a placeholder method.
        :rtype: bool
        """
        return False

    def unsetopts(self, opt: tuple[str, str]) -> bool:
        """
        Unset project options.

        Placeholder for unsetting specific options for the active project.

        :param Tuple[str, str] opt: Option key and value as a tuple.
        :return: `False` as this is a placeholder method.
        :rtype: bool
        """
        return False
