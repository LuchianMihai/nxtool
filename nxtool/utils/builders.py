"""
Wrappers over build tools. For the moment only cmake and make are supported
"""

import sys
import subprocess

from abc import ABC, abstractmethod
from pathlib import Path
from shutil import rmtree

from nxtool.config.configuration import PathsStore

class Builder(ABC):
    """
    Abstract base class for a builder responsible for configuring, building,
    installing, and cleaning build processes for a specified source and
    destination.

    Attributes:
        source (Path): Path to the source directory for the build.
        destination (Path): Path to the destination directory for build outputs.
    """

    def __init__(self, source: Path, destination: Path) -> None:
        """
        Initialize the Builder with a source and destination path.

        :param source: Path to the source directory for the build.
        :type source: Path
        :param destination: Path to the destination directory for build outputs.
        :type destination: Path
        """
        self.source = source
        self.destination = destination

    @abstractmethod
    def configure(self, config: str):
        """
        Configure the build environment based on the provided configuration.

        :param config: Configuration settings for the build environment.
        :type config: str
        """

    @abstractmethod
    def build(self, target: str = "all"):
        """
        Execute the build process for the specified target.

        :param target: The build target to compile. Defaults to "all".
        :type target: str
        """

    @abstractmethod
    def install(self):
        """
        Install the built files to the designated destination.
        """

    @abstractmethod
    def clean(self):
        """
        Clean intermediate build files without removing the entire output.
        """

    def fullclean(self):
        """
        Remove the entire output directory, including all built files.
        """
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

    def _run_make_cmd(self, args: list[str]) -> None:
        cmd = [
            "make",
            "-C",
            f"{PathsStore.nxtool_root}/nuttx"
        ] + args
        self._run_cmd(cmd)

    def _run_cmd(self, args: list[str]) -> None:
        with subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
        ) as proc:
            if proc.stdout:
                for line in iter(proc.stdout.readline, ''):
                    print(line)
                proc.communicate()

    def configure(self, config: str):
        """
        equivalent to ./tools/configure.sh
        """
        self._run_cmd([
            f"{PathsStore.nxtool_root}/nuttx/tools/configure.sh",
            f"{config}"
        ])

    def build(self, target: str = "all"):
        "run builder"
        self._run_make_cmd([])

    def install(self):
        "install target"

    def clean(self):
        "clean configuration"
        self._run_make_cmd(["distclean"])

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

    def _run_cmake_cmd(self, args: list[str]) -> None:
        cmd = [
            "cmake",
            ] + args
        print(cmd)
        with subprocess.Popen(
            cmd, stdout=subprocess.PIPE, text=True
        ) as proc:
            if proc.stdout:
                for line in iter(proc.stdout.readline, ''):
                    sys.stdout.write(line)
                proc.communicate()

    def configure(self, config: str, btype: str = "Debug", generator: str = "Ninja"):
        """
        Configure cmake project
        """

        self._run_cmake_cmd([
            "-S", f"{self.source}",
            "-B", f"{self.destination}",
            "-G", f"{generator}",
            "-D", f"BOARD_CONFIG={config}",
            "-D", f"CMAKE_BUILD_TYPE={btype}"
        ])

    def build(self, target: str = "all"):
        """
        build project
        """
        self._run_cmake_cmd([
            "--build", f"{self.destination}",
            "--target", f"{target}",
        ])

    def install(self, directory: str | None = None):
        pass

    def clean(self):
        "clean project"
        self._run_cmake_cmd([
            "--build", f"{self.destination}",
            "--target", "clean"
        ])
