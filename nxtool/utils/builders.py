"""
Wrappers over build tools. For the moment only cmake and make are supported
"""

from abc import ABC, abstractmethod
from pathlib import Path
from shutil import rmtree

from nxtool.utils.run_cmd import run_cmake_cmd

class Builder(ABC):
    def __init__(
        self,
        source: Path,
        destination: Path
    ) -> None:
        self.source = source
        self.destination = destination


    @abstractmethod
    def configure(self, config: str):
        pass

    @abstractmethod
    def build(self, target: str = "all"):
        pass

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def clean(self):
        pass

    def fullclean(self):
        if self.destination.exists() and self.destination.is_dir():
            rmtree(self.destination)

class MakeBuilder(Builder):
    """
    Wrapper class over make build system.
    Should be assumed that any arguments given here are already checked and valid
    """

    def __init__(
        self,
        source: Path,
        destination: Path
    ) -> None:
        super().__init__(
            source=source,
            destination=destination
        )

    def configure(self, config: str):
        """
        equivalent to ./tools/configure.sh
        """

    def build(self, target: str = "all"):
        "run builder"

    def install(self):
        "install target"

    def clean(self):
        "clean configuration"

class CMakeBuilder(Builder):
    def __init__(
        self,
        source: Path,
        destination: Path
    ) -> None:
        super().__init__(
            source=source,
            destination=destination
        )

    def configure(self, config: str, btype: str = "Debug", generator: str = "Ninja"):
        """
        Configure cmake project
        """

        run_cmake_cmd([
            f"-S {self.source}",
            f"-B {self.destination}",
            f"-G {generator}",

            f"-DBOARD_CONFIG={config}",
            f"-DCMAKE_BUILD_TYPE={btype}"
        ])

    def build(self, target: str = "all"):

        run_cmake_cmd([
            "--build",
            f"{self.destination}"
        ])

    def install(self, directory: str | None = None):
        pass

    def clean(self):
        "clean configuration"
