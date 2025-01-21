import numpy as np
from sklearn.preprocessing import StandardScaler

from simulator.util import generate_season_weights


class DiseaseCases:
    def generate_rainfall_only(self, rainfall, lag_rain: int, season=None):
        lagged_rainfall = np.roll(rainfall, lag_rain)
        poisson_rate = np.exp(lagged_rainfall)
        disease_cases = np.random.poisson(poisson_rate, len(rainfall))
        return disease_cases

    def generate_rainfall_and_temp(self, rainfall, temperature, lag_rain: int, lag_temperature: int, season=None):
        lagged_rainfall = np.roll(rainfall, lag_rain)
        lagged_temperature = np.roll(temperature, lag_temperature)
        poisson_rate = np.exp(lagged_rainfall + lagged_temperature)
        disease_cases = np.random.poisson(poisson_rate, len(rainfall))
        return disease_cases

    def generate_autoregressive_independent_of_covariates(self, n_time_points, population, season=None):
        white_noise = np.random.normal(0, 0.2, size=n_time_points-1)
        disease_cases = np.cumsum(white_noise)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = np.int32((1 / (1 + np.exp(-disease_cases))) * population)
        return disease_cases

    def generate_autoregressive_dependent_of_rainfall(self, n_time_points, rainfall, population, season=None):
        scaler = StandardScaler()
        scaled_rainfall = scaler.fit_transform(rainfall[1:].reshape(-1, 1))
        white_noise = np.random.normal(0, 0.2, size=n_time_points-1) + scaled_rainfall.flatten() * 0.5
        disease_cases = np.cumsum(white_noise)
        disease_cases = np.insert(disease_cases, 0, 0) - 0.5
        disease_cases = np.int32((1 / (1 + np.exp(-disease_cases))) * population)
        return disease_cases

    def generate_season_dependent(self, season, population):
        season_weights = generate_season_weights()
        disease_cases = season_weights[season] * 2 - 2  # maybe have some noise later
        disease_cases = np.int32((1 / (1 + np.exp(-disease_cases))) * population)
        return disease_cases

