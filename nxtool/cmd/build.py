"""
Build commands module.

This module provides command-line commands for interacting with nuttx's build systems,
providing functionality to configure, build, clean projects within a workspace.

Classes:
    BuildCmd:
        Command handler for managing configuration, building, cleaning 
        projects within a workspace.
"""
from pathlib import Path
from nxtool.config.configuration import PathsStore, ProjectStore, BoardsStore, ProjectInstance
from nxtool.utils.builders import CMakeBuilder, Builder

class BuildCmd():
    """
    Command handler for interacting with nuttx's cmake build system.

    The `BuildCmd` class provides functionality to configure, build, clean 
    cmake projects in a workspace.
    """
    def __init__(self):
        self.prj: ProjectStore = ProjectStore()

        if self.prj.current is None:
            raise RuntimeError("No projects present, current project is None")

        self.brd: BoardsStore = BoardsStore()
        self.inst: ProjectInstance = self.prj.current

        dest_path = PathsStore.nxtool_root / Path(f"build_{self.inst.name}")
        src_path = PathsStore.nxtool_root / Path("nuttx")

        self.builder: Builder = CMakeBuilder(src_path, dest_path)

    def __del__(self):
        if hasattr(self, "inst") is True:
            self.prj.current = self.inst
            self.prj.dump()
    
    def config(self, config: str | None = None) -> None:
        """
        run project configuration
        """
        if config is not None and self.brd.search(config) is not None:
            self.inst.config = config
        self.builder.configure(self.inst.config)

    def build(self) -> None:
        """
        run project build
        """
        self.builder.build()

    def clean(self, full: bool = False) -> None:
        """
        run project full clean
        """
        self.builder.clean() if full is False else self.builder.fullclean()

