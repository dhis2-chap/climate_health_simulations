from abc import abstractmethod, ABC


class PopulationGenerator(ABC):
    @abstractmethod
    def generate(self, n_time_points: int, population: int = None):
        pass

