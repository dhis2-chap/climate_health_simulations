from abc import abstractmethod, ABC


class TemperatureGenerator(ABC):
    @abstractmethod
    def generate(self, n_time_points: int):
        pass



