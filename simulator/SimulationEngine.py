from config.SimulationConfig import SimulationConfig
from simulator.ClimateHealth import ClimateHealth
from simulator.Simulator import Simulator
from simulator.diseases.DiseaseCases import DiseaseCases
from simulator.rainfall.RainfallGeneratorFactory import RainfallGeneratorFactory
from simulator.season.SeasonGenerator import SeasonGenerator
from simulator.temperature.TemperatureGeneratorFactory import TemperatureGeneratorFactory


class SimulationEngine:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.rain_factory = RainfallGeneratorFactory()
        self.temp_factory = TemperatureGeneratorFactory()
        self.season_generator = SeasonGenerator()
        self.disease_cases = DiseaseCases()

    def run(self, season_name, start_date, end_date, baseline_cases, use_realistic_data):
        rain_gen = self.rain_factory.create_generator(use_realistic_data)
        temp_gen = self.temp_factory.create_generator(use_realistic_data)

        # Create season
        season = self.season_generator.create_season(season_name, start_date, end_date)

        # Generate climate data
        rainfall = rain_gen.generate(season)
        temperature = temp_gen.generate(season)

        # Create disease cases and climate health objects
        disease_cases = self.disease_cases.generate(rainfall, temperature, season)
        climate_health = ClimateHealth(rainfall, temperature, season, disease_cases)

        # Run simulation
        simulator = Simulator(self.config, climate_health)
        simulator.run_simulation()

        # Get and print results
        results = simulator.get_results()
        for season, cases in results:
            print(f"Season: {season}, Predicted Cases: {cases}")

