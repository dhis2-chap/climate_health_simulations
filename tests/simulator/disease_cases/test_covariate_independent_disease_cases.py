import numpy as np
import pytest
import plotly.express as px
from climate_health_simulations.config.SimulationConfig import DependentVariable
from climate_health_simulations.simulator.ClimateData import ClimateData
from climate_health_simulations.simulator.diseases.CovariateIndependentDiseaseCases import CovariateIndependentDiseaseCases
from climate_health_simulations.simulator.util import generate_season_weights, apply_lag, standardize_variable

@pytest.fixture
def dependent_variable_config_autoregressive():
    config = {
        'is_autoregressive': True,
        'explanatory_variables': [
        ],
        'population': 100}
    config = DependentVariable(**config)
    return config

@pytest.fixture
def climate_data():
    rainfall = np.zeros(10)
    rainfall[10 // 2] = 4
    season = (np.arange(10) % 12) + 1
    return ClimateData(rainfall=rainfall, temperature=np.zeros(10), season=season, population=np.ones(10)*100)


def test_covariate_independent_disease_case_autoregressive(dependent_variable_config_autoregressive, climate_data):
    np.random.seed(123)
    disease_cases_generator = CovariateIndependentDiseaseCases(dependent_variable_config_autoregressive)
    disease_cases = disease_cases_generator.generate(climate_data)
    assert disease_cases.shape == (10,)
    correlation_autoregressive = np.corrcoef(disease_cases[:-1], disease_cases[1:])[0, 1]
    assert abs(correlation_autoregressive) > 0.2, "Disease cases do not exhibit a strong autoregressive pattern."
    print(correlation_autoregressive)
    assert np.all(disease_cases >= 0), "Disease cases should be non-negative."
    assert np.all(disease_cases <= climate_data.population[0]), "Disease cases should not exceed population."
    # fig = px.line(x=range(len(climate_data.rainfall)), y=climate_data.rainfall, title="Rainfall")
    # fig.show()
    # fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    # fig.show()