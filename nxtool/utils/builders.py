"""
Wrappers over build tools. For the moment only cmake and make are supported    
"""

class MakeBuilder:
    """
    Wrapper class over make build system.
    Should be assumed that any arguments given here are already checked and valid
    """

    def __init__(
        self,
        config: str
        ) -> None:
        self.config: str = config

    def configure(self):
        """
        equivalent to ./tools/configure.sh
        """

    def run(self):
        "run builder"

class CMakeBuilder:
    def __init__(self) -> None:
        pass

    def configure(self):
        pass

    def run(self):
        pass
