from abc import ABC, abstractmethod
from enum import Enum


class NxCmd(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, action: Enum | None = None, args: list[str] | None = None):
        pass
