import numpy as np

from climate_health_simulations.config.SimulationConfig import Config, DependentVariable
from climate_health_simulations.simulator.ClimateData import ClimateData
from climate_health_simulations.simulator.util import apply_lag, standardize_variable, apply_sigmoid_scaling_to_cases, \
    apply_sigmoid_and_poisson_projection_with_capping


class ClimateDependentDiseaseCases:
    def __init__(self, config: DependentVariable):
        self.config = config

    def generate(self, climate_data: ClimateData):
        if self.config.is_autoregressive:
            return self.generate_autoregressive(climate_data)
        else:
            return self.generate_non_autoregressive(climate_data)

    def generate_non_autoregressive(self, climate_data):
        explanatory_climate_data = self.get_explanatory_climate_data(climate_data)
        shape = explanatory_climate_data[0][0].shape
        eta = np.zeros(shape)
        for covariate, lag in explanatory_climate_data:
            lagged_covariate = apply_lag(covariate, lag)
            eta += lagged_covariate
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(eta, climate_data.population)
        return disease_cases

    def generate_autoregressive(self, climate_data):
        if climate_data.population is None:
            raise ValueError("Population must be supplied to scale the disease cases.")
        explanatory_climate_data = self.get_explanatory_climate_data(climate_data)
        n_time_points = len(explanatory_climate_data[0][0])
        white_noise = np.random.normal(0, 0.2, size=n_time_points)
        eta = np.zeros(n_time_points)
        for covariate, lag in explanatory_climate_data:
            lagged_covariate = apply_lag(covariate, lag)
            scaled_covariate = standardize_variable(lagged_covariate[1:])
            eta += scaled_covariate
        eta += np.cumsum(white_noise)
        disease_cases = apply_sigmoid_scaling_to_cases(eta, climate_data.population)
        return disease_cases

    def get_explanatory_climate_data(self, climate_data):
        climate_data = [(climate_data.rainfall, var.lag) if var.type == 'rain' else (
            climate_data.temperature, var.lag) if var.type == 'temperature' else None for var in
                        self.config.explanatory_variables]
        return tuple(item for item in climate_data if item is not None)

    def get_name(self):
        return "ClimateDependentDiseaseCases"
