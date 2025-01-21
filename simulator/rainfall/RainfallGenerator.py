from abc import ABC, abstractmethod

class RainfallGenerator(ABC):
    @abstractmethod
    def generate(self, season):
        pass

