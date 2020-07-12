from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from stocker.error import get


def data(df, features=[]):
    columns = ['Close']
    if len(features) > 0:
        for i in range(len(features)):
            columns.append(features[i])

    df = df[columns]

    return df


def get_lstm_input(data, steps=1):
    samples = []
    for i in range(steps, data.shape[0]):
        features = []
        for j in range(steps):
            features.append(data[i - steps + j, :])
        features.append(data[i, :])
        samples.append(features)

    features = []
    for j in range(steps + 1):
        features.append(data[-1, :])

    samples.append(features)
    samples = np.asarray(samples)
    return samples


def run(df, features=[], steps=1, training=0.9, error_method='mape'):

    new_df = data(df, features)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(new_df)
    reframed = get_lstm_input(scaled, steps)

    rows = round(len(df) * training)

    train = reframed[:rows, :, :]
    test = reframed[rows:, :, :]

    train_x, train_y = train[:, :steps, :], train[:, steps, 0]
    test_x, test_y = test[:, :steps, :], test[:-1, steps, 0]

    # designing and fitting network
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_x.shape[1], train_x.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    model.fit(train_x, train_y, epochs=100, batch_size=70, verbose=0)

    mod1 = rows + steps - 1
    mod2 = rows + steps

    # generate a prediction
    prediction = model.predict(test_x)
    new_scaled = np.copy(scaled)
    for x in range(mod1, new_scaled.shape[0]):
        new_scaled[x, 0] = prediction[x-mod1]

    # invert normalized values
    # for predictions
    y_predicted = scaler.inverse_transform(new_scaled)
    y_predicted = y_predicted[mod1:, 0]
    # for real values
    y = scaler.inverse_transform(scaled)
    y = y[mod2:, 0]

    finalprice = round(y_predicted[-1], 2)
    y_predicted = y_predicted[:-1]

    error = get(y, y_predicted, error_method)

    result = [finalprice, error]

    return result, y_predicted, new_df[-len(y):]

