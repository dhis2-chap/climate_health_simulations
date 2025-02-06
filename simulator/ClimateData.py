from dataclasses import dataclass

import numpy as np


@dataclass
class ClimateData:
    rainfall: np.ndarray
    temperature: np.ndarray
    season: np.ndarray
    population: np.ndarray



