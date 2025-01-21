import numpy as np

from simulator.Simulator import Simulator


def test_simulate_realistic_linear_lag3_dependency():
    climate_health = Simulator(10, 3).simulate_realistic_rain_linear_lag3_dependency()
    data = climate_health.get_data()
    print(data)

def test_simulate_realistic_rain3_temp1_linear_dependency():
    climate_health = Simulator(10, 3, 1).simulate_realistic_rain3_temp1_linear_dependency()
    data = climate_health.get_data()
    print(data)

def test_simulate_autoregressive_independent_rainfall():
    n_time_points = 10
    population = np.ones(n_time_points) * 1000
    climate_health = Simulator(n_time_points, population=population, lag_rain=0).simulate_autoregressive_independent_rainfall()
    data = climate_health.get_data()
    print(data)