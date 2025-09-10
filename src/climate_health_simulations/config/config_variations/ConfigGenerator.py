from itertools import product
from typing import Generator, List, Dict, Optional
import copy

from climate_health_simulations.config.SimulationConfig import Config, IndependentVariable, ExplanatoryVariable
from climate_health_simulations.config.config_variations.ConfigParameters import ConfigParameters


class ConfigGenerator:
    @classmethod
    def generate_all(cls, base_config: Config) -> Generator[Config, None, None]:
        """
        Generates all valid configuration variations using a Cartesian product
        of defined parameters while respecting Pydantic validation rules
        """

        weather_combos = cls._generate_weather_combinations()

        for (weather_config,
             ar_flag,
             explan_combo) in product(
            weather_combos,
            ConfigParameters.AUTOREGRESSIVE_OPTIONS,
            ConfigParameters.EXPLANATORY_COMBINATIONS
        ):

            try:
                # Create config copy with new parameters
                new_config = cls._build_config(
                    base_config=base_config,
                    weather_config=weather_config,
                    ar_flag=ar_flag,
                    explan_combo=explan_combo
                )
                yield new_config
            except ValueError as e:
                pass
                # print(f"Skipping invalid combination: {str(e)}")

    @classmethod
    def _generate_weather_combinations(cls) -> Generator[Dict, None, None]:
        """Generate all valid weather variable combinations"""
        for rain_real, rain_season in product(
                ConfigParameters.RAIN_FLAGS['is_realistic'],
                ConfigParameters.RAIN_FLAGS['is_season_dependent']
        ):
            for temp_real, temp_season in product(
                    ConfigParameters.TEMPERATURE_FLAGS['is_realistic'],
                    ConfigParameters.TEMPERATURE_FLAGS['is_season_dependent']
            ):
                try:
                    yield {
                        'independent_variables': [
                            IndependentVariable(
                                type='rain',
                                is_realistic=rain_real,
                                is_season_dependent=rain_season
                            ),
                            IndependentVariable(
                                type='temperature',
                                is_realistic=temp_real,
                                is_season_dependent=temp_season
                            ),
                            IndependentVariable(type='season', is_realistic=False)
                        ]
                    }
                except ValueError as e:
                    # print(f"Skipping invalid weather combination: {str(e)}")
                    pass

    @classmethod
    def _build_config(cls,
                      base_config: Config,
                      weather_config: Dict,
                      ar_flag: bool,
                      explan_combo: List[str]) -> Config:
        """Build and validate a new configuration"""
        config_dict = base_config.model_dump()
        config_dict.update(weather_config)

        # Update dependent variables
        config_dict['dependent_variable'] = copy.deepcopy(
            base_config.dependent_variable.model_dump()
        )
        config_dict['dependent_variable']['is_autoregressive'] = ar_flag
        config_dict['dependent_variable']['explanatory_variables'] = [
            ExplanatoryVariable(
                type=var_type,
                lag=lag if var_type in ['rain', 'temperature'] else None
            )
            for var_type in explan_combo
            for lag in ConfigParameters.LAG_OPTIONS
        ]
        return Config(**config_dict)
