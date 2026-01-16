import pytest
import yaml
from climate_health_simulations.simulator.Simulator import Simulator


@pytest.fixture
def config_climate_dependent_non_autoregressive():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': False,
            'explanatory_variables': [
                {'type': 'rain', 'lag': 3},
                {'type': 'temperature', 'lag': 3}
            ],
            'population': 100},
        'n_time_points': 10
    }
    return config

@pytest.fixture
def config_rain_dependent_non_autoregressive():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False, 'is_uniform': False},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': False,
            'explanatory_variables': [
                {'type': 'rain', 'lag': 3},
            ],
            'population': 100},
        'n_time_points_train': 10,
        'n_time_points_test': 10,
        'n_rainfall_train': 3,
        'n_rainfall_test': 3
    }
    return config

@pytest.fixture
def config_uniform_rain_dependent_non_autoregressive():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False, 'is_uniform': True},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': False,
            'is_non_linear': True,
            'explanatory_variables': [
                {'type': 'rain', 'lag': 3, 'min_val': 0, 'max_val': 100},
            ],
            'population': 1000},
        'n_time_points_train': 10,
        'n_time_points_test': 10,
        'n_rainfall_train': 3,
        'n_rainfall_test': 3
    }
    return config

@pytest.fixture
def config_climate_dependent_autoregressive():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': True,
            'explanatory_variables': [
                {'type': 'rain', 'lag': 3},
                {'type': 'temperature', 'lag': 3}
            ],
            'population': 100},
        'n_time_points': 10
    }
    return config

def test_climate_dependent_non_autoregressive(config_climate_dependent_non_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    # print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_climate_dependent_non_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    # print(simulator.disease_cases_generator.create_generator(simulator.config.dependent_variable).get_name())
    climate_health = simulator.run()
    data = climate_health.get_data()
    # print(data)

def test_rain_dependent_non_autoregressive(config_rain_dependent_non_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    # print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_rain_dependent_non_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    # print(simulator.disease_cases_generator.create_generator(simulator.config.dependent_variable).get_name())
    climate_health = simulator.run()
    data = climate_health.get_data()
    print(data)

def test_uniform_rain_dependent_non_autoregressive(config_uniform_rain_dependent_non_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    # print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_uniform_rain_dependent_non_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    # print(simulator.disease_cases_generator.create_generator(simulator.config.dependent_variable).get_name())
    climate_health = simulator.run()
    data = climate_health.get_data()
    print(data)

def test_climate_dependent_autoregressive(config_climate_dependent_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    # print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_climate_dependent_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    climate_health = simulator.run()
    data = climate_health.get_data()
    # print(data)
