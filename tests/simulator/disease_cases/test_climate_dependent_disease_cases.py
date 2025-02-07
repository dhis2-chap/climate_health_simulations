import numpy as np
import pytest
import plotly.express as px
from config.SimulationConfig import DependentVariable
from simulator.ClimateData import ClimateData
from simulator.diseases.ClimateDependentDiseaseCases import ClimateDependentDiseaseCases


@pytest.fixture
def dependent_variable_config_non_autoregressive():
    config = {
        'is_autoregressive': False,
        'explanatory_variables': [
            {'type': 'rain', 'lag': 3},
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
        ],
        'population': 100}
    config = DependentVariable(**config)
    return config

@pytest.fixture
def climate_data():
    rainfall = np.zeros(10)
    rainfall[10 // 2] = 4
    return ClimateData(rainfall=rainfall, temperature=np.zeros(10), season=np.zeros(10), population=np.ones(10)*100)

def test_climate_dependent_disease_case_non_autoregressive(dependent_variable_config_non_autoregressive, climate_data):
    disease_cases = ClimateDependentDiseaseCases(dependent_variable_config_non_autoregressive)
    disease_cases = disease_cases.generate(climate_data)
    max_rainfall_index = np.argmax(climate_data.rainfall)
    max_disease_cases_index = np.argmax(disease_cases)
    assert max_disease_cases_index - max_rainfall_index == 3
    assert disease_cases.shape == (10,)
    # fig = px.line(x=range(len(climate_data.rainfall)), y=climate_data.rainfall, title="Rainfall")
    # fig.show()
    # fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    # fig.show()

def test_climate_dependent_disease_case_autoregressive(dependent_variable_config_autoregressive, climate_data):
    np.random.seed(1234)
    disease_cases = ClimateDependentDiseaseCases(dependent_variable_config_autoregressive)
    disease_cases = disease_cases.generate(climate_data)
    correlation = np.corrcoef(disease_cases[:-1], disease_cases[1:])[0, 1]
    assert abs(correlation) > 0.4
    assert disease_cases.shape == (10,)
    # fig = px.line(x=range(len(climate_data.rainfall)), y=climate_data.rainfall, title="Rainfall")
    # fig.show()
    # fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    # fig.show()