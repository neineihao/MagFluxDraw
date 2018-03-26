import numpy as np
import math
import matplotlib.pyplot as plt

def change(m):
    number = m.size
    if number <= 2:
        return m
    c_m = swift_matrix(m)
    mid = number // 2
    left = change(c_m[0:mid])
    right = change(c_m[mid:])
    return np.concatenate((left, right))

def swift_matrix(m):
    size = m.size
    result = np.zeros(size)
    for i in range(size):
        rem = i % 2
        quo = i // 2
        position = rem * size // 2 + quo
        result[position] = m[i]
    return result

def fft_sampling(time, signal):
    fft_result = np.fft.fft(signal) / len(signal)
    real = fft_result.real
    imag = fft_result.imag
    return real, imag

def extract_fre_data(data):
    size = data.size
    h_size = size // 2
    constant = data[0]
    m = data[1:h_size]
    reverse_m = data[h_size + 1:][::-1]
    return constant, m, reverse_m

def fft_analysis(time ,signal):
    fre = np.arange(1, time.size/2 , 1)
    real, imag = fft_sampling(time, signal)
    constant, real_m, real_reverse_m = extract_fre_data(real)
    cos = np.abs(real_m + real_reverse_m)
    imag_con, imag_m, imag_reverse_m = extract_fre_data(imag)
    sin =  np.abs(imag_reverse_m - imag_m)
    return fre, constant, sin, cos

def plot_init():
    plt.figure(1)
    plt.subplot(111)


def plot_2D(x, y):
    plt.plot(x, y)

def plot_show():
    plt.show()


if __name__ == '__main__':
    print("Hello world !!")
    test_list = np.arange(0, 8, 1)
    constant, m, reverse_m = extract_fre_data(test_list)
    time = np.arange(- np.pi, np.pi, np.pi / 16)
    cos_wave = 3 * np.cos(3 * time) + 4 * np.cos(6 * time)
    sin_wave = 6 * np.sin(4 * time)
    signal = cos_wave + sin_wave + 3
    fre, constant, sin, cos = fft_analysis(time, signal)
    plot_init()
    plot_2D(fre, cos)
    plot_2D(fre, sin)
    plot_show()