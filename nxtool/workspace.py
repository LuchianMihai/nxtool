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
class ProjectInstance():
    name: str
    config: str = None
    board: str = None
        

@dataclass
class ProjectStore():
    current: ProjectInstance = field(default_factory=lambda: ProjectInstance("make"))
    projects: list[ProjectInstance] = field(init=False)

    def __post_init__(self):
        self.projects = [self.current]

    def _pack_data(self) -> dict[str, any]:
        pack = {}
        pack["current"] = {}
        pack["current"]["name"] = self.current.name

        pack["projects"] = [{ "name": p.name, "config": p.config, "board": p.config }
                            for p in self.projects]
        return pack

    def load(self, path: str) -> None:
        try:
            with open(path, 'r') as file:
                data: dict = toml.load(file)
                print(f"{data["current"]["name"]}")
                self.current = ProjectInstance(data["current"]["name"])
                self.projects = [ProjectInstance(
                    p["name"],
                    p["config"] if "config" in p else None,
                    p["board"] if "board" in p else None) 
                    for p in data["projects"]]
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

