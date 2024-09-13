from abc import ABC, abstractmethod

class NxCmd(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def run(self):
        pass