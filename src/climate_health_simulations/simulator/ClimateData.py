from dataclasses import dataclass

import numpy as np


@dataclass
class ClimateData:
    rainfall: np.ndarray
    temperature: np.ndarray
    month: np.ndarray
    time_period: np.ndarray
    population: np.ndarray



