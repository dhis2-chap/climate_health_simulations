import numpy as np
import plotly.express as px
import pandas as pd
from simulator.diseases.DiseaseCases import DiseaseCases


def test_disease_case_generator():
    rainfall = np.zeros(10)
    rainfall[10 // 2] = 4
    disease_cases = DiseaseCases()
    disease_cases = disease_cases.generate(rainfall, lag=3)
    max_rainfall_index = np.argmax(rainfall)
    max_disease_cases_index = np.argmax(disease_cases)
    fig = px.line(x=range(len(rainfall)), y=rainfall, title="Rainfall")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()
    assert max_disease_cases_index-max_rainfall_index == 3

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
    disease_cases = DiseaseCases()
    disease_cases = disease_cases.generate_autoregressive_dependent_of_rainfall(n_time_points, rainfall, population)
    fig = px.line(x=range(len(rainfall)), y=rainfall, title="Rainfall")
    fig.show()
    fig = px.line(x=range(len(disease_cases)), y=disease_cases, title="Disease Cases")
    fig.show()