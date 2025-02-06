import numpy as np
import pytest
import plotly.express as px
from config.SimulationConfig import DependentVariable
from simulator.ClimateData import ClimateData
from simulator.diseases.ClimateAndSeasonDependentDiseaseCases import ClimateAndSeasonDependentDiseaseCases
from simulator.util import generate_season_weights, apply_lag, standardize_variable


@pytest.fixture
def dependent_variable_config_non_autoregressive():
    config = {
        'is_autoregressive': False,
        'explanatory_variables': [
            {'type': 'rain', 'lag': 3},
            {'type': 'season'},
        ],
        'population': 100}
    config = DependentVariable(**config)
    return config

@pytest.fixture
def dependent_variable_config_autoregressive():
    config = {
        'is_autoregressive': True,
        'explanatory_variables': [
            {'type': 'rain', 'lag': 3},
            {'type': 'season'},
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


def test_climate_and_season_dependent_disease_case_non_autoregressive(dependent_variable_config_non_autoregressive, climate_data):
    np.random.seed(1234)
    disease_cases = ClimateAndSeasonDependentDiseaseCases(dependent_variable_config_non_autoregressive)
    disease_cases = disease_cases.generate(climate_data)
    assert disease_cases.shape == (10,)
    season_weights = generate_season_weights()
    seasonal_influence = season_weights[climate_data.season - 1][1:] * 2 - 5
    correlation = np.corrcoef(seasonal_influence, disease_cases[1:])[0, 1]
    assert abs(correlation) > 0.7, "Disease cases should exhibit some correlation with seasonal weights."
    assert np.all(disease_cases >= 0), "Disease cases should be non-negative."
    assert np.all(disease_cases <= climate_data.population[0]), "Disease cases should not exceed population."
    fig = px.line(x=range(len(climate_data.rainfall)), y=climate_data.rainfall, title="Rainfall")
    fig.show()
    fig = px.line(x=range(len(seasonal_influence)), y=seasonal_influence, title="Season weights")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()

def test_climate_and_season_dependent_disease_case_autoregressive(dependent_variable_config_autoregressive, climate_data):
    np.random.seed(2025)
    disease_cases_generator = ClimateAndSeasonDependentDiseaseCases(dependent_variable_config_autoregressive)
    disease_cases = disease_cases_generator.generate(climate_data)
    assert disease_cases.shape == (10,)
    season_weights = generate_season_weights()
    seasonal_influence = season_weights[climate_data.season - 1][1:]
    initial_disease_cases = seasonal_influence.copy()
    for covariate, lag in disease_cases_generator.get_explanatory_climate_data(climate_data):
        lagged_covariate = apply_lag(covariate, lag)
        scaled_covariate = standardize_variable(lagged_covariate[1:])
        initial_disease_cases += scaled_covariate.flatten() * 0.5
    correlation = np.corrcoef(seasonal_influence, initial_disease_cases)[0, 1]
    assert abs(correlation) > 0.7, "Initial disease cases should exhibit some correlation with seasonal weights."
    assert np.all(disease_cases >= 0), "Disease cases should be non-negative."
    assert np.all(disease_cases <= climate_data.population[0]), "Disease cases should not exceed population."
    correlation_autoregressive = np.corrcoef(disease_cases[:-1], disease_cases[1:])[0, 1]
    assert abs(correlation_autoregressive) > 0.6, "Disease cases do not exhibit a strong autoregressive pattern."
    fig = px.line(x=range(len(climate_data.rainfall)), y=climate_data.rainfall, title="Rainfall")
    fig.show()
    fig = px.line(x=range(len(seasonal_influence)), y=seasonal_influence, title="Season weights")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()
