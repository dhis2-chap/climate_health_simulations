import numpy as np
import pytest
import plotly.express as px
from config.SimulationConfig import DependentVariable
from simulator.ClimateData import ClimateData
from simulator.diseases.ClimateDependentDiseaseCases import ClimateDependentDiseaseCases
from simulator.diseases.SeasonDependentDiseaseCases import SeasonDependentDiseaseCases
from simulator.util import apply_sigmoid_and_poisson_projection_with_capping, standardize_variable, \
    generate_season_weights


def test_generate_autoregressive_independent_of_covariates():
    n_time_points = 10
    population = np.ones(n_time_points) * 1000
    disease_cases = DiseaseCases()
    disease_cases = disease_cases.generate_autoregressive_independent_of_covariates(n_time_points, population)
    print(disease_cases)


def test_generate_autoregressive_dependent_of_rainfall():
    n_time_points = 10
    rainfall = np.random.randint(100, 500, n_time_points)
    population = np.ones(n_time_points) * 1000
    # disease_cases = DiseaseCases()
    # disease_cases = disease_cases.generate_autoregressive_dependent_of_rainfall(n_time_points, rainfall, population)
    disease_cases = ClimateDependentDiseaseCases(rainfall, lags=[0], is_autoregressive=True, population=population)
    disease_cases = disease_cases.generate()
    fig = px.line(x=range(len(rainfall)), y=rainfall, title="Rainfall")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()


def test_generate_season_dependent():
    season = np.array(range(1, 13))
    season = np.tile(season, 2)
    population = np.ones(len(season)) * 1000
    # disease_cases = DiseaseCases()
    # disease_cases = disease_cases.generate_season_dependent(season, population)
    disease_cases = SeasonDependentDiseaseCases(season, population)
    disease_cases = disease_cases.generate()
    fig = px.line(x=range(len(season)), y=season, title="Season")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()


def test_generate_season_and_rainfall_dependent():
    season = np.array(range(1, 13))
    season = np.tile(season, 2)
    population = np.ones(len(season)) * 1000
    n_time_points = len(season)
    rainfall = np.random.randint(100, 500, n_time_points)
    scaled_rainfall = standardize_variable(rainfall[1:])
    season_weights = generate_season_weights()
    disease_cases_2 = season_weights[season - 1][1:] * 2 - 5
    disease_cases = disease_cases_2 + scaled_rainfall * 0.5
    disease_cases = apply_sigmoid_and_poisson_projection_with_capping(disease_cases, population)

