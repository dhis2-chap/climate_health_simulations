import pytest
import yaml
from simulator.Simulator import Simulator


@pytest.fixture
def config_covariate_independent_autoregressive():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': True,
            'explanatory_variables': [
            ],
            'population': 100},
        'n_time_points': 10
    }
    return config


def test_covariate_independent_autoregressive(config_covariate_independent_autoregressive, tmp_path):
    simulation_config_path = tmp_path / 'simulation_config.yaml'
    # print(simulation_config_path)
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config_covariate_independent_autoregressive, f)
    simulator = Simulator(simulation_config_path)
    climate_health = simulator.run()
    data = climate_health.get_data()
    # print(data)
