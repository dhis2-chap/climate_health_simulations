import numpy as np
from simulator.util import generate_season_weights, apply_lag, standardize_variable, apply_sigmoid_scaling_to_cases, \
    apply_sigmoid_and_poisson_projection_with_capping


class OldDiseaseCases:
    def generate_rainfall_only(self, rainfall, lag_rain: int, season=None):
        lagged_rainfall = apply_lag(rainfall, lag_rain)
        poisson_rate = np.exp(lagged_rainfall)
        disease_cases = np.random.poisson(poisson_rate, len(rainfall))
        return disease_cases

    def generate_rainfall_and_temp(self, rainfall, temperature, lag_rain: int, lag_temperature: int, season=None):
        lagged_rainfall = apply_lag(rainfall, lag_rain)
        lagged_temperature = apply_lag(temperature, lag_temperature)
        poisson_rate = np.exp(lagged_rainfall + lagged_temperature)
        disease_cases = np.random.poisson(poisson_rate, len(rainfall))
        return disease_cases

    def generate_autoregressive_independent_of_covariates(self, n_time_points, population, season=None):
        white_noise = np.random.normal(0, 0.2, size=n_time_points - 1)
        disease_cases = np.cumsum(white_noise)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_scaling_to_cases(disease_cases, population)
        return disease_cases

    def generate_autoregressive_dependent_of_rainfall(self, n_time_points, rainfall, population, season=None):
        scaled_rainfall = standardize_variable(rainfall[1:]) # why from first element? becuse we wnated to make the first element 0 and independent
        white_noise = np.random.normal(0, 0.2, size=n_time_points - 1) + scaled_rainfall.flatten() * 0.5
        disease_cases = np.cumsum(white_noise)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_scaling_to_cases(disease_cases, population)
        return disease_cases

    def generate_season_dependent(self, season, population):
        season_weights = generate_season_weights()
        disease_cases = season_weights[
                            season-1] * 2 - 5 # + np.random.normal(scale=0.5, size=len(season)) # season we pass here is vector of month indices that should affect the disease cases
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, population)
        return disease_cases

    def generate_season_and_rainfall_dependent(self, season, rainfall, population):
        scaled_rainfall = standardize_variable(rainfall[1:])
        season_weights = generate_season_weights()
        disease_cases = season_weights[season-1] * 2 - 5 + scaled_rainfall * 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, population)
        return disease_cases

    def generate_autoregressive_dependent_of_season(self, n_time_points, season, population): #todo remember to remove lagged disease cases
        season_weights = generate_season_weights()
        season_weights = season_weights[season - 1][1:]
        # white_noise = np.random.normal(0, 0.2, size=n_time_points - 1) + season_weights[1:] * 0.5
        disease_cases = np.cumsum(season_weights)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, population)
        return disease_cases

    def generate_autoregressive_dependent_of_season_and_rainfall(self, n_time_points, rainfall, season, population): #todo remember to remove lagged disease cases
        scaled_rainfall = standardize_variable(rainfall[1:])
        season_weights = generate_season_weights()
        season_weights = season_weights[season - 1][1:] + scaled_rainfall.flatten() * 0.5
        # white_noise = np.random.normal(0, 0.2, size=n_time_points - 1) + season_weights[1:] * 0.5
        disease_cases = np.cumsum(season_weights)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, population)
        return disease_cases