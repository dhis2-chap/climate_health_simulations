import pytest
import yaml
from climate_health_simulations.simulator.Simulator import Simulator


@pytest.fixture
def config_climate_and_season_dependent_non_autoregressive():
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
                {'type': 'temperature', 'lag': 3},
                {'type': 'season'}
            ],
            'population': 100},
        'n_time_points': 10
    }
    return config


@pytest.fixture
def config_climate_and_season_dependent_autoregressive():
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
                {'type': 'temperature', 'lag': 3},
                {'type': 'season'}
            ],
            'population': 100},
        'n_time_points': 10
    }
    return config

# You could for instance generate 100 data points in each simulation, use both autoregressive and non-autoregressive models, and choose different types of disease models.

@pytest.fixture
def config_climate_dependent():
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


def test_climate_and_season_dependent_non_autoregressive(config_climate_and_season_dependent_non_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_climate_and_season_dependent_non_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    climate_health = simulator.run()
    data = climate_health.get_data()
    # print(data)
    # climate_health.plot_data()

def test_climate_and_season_dependent_autoregressive(config_climate_and_season_dependent_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_climate_and_season_dependent_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    climate_health = simulator.run()
    data = climate_health.get_data()
    # print(data)
