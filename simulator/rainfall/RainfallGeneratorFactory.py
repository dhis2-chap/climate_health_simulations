from simulator.rainfall.RainfallGenerator import RainfallGenerator
from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator


class RainfallGeneratorFactory:
    def create_generator(self, realistic: bool) -> RainfallGenerator:
        if realistic:
            return RealisticRainfallGenerator()
        else:
            return SyntheticRainfallGenerator()
