from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar
import toml



@dataclass()
class PathsStore():
    """
    A class to store and manage various paths used throughout the project.

    :ivar nxtool_dir_name: The directory name for nxtool (default: ".nxtool").
    :vartype nxtool_dir_name: Path
    :ivar nxtool_root: The root directory for nxtool,
        determined by the `topdir` function.
    :vartype nxtool_root: Path
    :ivar nxtool_config: The path to the nxtool configuration file (`config.toml`).
    :vartype nxtool_config: Path
    :ivar nxtool_projects: The path to the nxtool projects file (`projects.toml`).
    :vartype nxtool_projects: Path

    This class organisez/manages the paths throughout the project.
    - It holds only class attributes so there's no need for dependency injection pattern
    - It is initialized in main.py
    """
    nxtool_dir_name: ClassVar[Path] = Path()
    nxtool_root: ClassVar[Path] = Path()
    nxtool_config: ClassVar[Path] = Path()
    nxtool_projects: ClassVar[Path] = Path()

@dataclass
class ConfigStore():
    """
    Config class that stores data from .nxtool/config.

    :ivar nuttx: URL for the NuttX repository.
    :vartype nuttx: str
    :ivar apps: URL for the NuttX apps repository.
    :vartype apps: str
    """

    nuttx: str = "https://github.com/apache/nuttx"
    apps: str = "https://github.com/apache/nuttx-apps"

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["remotes"] = {}
        pack["remotes"]["nuttx"] = self.nuttx
        pack["remotes"]["apps"] = self.apps
        return pack

    def load(self) -> None:
        try:
            with open(PathsStore.nxtool_config, 'r', encoding='utf-8') as file:
                data: dict = toml.load(file)
                self.nuttx = data["remotes"]["nuttx"]
                self.apps = data["remotes"]["apps"]
        except FileNotFoundError:
            print(f"Error: File '{PathsStore.nxtool_config}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{PathsStore.nxtool_config}' contains invalid JSON.")
            return

    def dump(self) -> None:
        try:
            with open(PathsStore.nxtool_config, 'w', encoding='utf-8') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{PathsStore.nxtool_config}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{PathsStore.nxtool_config}' contains invalid JSON.")
            return
