import re

def split_config_str(config: str) -> tuple[str, str] | bool:
    if ":" in config or "/" in config:
        # list unpacking throws except if more than 2 values are returned
        # if config is not formatted correctly handle accordingly
        try:
            board, config = re.split(r"[:/]", config)
            return (board, config)
        except ValueError:
            print("config value not formated correctly")
    return False
