import numpy as np


def pure_deal_data(data, seq_len):
    result = []
    for index in range(len(data) - seq_len + 1):
        result.append(data[index: index + seq_len])
    result = normalise_windows(result)
    result = np.array(result)
    x_data = np.reshape(result, (result.shape[0], result.shape[1], 1))
    return x_data


def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data


def pure_predict(model, data):
    # Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
    predicted = model.predict(data)
    predicted = np.reshape(predicted, (predicted.size,))
    return predicted
