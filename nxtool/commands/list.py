
import typer

from nxtool.workspace import BoardsStore, ProjectStore, ToolsStore

app = typer.Typer()

@app.command(name="boards")
def list_boards():
    prj: ListCmd = ListCmd()
    prj.boards()

@app.command(name="projects")
def list_projectst():
    prj: ListCmd = ListCmd()
    prj.projects()

@app.command(name="prj")
def list_current_project():
    prj: ListCmd = ListCmd()
    prj.project()

@app.command(name="tools")
def list_tools():
    prj: ListCmd = ListCmd()
    prj.tools()

class ListCmd():
    def __init__(self):
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()
        self.tls: ToolsStore = ToolsStore()

    def boards(self):
        print(self.brd.boards_dict)

    def projects(self):
        self.prj.load()
        print(self.prj.projects)

    def project(self):
        self.prj.load()
        print(self.prj.current)

    def tools(self):
        print(self.tls.tools_list)