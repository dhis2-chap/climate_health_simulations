from config.SimulationConfig import DependentVariable
from simulator.diseases.ClimateAndSeasonDependentDiseaseCases import ClimateAndSeasonDependentDiseaseCases
from simulator.diseases.ClimateDependentDiseaseCases import ClimateDependentDiseaseCases
from simulator.diseases.CovariateIndependentDiseaseCases import CovariateIndependentDiseaseCases
from simulator.diseases.SeasonDependentDiseaseCases import SeasonDependentDiseaseCases


class DiseaseCasesGeneratorFactory:
    def create_generator(self, config: DependentVariable):
        explanatory_vars = config.explanatory_variables
        if not explanatory_vars:
            return CovariateIndependentDiseaseCases(config)
        has_season = any(var.type == 'season' for var in explanatory_vars)
        has_climate = any(var.type in ('rain', 'temperature') for var in explanatory_vars)
        if has_season and not has_climate:
            return SeasonDependentDiseaseCases(config)
        elif not has_season and has_climate:
            return ClimateDependentDiseaseCases(config)
        elif has_season and has_climate:
            return ClimateAndSeasonDependentDiseaseCases(config)
        else:
            raise ValueError("Invalid combination of explanatory variables.")