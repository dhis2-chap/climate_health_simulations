from abc import ABC, abstractmethod

class RainfallGenerator(ABC):
    @abstractmethod
    def generate(self, n_time_points: int):
        pass

