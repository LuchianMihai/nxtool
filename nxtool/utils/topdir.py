from pathlib import Path

def topdir(target_dir: Path) -> Path:
    """Search for topdir of the current workspace

    Args:
        target_dir (Path): name of the directory that defines the root of thw workspace

    Returns:
        Path | None: path to workspace root
    """
    current_dir: Path = Path.cwd()
    ret: Path | None = next(
        (
            p for p in [current_dir] + list(current_dir.parents)
            if (p / f"{target_dir}").is_dir()
        ),
        None
    )

    if ret is None:
        raise FileNotFoundError

    return ret
