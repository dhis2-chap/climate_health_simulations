import numpy as np

from config.SimulationConfig import Config, DependentVariable
from simulator.ClimateData import ClimateData
from simulator.util import apply_sigmoid_scaling_to_cases


class CovariateIndependentDiseaseCases:
    def __init__(self, config: DependentVariable):
        self.config = config

    def generate(self, climate_data: ClimateData) -> np.ndarray:
        return self.generate_autoregressive(climate_data.population)

    def generate_autoregressive(self, population: np.ndarray) -> np.ndarray:
        white_noise = np.random.normal(0, 0.2, size=len(population) - 1)
        disease_cases = np.cumsum(white_noise)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_scaling_to_cases(disease_cases, population)
        return disease_cases

    def get_name(self):
        return "CovariateIndependentDiseaseCases"
