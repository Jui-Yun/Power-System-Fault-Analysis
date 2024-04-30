import numpy as np
import pandas as pd
from scipy.signal import firwin, lfilter

input_signal = []

def apply_lowpass_filter(signal):
    input_signal.append(float(signal))
    if len(input_signal) >= 5:
        input_signal_array = np.array(input_signal)

        # calculate filter parameter
        cutoff_freq = 10.0
        sampling_freq = 100.0
        filter_order = 30
        nyquist_freq = 0.5 * sampling_freq
        normalized_cutoff_freq = cutoff_freq / nyquist_freq
        filter_coefficients = firwin(filter_order, normalized_cutoff_freq)

        # apply filter
        filtered_signal = lfilter(filter_coefficients, 1.0, input_signal_array)
        return np.average(filtered_signal)
    else:
        return 0

def main():
    df = pd.read_csv('./PVtest.csv')
    for i in range(df.shape[0]):
        filtered_signal = apply_lowpass_filter(df['PV'][i])
        print(df['PV'][i] - filtered_signal)

if __name__ == "__main__":
    main()

