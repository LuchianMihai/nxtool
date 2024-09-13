import typer
from nxtool.commands import NxCmd

app = typer.Typer()

@app.callback(invoke_without_command=True)
def build():
    a = Build()
    a.run()

class Build(NxCmd):
    def __init__(self):
        pass
    
    def run(self):
        print(f"Do some building")