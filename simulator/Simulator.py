import numpy as np
from config.SimulationConfig import SimulationConfig
from simulator.ClimateHealth import ClimateHealth
from simulator.diseases.DiseaseCases import DiseaseCases
from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
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

    def simulate_linear_lag3_dependency(self):
        pass

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


    def simulate_cases(self):
        rain = self.climate_health.rainfall
        temp = self.climate_health.temperature
        baseline_cases = self.climate_health.disease_cases.baseline_cases

        if self.config.non_linear_effects:
            cases = np.exp(rain) + np.log(temp)
        else:
            cases = rain * 0.5 + temp * 0.3

        if self.config.use_interactions:
            cases += rain * temp * 0.1

        # Additional logic for lag and autoregressive effects

        return max(0, baseline_cases + int(cases))

    def run_simulation(self):
        cases = self.simulate_cases()
        self.results.append((self.climate_health.season.name, cases))

    def get_results(self):
        return self.results
