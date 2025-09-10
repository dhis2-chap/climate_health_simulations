import numpy as np

from climate_health_simulations.config.SimulationConfig import DependentVariable
from climate_health_simulations.simulator.ClimateData import ClimateData
from climate_health_simulations.simulator.diseases.DiseaseCases import DiseaseCases
from climate_health_simulations.simulator.util import generate_season_weights, standardize_variable, apply_lag, \
    apply_sigmoid_and_poisson_projection_with_capping


class ClimateAndSeasonDependentDiseaseCases(DiseaseCases):
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
        disease_cases = season_weights[climate_data.season - 1] * 2 - 1
        for covariate, lag in self.get_explanatory_climate_data(climate_data):
            lagged_covariate = apply_lag(covariate, lag)
            scaled_covariate = standardize_variable(lagged_covariate)
            disease_cases += scaled_covariate.flatten() * 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, climate_data.population)
        return disease_cases

    def generate_autoregressive(self, climate_data):
        season_weights = generate_season_weights()
        disease_cases = season_weights[climate_data.season - 1] - 0.5
        for covariate, lag in self.get_explanatory_climate_data(climate_data):
            lagged_covariate = apply_lag(covariate, lag)
            scaled_covariate = standardize_variable(lagged_covariate)
            disease_cases += scaled_covariate.flatten() * 0.5
        disease_cases = np.cumsum(disease_cases) - 0.5
        # disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, climate_data.population)
        return disease_cases

    def get_explanatory_climate_data(self, climate_data):
        climate_data = [(climate_data.rainfall, var.lag) if var.type == 'rain' else (
        climate_data.temperature, var.lag) if var.type == 'temperature' else None for var in
                        self.config.explanatory_variables]
        return tuple(item for item in climate_data if item is not None)

    def get_name(self):
        return "ClimateAndSeasonDependentDiseaseCases"