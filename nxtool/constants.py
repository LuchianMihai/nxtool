from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    NXTOOL_DIR_NAME: str = ".nxtool"
    NXTOOL_CONFIG: str = "config.toml"
    NXTOOL_PROJECTS: str = "projects.toml"
