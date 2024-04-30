import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

input_signals = []

def filter_contract_capacity(signal_data):
    amplitude_threshold = 1500
    input_signals.append(signal_data)

    if len(input_signals) >= 20:
        # predict the next stage
        times = []
        for i in range(len(input_signals)):
            times.append(i)
        X = np.array(input_signals).reshape(-1,1)
        y = np.array(times)
        model = LinearRegression()
        model.fit(X, y)

        predict_data = model.predict(np.array(signal_data).reshape(-1,1))
        if predict_data > amplitude_threshold:
            print("Fail")
        else:
            print("Success")

    if len(input_signals) >= 15:
        # apply filter
        filtered_signal = np.where(np.abs(signal_data) > amplitude_threshold, 0, 1)
        return filtered_signal

def main():
    df = pd.read_csv('./PVtest.csv')
    for i in range(df.shape[0]):
        filtered_signal = filter_contract_capacity(df['PV'][i])
        print(filtered_signal)

if __name__ == "__main__":
    main()

