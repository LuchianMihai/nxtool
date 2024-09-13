from dataclasses import dataclass, field
from enum import Enum
import toml


@dataclass
class ConfigStore():
    f"""
    Config class that stores data from .nxtool/config.

    :ivar nuttx: URL for the NuttX repository.
    :vartype nuttx: str
    :ivar apps: URL for the NuttX apps repository.
    :vartype apps: str
    """

    nuttx: str = "https://github.com/apache/nuttx"
    apps: str = "https://github.com/apache/nuttx-apps"

    def _pack_data(self) -> dict[str, any]:
        pack = {}
        pack["nuttx"] = self.nuttx
        pack["apps"] = self.apps
        return pack


    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as file:
                data: dict = toml.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{file_path}' contains invalid JSON.")
            return
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return

    def dump(self, path: str) -> None:
        try:
            with open(path, 'w') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{file_path}' contains invalid JSON.")
            return
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return

@dataclass
class Project():
    name: str = None
    config: str = None
    board: str = None
        

@dataclass
class ProjectStore():
    current: Project = field(default_factory=lambda: Project("make"))
    projects: list[Project] = field(init=False)

    def __post_init__(self):
        self.projects = [self.current]

    def _pack_data(self) -> dict[str, any]:
        pack = {}
        pack["current"] = {}
        pack["current"]["name"] = self.current.name

        pack["projects"] = [{ "name": p.name, "config": p.config, "board": p.config }
                            for p in self.projects]
        return pack

    def dump(self, path: str) -> None:
        try:
            with open(path, 'w') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{file_path}' contains invalid JSON.")
            return
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return

