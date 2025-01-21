from abc import abstractmethod, ABC


class TemperatureGenerator(ABC):
    @abstractmethod
    def generate(self, season):
        pass



