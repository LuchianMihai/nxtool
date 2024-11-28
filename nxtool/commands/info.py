"""
List command is intended to be used in shell scripts rather than interactive
Think of apt vs apt-get
"""
import typer

from nxtool.configuration import BoardsStore, ProjectStore, ToolsStore

app = typer.Typer()

@app.callback()
def cb():
    """
    sub-command to show workspace and projects info
    """

@app.command(name="boards")
def list_boards():
    """
    list all boards and configurations
    """
    prj: InfoCmd = InfoCmd()
    prj.boards()

@app.command(name="projects")
def list_projectst():
    """
    list all workspace projects
    """
    prj: InfoCmd = InfoCmd()
    prj.projects()

@app.command(name="project")
def list_current_project():
    """
    list current project
    """
    prj: InfoCmd = InfoCmd()
    prj.project()

@app.command(name="tools")
def list_tools():
    """
    list nuttx tools
    """
    prj: InfoCmd = InfoCmd()
    prj.tools()

class InfoCmd():
    def __init__(self):
        self.prj: ProjectStore = ProjectStore()
        self.brd: BoardsStore = BoardsStore()
        self.tls: ToolsStore = ToolsStore()

    def boards(self):
        print(self.brd.boards_dict)

    def projects(self):
        print(self.prj.projects)

    def project(self):
        print(self.prj.current)

    def tools(self):
        print(self.tls.tools_list)
