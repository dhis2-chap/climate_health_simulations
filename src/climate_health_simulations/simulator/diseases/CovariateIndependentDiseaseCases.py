import numpy as np

from climate_health_simulations.config.SimulationConfig import Config, DependentVariable
from climate_health_simulations.simulator.ClimateData import ClimateData
from climate_health_simulations.simulator.util import apply_sigmoid_and_poisson_projection_with_capping


class CovariateIndependentDiseaseCases:
    def __init__(self, config: DependentVariable):
        self.config = config
        #todo: make also not autoregressive version
        #todo: never insert zero at the start
        #todo: see if Ingar could try out EWARS models can be run on one simulated dataset run through chap python
        #todo: Martin could support all the simulations in his DSL

    def generate(self, climate_data: ClimateData) -> np.ndarray:
        return self.generate_autoregressive(climate_data.population)

    def generate_non_autoregressive(self, population: np.ndarray) -> np.ndarray:
        white_noise = np.random.normal(0, 0.2, size=len(population))
        #disease_cases = np.cumsum(white_noise)
        #disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(white_noise, population)
        return disease_cases

    def generate_autoregressive(self, population: np.ndarray) -> np.ndarray:
        white_noise = np.random.normal(0, 0.2, size=len(population)) #todo make scale an adjustable argument
        eta = np.cumsum(white_noise)
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(eta, population)
        return disease_cases

    def get_name(self):
        return "CovariateIndependentDiseaseCases"
