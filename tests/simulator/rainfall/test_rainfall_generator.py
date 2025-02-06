import numpy as np

from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from simulator.rainfall.SyntheticRainfallDependentOnSeasonGenerator import SyntheticRainfallDependentOnSeasonGenerator
from simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator


def test_realistic_rainfall_generator():
    rainfall_generator = RealisticRainfallGenerator()
    rainfall = rainfall_generator.generate(10)
    assert len(rainfall) == 10
    assert all([0 <= r <= 4 for r in rainfall])


def test_synthetic_rainfall_generator():
    rainfall_generator = SyntheticRainfallGenerator()
    rainfall = rainfall_generator.generate(10)
    assert np.argmax(rainfall) == len(rainfall) // 2

def test_synthetic_rainfall_dependent_on_season():
    n_time_points = 10
    rainfall_generator = SyntheticRainfallDependentOnSeasonGenerator()
    rainfall = rainfall_generator.generate(n_time_points)
    max_indices = np.argsort(rainfall)[-2:]
    min_indices = np.argsort(rainfall)[:2]
    assert np.allclose(rainfall[max_indices], 4.0, atol=0.3)
    assert np.allclose(rainfall[min_indices], 0.0, atol=1.1)



