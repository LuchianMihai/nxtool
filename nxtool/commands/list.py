from enum import Enum, unique
from typing import Any
import typer


from nxtool.commands import NxCmd
from nxtool.workspace import BoardsStore

@unique
class Action(Enum):
    BOARDS = 1

app = typer.Typer()

@app.command(name="boards")
def boards():
    prj: ListCmd = ListCmd()
    prj.run(Action.BOARDS)


class ListCmd(NxCmd):
    def __init__(self):
        pass

    def run(self, action: Enum | None = None, args: list[Any] | None = None):
        if action is not None:
            match action:
                case Action.BOARDS:
                    brd : BoardsStore = BoardsStore()
                    print(f"{brd.boards_dict}")
