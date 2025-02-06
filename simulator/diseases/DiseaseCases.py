from abc import ABC, abstractmethod
import numpy as np

from simulator.ClimateData import ClimateData


class DiseaseCases(ABC):
    @abstractmethod
    def generate(self, climate_data: ClimateData):
        pass

    def get_name(self):
        raise NotImplementedError("Subclasses must implement get_name method")
