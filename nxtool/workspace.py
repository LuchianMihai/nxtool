from dataclasses import dataclass, field
import glob
import re
from typing import Any

import toml




@dataclass(frozen=True)
class Paths:
    """
    class used to store paths throughout the project
    """
    nxtool_dir_name: Path = Path(".nxtool")
    nxtool_root: Path = _topdir(nxtool_dir_name)
    nxtool_config: Path = nxtool_root / nxtool_dir_name / "config.toml"
    nxtool_projects: Path = nxtool_root / nxtool_dir_name / "projects.toml"

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

    _config_file: str = f"{Paths.nxtool_config}"

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
    # _prj_id: uuid.UUID = field(default_factory=uuid.uuid4)

    # Define the __eq__ method to compare objects
    def __eq__(self, other):
        if isinstance(other, ProjectInstance):
            return self.name == other.name
        return False

    # Define the __hash__ method based on a unique attribute
    def __hash__(self):
        return hash(self.name)


@dataclass
class ProjectStore():
    current: ProjectInstance = field(
        default_factory=lambda: ProjectInstance("make")
    )
    projects: set[ProjectInstance] = field(init=False)

    _projects_path = f"{Paths.nxtool_projects}"

    def __post_init__(self):
        self.projects = {self.current}

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["current"] = {}
        pack["current"]["name"] = self.current.name

        pack["projects"] = [
            {"name": p.name, "config": p.config}
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
                self.current = ProjectInstance(data["current"]["name"])
                self.projects = {
                    ProjectInstance(
                        p["name"],
                        p["config"] if "config" in p else None
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

@dataclass
class BoardsStore():
    boards_list: list[str] = field(
        default_factory=lambda: glob.glob("./nuttx/**/defconfig", recursive=True)
    )
    boards_dict: dict[str, list[str]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        for board in self.boards_list:
            b = Path(board).as_posix()
            m = re.search(r'/([a-zA-Z0-9_]*)/configs/(.*)/defconfig$', b)
            if m is not None:
                key = m.group(1)
                value = m.group(2)

                # Use setdefault to initialize the list if the key doesn't exist
                self.boards_dict.setdefault(key, []).append(value)

    def _split_config_str(self, config: str) -> tuple[str, str] | None:
        if ":" in config or "/" in config:
            # list unpacking throws except if more than 2 values are returned
            # if config is not formatted correctly handle accordingly
            try:
                board, brd_cfg = re.split(r"[:/]", config)
                return (board, brd_cfg)
            except ValueError:
                print("config value not formated correctly")
        return None

    def search(self, config: str) -> tuple[str, str] | None:
        cfg = self._split_config_str(config)
        if cfg is not None:
            return cfg if cfg[1] in self.boards_dict[cfg[0]] else None
        return None
