import numpy as np

from config.SimulationConfig import DependentVariable
from simulator.ClimateData import ClimateData
from simulator.util import apply_sigmoid_and_poisson_projection_with_capping, generate_season_weights


class SeasonDependentDiseaseCases:
    def __init__(self, config: DependentVariable):
        self.config = config

    def generate(self, climate_data: ClimateData):
        if self.config.is_autoregressive:
            return self.generate_autoregressive(climate_data)
        else:
            return self.generate_non_autoregressive(climate_data)

    def generate_non_autoregressive(self, climate_data):
        season_weights = generate_season_weights()
        disease_cases = season_weights[climate_data.season - 1] * 2 - 3
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, climate_data.population)
        return disease_cases

    def generate_autoregressive(self, climate_data):
        season_weights = generate_season_weights()
        season_weights = season_weights[climate_data.season - 1]
        disease_cases = np.cumsum(season_weights)/3 - 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, climate_data.population)
        return disease_cases

    def get_name(self):
        return "SeasonDependentDiseaseCases"
