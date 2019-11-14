import math
from sklearn.metrics import mean_squared_error


def get(true_values, predicted_values, error_method='mape'): # function to calculate the error
    error = 0

    if error_method == 'mape':
        # calculate the mean absolute percentage error
        error = (abs((true_values - predicted_values) / true_values).sum() / len(true_values)) * 100
        error = round(error, 3)

    if error_method == 'mse':
        # calculate the mean squared error
        error = round(math.sqrt(mean_squared_error(true_values, predicted_values)), 3)

    return error
