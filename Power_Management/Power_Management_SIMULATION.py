import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
pd.options.mode.chained_assignment = None


def plot_fig(df):
    PV_signal = df['PV']
    PL_signal = df['Load']
    PG_signal = df['Grid']
    PB_signal = df['Battery']
    PFC_signal = np.zeros(df.shape[0])
    plt.figure(figsize = (12, 8))
    plt.plot(PV_signal, linestyle='-', label = 'PV')
    plt.plot(PL_signal, linestyle='-', label = 'Load')
    plt.plot(PG_signal, linestyle='-', label = 'Grid')
    plt.plot(PB_signal, linestyle='-', label = 'Battery')
    plt.plot(PFC_signal, linestyle='-', label = 'FC')

    # Adding title and labels
    plt.title('Result')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')

    plt.grid(True)
    plt.show()

def calculate_signals(df, SoC, connected):
    SoC_max = 90
    SoC_min = 10
    for i in range(df.shape[0]):
        SoC = SoC - (100 / df.shape[0])
        if SoC <= SoC_max:
            if SoC_min <= SoC:
                df['Battery'][i] = df['PV'][i] - df['Load'][i]
            else:
                if connected == True:
                    df['Battery'][i] = df['PV'][i] + df['Grid'][i] - df['Load'][i]
                else:
                    df['Battery'][i] = df['PV'][i] + 0 - df['Load'][i]
        else:
            if df['PV'] <= df['Load']:
                df['Battery'][i] = df['PV'][i] - df['Load'][i]
            else:
                df['Load'][i] = df['PV'][i]
        df['Grid'] = df['Battery'] + df['Load'] - df['PV']
    return df

def main():
    # Read csv file
    df = pd.read_csv('./Combined_PV_Load_data.csv')
    df['Battery'] = np.zeros(df.shape[0])
    df['Grid'] = np.zeros(df.shape[0])

    # calculate parameters and plot them
    df = calculate_signals(df, 90, True)
    plot_fig(df)


if __name__ == "__main__":
    main()