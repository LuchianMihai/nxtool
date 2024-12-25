from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, TypedDict
import glob
import re
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
    nxtool_build_dir: ClassVar[Path] = Path()
    nxtool_bin_dir: ClassVar[Path] = Path()

@dataclass
class ConfigStore():
    """
    Config class that stores data from .nxtool/config.
    """

    remotes: list[tuple[str, str]] = field(init=False)

    def __post_init__(self):
        self.load()

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["remotes"] = {}
        pack["remotes"] = [
            {"name": r[0], "repo": r[1]}
            for r in self.remotes
        ]
        return pack

    def load(self) -> None:
        try:
            with open(PathsStore.nxtool_config, 'r', encoding='utf-8') as file:
                data: dict = toml.load(file)
                if "remotes" in data:
                    self.remotes = [
                        (r["name"], r["repo"])
                        for r in data["remotes"]
                    ]
                else:
                    self.remotes = list()
        except FileNotFoundError:
            print(f"Error: File '{PathsStore.nxtool_config}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{PathsStore.nxtool_config}' contains invalid TOML.")
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
            print(f"Error: File '{PathsStore.nxtool_config}' contains invalid TOML.")
            return

class ProjectOpts(TypedDict, total=False):
    generator: str
    compiler: str

@dataclass
class ProjectInstance():
    name: str = field()
    config: str = field()
    opts: ProjectOpts = field(default_factory = lambda: ({}))

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

    # This should be instance attributes
    current: ProjectInstance | None = field(init=False)
    projects: set[ProjectInstance] = field(init=False)

    def __post_init__(self):
        self.load()

    def _pack_data(self) -> dict[str, Any]:
        pack = {}
        pack["current"] = {}
        pack["current"]["name"] = self.current.name if self.current is not None else ""

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
            with open(PathsStore.nxtool_projects, 'r', encoding='utf-8') as file:
                data: dict = toml.load(file)
                self.projects = set()
                self.current = None

                if "projects" in data:
                    self.projects = {
                        ProjectInstance(p["name"], p["config"])
                        for p in data["projects"]
                    }
                    self.current = self.search(data["current"]["name"])

        except FileNotFoundError:
            print(f"Error: File '{PathsStore.nxtool_projects}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{PathsStore.nxtool_projects}' contains invalid TOML.")
            return

    def dump(self) -> None:
        try:
            with open(PathsStore.nxtool_projects, 'w', encoding='utf-8') as file:
                data = self._pack_data()
                toml.dump(data, file)
        except FileNotFoundError:
            print(f"Error: File '{PathsStore.nxtool_projects}' not found.")
            return
        except toml.TomlDecodeError:
            print(f"Error: File '{PathsStore.nxtool_projects}' contains invalid TOML.")
            return

@dataclass
class BoardsStore():
    boards_list: list[str] = field(init=False)
    boards_dict: dict[str, list[str]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.boards_list = glob.glob("./nuttx/**/defconfig", recursive=True)

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

@dataclass
class ToolsStore():
    tools_list: list[str] = field(init=False)

    def __post_init__(self):
        cmakelists = open('./nuttx/tools/CMakeLists.txt', 'r', encoding='utf-8').read()
        self.tools_list = re.findall(r'add_executable\((.*?)\s.*\)', cmakelists)

    def search(self, config: str) -> bool:
        return any(config in item for item in self.tools_list)
