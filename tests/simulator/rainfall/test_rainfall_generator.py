from simulator.rainfall.RealisticRainfallGenerator import RealisticRainfallGenerator
from simulator.rainfall.SyntheticRainfallGenerator import SyntheticRainfallGenerator


def test_realistic_rainfall_generator():
    rainfall_generator = RealisticRainfallGenerator()
    rainfall = rainfall_generator.generate(10)
    assert len(rainfall) == 10
    assert all([0 <= r <= 4 for r in rainfall])
    print(rainfall)

def test_generate_season_weights():
    rainfall_generator = SyntheticRainfallGenerator()
    weights = rainfall_generator.generate_season_weights()
    print(weights)
    print(weights.sum())