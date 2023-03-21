import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def load_from_file(file):
    raw = pd.read_csv(file)
    return raw


def save_to_file(df, filename):
    df.to_csv(filename, index=False)
    print('Successfully saved to file:', filename)


# 🥉 task
def calc_time_and_acceleration(df, frequency):
    period = 1 / frequency

    t = np.arange(0, len(df)) * period
    yf = df['ax'] + df['ay'] + df['az']

    df['time'] = t
    df['acc'] = yf

    df = df[['time', 'ax', 'ay', 'az', 'acc']]

    plt.plot(t, yf)
    plt.show()

    save_to_file(df, 'out.csv')


# 🥈 task
def calc_fft_for_axes(df, frequency):
    window = np.hamming(len(df['ax']))  # okno czasowe
    fft_ax = np.abs(np.fft.rfft(df['ax'] * window))  # wartość FFT
    fft_ay = np.abs(np.fft.rfft(df['ay'] * window))  # wartość FFT
    fft_az = np.abs(np.fft.rfft(df['az'] * window))  # wartość FFT
    freq = np.fft.rfftfreq(len(df['ax']), 1 / frequency)

    plt.subplot(3, 1, 1)
    plt.plot(freq, fft_ax)

    plt.subplot(3, 1, 2)
    plt.plot(freq, fft_ay)

    plt.subplot(3, 1, 3)
    plt.plot(freq, fft_az)

    plt.show()

    result_df = pd.DataFrame(zip(freq, fft_ax, fft_ay, fft_az), columns=['freq', 'fft_ax', 'fft_ay', 'fft_az'])
    save_to_file(result_df, 'out2.csv')

    # czestotliwość wiodąca
    print("f-wiodąca ax = ", max(fft_ax))
    print("f-wiodąca ay = ", max(fft_ay))
    print("f-wiodąca az = ", max(fft_az))


data = load_from_file("data.csv")
fs = 6666
calc_time_and_acceleration(data, fs)
calc_fft_for_axes(data, fs)
