import pytest

from climate_health_simulations.config.SimulationConfig import Config
from climate_health_simulations.config.config_variations.ConfigGenerator import ConfigGenerator


class TestConfigGeneration:
    @pytest.fixture
    def base_config(self):
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
        return Config(**config)

    def test_generation_counts(self, base_config):
        configs = list(ConfigGenerator.generate_all(base_config))
        assert len(configs) == 144

    def test_explanatory_variations(self, base_config):
        """Test all explanatory combinations are generated"""
        generated = [
            c.dependent_variable.explanatory_variables
            for c in ConfigGenerator.generate_all(base_config)
        ]
        assert any(len(vars) == 0 for vars in generated)  # Empty case
        assert any(len(vars) == 3 for vars in generated)  # Full combination