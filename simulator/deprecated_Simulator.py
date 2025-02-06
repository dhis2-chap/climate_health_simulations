import numpy as np
from config.SimulationConfig import SimulationConfig
from simulator.ClimateHealth import ClimateHealth
from simulator.diseases.old_DiseaseCases import DiseaseCases
from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator
from simulator.temperature.RealisticTemperatureGenerator import RealisticTemperatureGenerator


class Simulator:
    def __init__(self, n_time_points: int, lag_rain: int = None, lag_temperature: int = None, population:np.float32 = None):
        # self.config = config
        # self.climate_health = climate_health
        self.n_time_points = n_time_points
        self.lag_rain = lag_rain
        self.lag_temperature = lag_temperature
        self.population = population
        # self.results = []


    def simulate_synthetic_rainfall_linear_lag3_dependency(self):
        rainfall_generator = SyntheticRainfallGenerator()
        rainfall = rainfall_generator.generate(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_rainfall_only(rainfall, self.lag_rain)
        return ClimateHealth(rainfall, disease_cases, self.lag_rain)

    def simulate_realistic_rain_linear_lag3_dependency(self):
        rainfall_generator = RealisticRainfallGenerator()
        rainfall = rainfall_generator.generate(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_rainfall_only(rainfall, self.lag_rain)
        return ClimateHealth(rainfall, disease_cases, self.lag_rain)

    def simulate_realistic_rain3_temp1_linear_dependency(self):
        rainfall_generator = RealisticRainfallGenerator()
        rainfall = rainfall_generator.generate(self.n_time_points)
        temperature_generator = RealisticTemperatureGenerator()
        temperature = temperature_generator.generate(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_rainfall_and_temp(rainfall, temperature, self.lag_rain,
                                                                 self.lag_temperature)
        return ClimateHealth(rainfall, disease_cases, max(self.lag_rain, self.lag_temperature), temperature)

    def simulate_autoregressive_independent_rainfall(self):
        rainfall_generator = RealisticRainfallGenerator()
        rainfall = rainfall_generator.generate(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_autoregressive_independent_of_covariates(self.n_time_points,
                                                                                        self.population)
        return ClimateHealth(rainfall, disease_cases, self.lag_rain)

    def simulate_autoregressive_dependent_rainfall(self):
        rainfall_generator = RealisticRainfallGenerator()
        rainfall = rainfall_generator.generate(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_autoregressive_dependent_of_rainfall(self.n_time_points, rainfall,
                                                                                    self.population)
        return ClimateHealth(rainfall, disease_cases, self.lag_rain)

    def simulate_season_dependent(self, season):
        rainfall_generator = SyntheticRainfallGenerator()
        rainfall = rainfall_generator.generate_rainfall_dependent_on_season(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_season_dependent(season, self.population)
        return ClimateHealth(rainfall, disease_cases, 0)

    def simulate_rainfall_dependent_with_season_correlation(self):
        rainfall_generator = SyntheticRainfallGenerator()
        rainfall = rainfall_generator.generate_rainfall_dependent_on_season(self.n_time_points)
        disease_cases = DiseaseCases()
        disease_cases = disease_cases.generate_rainfall_only(rainfall, self.lag_rain)
        return ClimateHealth(rainfall, disease_cases, self.lag_rain)

