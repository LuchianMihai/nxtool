from enum import Enum, unique
from typing import Any
import typer

from nxtool.workspace import BoardsStore

app = typer.Typer()

@app.command(name="boards")
def boards():
    prj: ListCmd = ListCmd()
    prj.run()

class ListCmd():
    def __init__(self):
        pass
    
    def run(self):
        pass