import numpy as np
import yaml
from config.SimulationConfig import IndependentVariable, ExplanatoryVariable, DependentVariable, Config
from simulator.ClimateData import ClimateData
from simulator.ClimateHealth import ClimateHealth
from simulator.diseases.DiseaseCasesGeneratorFactory import DiseaseCasesGeneratorFactory
from simulator.population.PopulationGeneratorFactory import PopulationGeneratorFactory
from simulator.rainfall.RainfallGeneratorFactory import RainfallGeneratorFactory
from simulator.temperature.TemperatureGeneratorFactory import TemperatureGeneratorFactory


class Simulator:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        try:
            self.config = Config(**config_data)
        except Exception as e:
            raise ValueError(f"Invalid configuration: {e}")
        self.rain_factory = RainfallGeneratorFactory()
        self.temp_factory = TemperatureGeneratorFactory()
        self.population_factory = PopulationGeneratorFactory()
        self.disease_cases_generator = DiseaseCasesGeneratorFactory()

    def run(self):
        rain_is_realistic, rain_season_dependent,  = self.config.get_independent_variable_properties("rain")
        temp_is_realistic, temp_season_dependent = self.config.get_independent_variable_properties("temperature")

        rain_gen = self.rain_factory.create_generator(rain_is_realistic, rain_season_dependent)
        temp_gen = self.temp_factory.create_generator(temp_is_realistic, temp_season_dependent)
        disease_cases_gen = self.disease_cases_generator.create_generator(self.config.dependent_variable)
        pop_gen = self.population_factory.create_generator(False)  # todo: fix this to be dynamic

        # Generate climate data
        season = (np.arange(self.config.n_time_points) % 12) + 1
        rainfall = rain_gen.generate(self.config.n_time_points)
        temperature = temp_gen.generate(self.config.n_time_points)
        population = pop_gen.generate(self.config.n_time_points, self.config.dependent_variable.population)
        climate_data = ClimateData(rainfall, temperature, season, population)

        disease_cases = disease_cases_gen.generate(climate_data)
        climate_health = ClimateHealth(climate_data, disease_cases, self.config.get_max_lag())
        return climate_health

