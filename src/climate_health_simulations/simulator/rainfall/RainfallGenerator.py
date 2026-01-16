from abc import ABC, abstractmethod

class RainfallGenerator(ABC):
    @abstractmethod
    def generate(self, n_time_points_train: int, n_time_points_test: int, n_rainfall_train: int, n_rainfall_test: int) -> None:
        pass

