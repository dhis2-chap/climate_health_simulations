from simulator.temperature.RealisticTemperatureGenerator import RealisticTemperatureGenerator
from simulator.temperature.SyntheticTemperatureGenerator import SyntheticTemperatureGenerator
from simulator.temperature.TemperatureGenerator import TemperatureGenerator


class TemperatureGeneratorFactory:
    def create_generator(self, realistic: bool) -> TemperatureGenerator:
        if realistic:
            return RealisticTemperatureGenerator()
        else:
            return SyntheticTemperatureGenerator()
