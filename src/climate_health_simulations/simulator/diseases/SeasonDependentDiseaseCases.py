import numpy as np

from climate_health_simulations.config.SimulationConfig import DependentVariable
from climate_health_simulations.simulator.ClimateData import ClimateData
from climate_health_simulations.simulator.util import apply_sigmoid_and_poisson_projection_with_capping, generate_season_weights


class SeasonDependentDiseaseCases:
    def __init__(self, config: DependentVariable):
        self.config = config
        #todo: add white noise to both methods

    def generate(self, climate_data: ClimateData):
        if self.config.is_autoregressive:
            return self.generate_autoregressive(climate_data)
        else:
            return self.generate_non_autoregressive(climate_data)

    def generate_non_autoregressive(self, climate_data):
        season_weights = generate_season_weights()
        eta = season_weights[climate_data.season - 1]
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(eta, climate_data.population)
        return disease_cases

    def generate_autoregressive(self, climate_data):
        season_weights = generate_season_weights()
        eta_season = season_weights[climate_data.season - 1]
        n_time_points = len(climate_data.population)
        white_noise = np.random.normal(0, 0.2, size=n_time_points)
        AR_term = np.cumsum(white_noise)
        eta = eta_season + AR_term
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(eta, climate_data.population)
        return disease_cases

    def get_name(self):
        return "SeasonDependentDiseaseCases"
