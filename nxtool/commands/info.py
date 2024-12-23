"""
List command is intended to be used in shell scripts rather than interactive
Think of apt vs apt-get
"""

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
