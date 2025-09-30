import numpy as np
from scipy.special.cython_special import logit
from sklearn.preprocessing import StandardScaler


def generate_season_weights():  # maybe this has to be revisited at a later time point
    x = np.array(range(12))
    y = np.sin(x / 12 * 2 * np.pi)
    return y


def apply_lag(data, lag: int):
    return np.roll(data, lag)


def standardize_variable(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    return scaled_data.flatten()

def apply_sigmoid_scaling_to_cases(disease_cases, population):
    return np.int32((1 / (1 + np.exp(-disease_cases))) * population)

#TODO make the median and max_rate adjustable by arguments from classes further up
def apply_sigmoid_and_poisson_projection_with_capping(eta, population, median = 0.1, max_rate = 0.3):
    transformed_eta = eta + logit(median/max_rate) #adds a constant to adjust the median value
    disease_cases = apply_sigmoid_scaling_to_cases(transformed_eta, population) * max_rate #scales to set the max rate
    disease_cases = np.random.poisson(disease_cases)
    disease_cases[disease_cases > population] = population[disease_cases > population] #ensures the sampled value is below the population
    return disease_cases

