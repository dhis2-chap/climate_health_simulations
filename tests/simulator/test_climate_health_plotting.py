import numpy as np

from simulator.ClimateHealth import ClimateHealth


def test_climate_health_plotting():
    rainfall = np.random.uniform(0,4, 10)
    temp = np.random.uniform(0,4, 10)
    disease_cases = np.random.poisson(np.exp(rainfall + temp))
    climate_health_data = ClimateHealth(rainfall, disease_cases, 0, temp)
    climate_health_data.plot_data()