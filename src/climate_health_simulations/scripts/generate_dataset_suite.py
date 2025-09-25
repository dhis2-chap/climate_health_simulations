import os
import yaml
from climate_health_simulations.config.SimulationConfig import Config
from climate_health_simulations.config.config_variations.ConfigGenerator import ConfigGenerator
from climate_health_simulations.simulator.Simulator import Simulator
from pathlib import Path

def get_base_config():
    config = {
        'independent_variables': [
            {'type': 'rain', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'temperature', 'is_realistic': False, 'is_season_dependent': False},
            {'type': 'season', 'is_realistic': False},
        ],
        'dependent_variable': {
            'is_autoregressive': False,
            'explanatory_variables': [
                {'type': 'rain', 'lag': 3},
                {'type': 'temperature', 'lag': 3},
                {'type': 'season'}
            ],
            'population': 100},
        'n_time_points_train': 10,
        'n_time_points_test': 5
    }
    return Config(**config)


def save_simulation_config(config, simulation_config_path):
    with open(simulation_config_path, 'w') as f:
        yaml.dump(config.model_dump(), f)


def get_paths(dir_name, output_path):
    target_path = os.path.join(output_path, dir_name)
    os.makedirs(target_path, exist_ok=True)
    data_path = os.path.join(target_path, "simulated_data.csv")
    plot_path = os.path.join(target_path, "plot.html")
    simulation_config_path = os.path.join(target_path, 'simulation_config.yaml')
    return data_path, plot_path, simulation_config_path


def generate_datasets(output_path):
    configs = list(ConfigGenerator.generate_all(get_base_config()))
    for index, config in enumerate(configs[:10]):
        dir_name = f"config_{index}"
        data_path, plot_path, simulation_config_path = get_paths(dir_name, output_path)
        save_simulation_config(config, simulation_config_path)
        simulator = Simulator(config_path=simulation_config_path)
        climate_health = simulator.run()
        climate_health.save_data(data_path)
        climate_health.plot_data(plot_path)

project_root = Path(__file__).resolve().parents[3]
output_dir = project_root / "toy_simulations"

if __name__ == "__main__":
    print(project_root)
    generate_datasets(output_dir)

#if __name__ == '__main__':
   # generate_datasets("/Users/Halvard/Documents/GitHub/climate_health_simulations/toy_simulations")
    #generate_datasets("/Users/skanduri/Documents/Projects/climate_health/toy_simulations")
