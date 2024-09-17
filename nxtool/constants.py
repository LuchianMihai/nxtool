from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    """
    class used to store constants throughout the project
    """
    nxtool_dir_name: str = ".nxtool"
    nxtool_config: str = f"{nxtool_dir_name}/config.toml"
    nxtool_projects: str = f"{nxtool_dir_name}/projects.toml"
