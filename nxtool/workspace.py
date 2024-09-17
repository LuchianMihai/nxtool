from dataclasses import dataclass, field
from typing import Any
import uuid

import toml

from nxtool.constants import Constants as cst

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

    _config_file: str = f"{cst.nxtool_config}"

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["remotes"] = {}
        pack["remotes"]["nuttx"] = self.nuttx
        pack["remotes"]["apps"] = self.apps
        return pack

    def load(self) -> None:
        try:
            with open(self._config_file, 'r', encoding='utf-8') as file:
                data: dict = toml.load(file)
                self.nuttx = data["remotes"]["nuttx"]
                self.apps = data["remotes"]["apps"]
        except FileNotFoundError:
            print(f"Error: File '{self._config_file}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{self._config_file}' contains invalid JSON.")
            return

    def dump(self) -> None:
        try:
            with open(self._config_file, 'w', encoding='utf-8') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{self._config_file}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{self._config_file}' contains invalid JSON.")
            return


@dataclass
class ProjectInstance():
    name: str
    config: str | None = None
    board: str | None = None
    _prj_id: uuid.UUID = field(default_factory=uuid.uuid4)

    # Define the __eq__ method to compare objects
    def __eq__(self, other):
        if isinstance(other, ProjectInstance):
            return self._prj_id == other._prj_id
        return False

    # Define the __hash__ method based on a unique attribute
    def __hash__(self):
        return hash(self._prj_id)


@dataclass
class ProjectStore():
    current: ProjectInstance = field(
        default_factory=lambda: ProjectInstance("make")
    )
    projects: set[ProjectInstance] = field(init=False)

    _projects_path = f"{cst.nxtool_projects}"

    def __post_init__(self):
        self.projects = {self.current}

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["current"] = {}
        pack["current"]["name"] = self.current.name

        pack["projects"] = [
            {"name": p.name, "config": p.config, "board": p.board}
            for p in self.projects
        ]
        return pack

    def search(self, name: str) -> ProjectInstance | None:
        return next(
            (x for x in self.projects if x.name == name),
            None
        )

    def load(self) -> None:
        try:
            with open(self._projects_path, 'r', encoding='utf-8') as file:
                data: dict = toml.load(file)
                print(f"{data["current"]["name"]}")
                self.current = ProjectInstance(data["current"]["name"])
                self.projects = {
                    ProjectInstance(
                        p["name"],
                        p["config"] if "config" in p else None,
                        p["board"] if "board" in p else None
                    )
                    for p in data["projects"]
                }
        except FileNotFoundError:
            print(f"Error: File '{self._projects_path}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{self._projects_path}' contains invalid JSON.")
            return

    def dump(self) -> None:
        try:
            with open(self._projects_path, 'w', encoding='utf-8') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{self._projects_path}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{self._projects_path}' contains invalid JSON.")
            return
