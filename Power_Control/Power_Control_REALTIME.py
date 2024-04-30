import matplotlib.pyplot as plt
import numpy as np

def plot_fig_original(freq, percentage1, percentage2):
    # Create a linear plot for the dReg adjustment curve
    plt.figure(figsize=(10, 6))
    plt.plot(freq, percentage1, marker='o', linestyle='-')
    plt.plot(freq, percentage2, marker='o', linestyle='-')

    # Adding title and labels
    plt.title('dReg Adjustment Curve')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('dReg (kW)')

    plt.grid(True)
    plt.show()

def plot_fig(freq, percentage1, percentage2):
    # Create a linear plot for the dReg adjustment curve
    plt.figure(figsize=(10, 6))
    plt.plot(freq, (percentage1 + percentage2) / 2, marker='o', linestyle='-')

    # Adding title and labels
    plt.title('dReg Adjustment Curve')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('dReg (kW)')

    plt.grid(True)
    plt.show()

def get_dreg_output(freq_value, freq_array, percentage1_array, percentage2_array):
    dreg1 = np.interp(freq_value, freq_array, percentage1_array)
    dreg2 = np.interp(freq_value, freq_array, percentage2_array)
    return dreg1, dreg2

def calculate(input_frequency):
    # Given values from the table
    freqs = np.array([59.75, 59.86, 59.98, 60.02, 60.14, 60.25])  # Frequencies
    percentages1 = np.array([1, 0.52, 0.09, 0.09, -0.52, -1])  # Corresponding dReg percentages
    percentages2 = np.array([1, 0.52, -0.09, -0.09, -0.52, -1])  # Corresponding dReg percentages

    # plot_fig_original(freqs, percentages1, percentages2) # plot the original dReg figure
    # plot_fig(freqs, percentages1, percentages2) # plot the calculated dReg figure
    dreg1, dreg2 = get_dreg_output(input_frequency, freqs, percentages1, percentages2)
    print(f"dReg value from for frequency {input_frequency} Hz is about: {round((dreg1 + dreg2) / 2)}kW")

def main():
    calculate(float(input("Enter a frequency value: ")))

if __name__ == "__main__":
    main()