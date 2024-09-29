from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class NxCmd(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, action: Enum | None = None, args: list[Any] | None = None) -> None:
        """
        Interface function to run commands with specific arguments
        """
