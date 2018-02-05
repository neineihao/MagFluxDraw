import numpy as np
import logging
import matplotlib.pyplot as plt
from MagFluxSimulate import calculate_amplitude, degree_setting
from matplotlib.animation import FuncAnimation


class Animate4Line(object):
    def __init__(self, ax, color, label, x_data):
        self.success = 0
        self.x_data = x_data
        self.ax = ax
        self.lines = []
        for i, color_item in enumerate(color):
            color_setting = '{}-'.format(color_item)
            self.lines.append(ax.plot([], [], color_setting, label=label[i])[0])
        self.lines = tuple(self.lines)
        self.width = (x_data.max() - x_data.min()) / x_data.size
        # self.title = "When Rotating {} degree"

    def set_rotate_degree(self, degree_default, vary_matrix):
        self.degree_default = degree_default
        self.vary_matrix = vary_matrix

    def set_dipole_position(self, dipole_position):
        self.dipole_position = dipole_position

    def set_sensor_position(self, sensor_position):
        self.sensor_position = sensor_position

    def setting(self,y_high):
        self.ax.set_ylim(-y_high, y_high)
        self.ax.set_xlim(self.x_data.min(), self.x_data.max())
        self.ax.grid(True)
        self.ax.set_title("The position of dipole, sensor = {}, {}\n The rotating vary matrix = {}"
                          .format(self.dipole_position, self.sensor_position, self.vary_matrix))

    def init(self):
        self.success = 0
        for i,item in enumerate(self.lines):
            item.set_data([],[])
        # self.ax.set_xlabel(self.label.format(self.success))
        return self.lines

    def __call__(self, i):
        if i == 0:
            return self.init()
        self.success += 1
        degree_matrix = degree_setting(self.degree_default, self.vary_matrix, self.success)
        rotate_result= calculate_amplitude(degree_matrix, self.dipole_position, self.sensor_position,self.x_data)
        result_dict = draw_data_package(rotate_result, self.x_data, self.width)
        for index, (key, value) in enumerate(result_dict.items()):
            self.lines[index].set_data(self.x_data, value)
        print("Degree : {}".format(self.success))
        # self.ax.set_xlabel(self.label.format(self.success))
        return self.lines

class Fourier_Package():
    def __init__(self, signal, x_data, width, f):
        self.signal = signal
        self.x_data = x_data
        self.width = width
        self.f = f

    def analysis(self):
        self.cos = integral(self.signal * np.cos(self.f * self.x_data), self.width) / np.pi
        self.sin = integral(self.signal * np.sin(self.f * self.x_data), self.width) / np.pi
        self.a0 = integral(self.signal, self.width) / (2 * np.pi)

    def show(self):
        logging.info("The coefficient of (constant,  cos, sin): ({}, {}, {})".format(
            self.a0, self.cos, self.sin))

    def cos_component(self):
        return self.cos * np.cos(self.f * self.x_data)

    def sin_component(self):
        return self.sin * np.sin(self.f * self.x_data)

    def constant_component(self):
        return self.a0 * np.ones(self.x_data.size)


def square_sum(mag_result):
    row, column = mag_result.shape
    total = np.zeros(column)
    for i in range(row):
        total += mag_result[i, :] ** 2
    return total

def integral(y_data, width):
    result = 0
    for i in range(len(y_data)):
        if i == 0:
            continue
        else:
            result += (y_data[i-1] + y_data[i]) / 2 * width
    return result


def test_fourier():
    data_number = 1000
    upper, lower = np.pi, -np.pi
    x_axis = np.linspace(lower, upper, data_number)
    width = (upper - lower) / data_number
    signal = 4 +  5 * np.cos(x_axis) + 3 * np.sin(x_axis)
    fourier_signal = Fourier_Package(signal, x_axis, width, 1)
    fourier_signal.analysis()
    fourier_signal.show()
    fig, ax = plt.subplots(1,1)
    ax.plot(x_axis, signal, label='signal')
    ax.plot(x_axis, fourier_signal.cos_component(), label='cos')
    ax.plot(x_axis, fourier_signal.sin_component(), label='sin')
    ax.plot(x_axis, fourier_signal.constant_component(), label='constant')
    ax.grid(True)
    ax.set_title("Test for Fourier Series")
    ax.legend()
    plt.show()

    # result = integral(signal * np.cos(x_axis), width) / np.pi
    # print("The result of integral is {}".format(result))

def draw_data_package(mag_result, x_data, width):
    result_dict = {}
    row, column = mag_result.shape
    name_list = ['Bx', 'By', 'Bz']
    temp_total = np.zeros(column)
    for i in range(row):
        result_dict[name_list[i]] = np.abs(mag_result[i, :])
        temp_total += result_dict[name_list[i]] ** 2
    result_dict['Sum'] = temp_total
    fourier_signal = Fourier_Package(temp_total, x_data, width, 2)
    fourier_signal.analysis()
    fourier_signal.show()
    result_dict['Cos2w'] = fourier_signal.cos_component()
    result_dict['Sin2w'] =  fourier_signal.sin_component()
    result_dict['Constant'] = fourier_signal.constant_component()

    return result_dict

def animation_draw():
    fig, ax = plt.subplots()
    dipole_position = np.array([0, 0, 0])
    sensor_position = np.array([0.4, 0.2, 0.8])
    degree_default = np.array([0, 0, 0])
    vary_matrix = np.array([1, 1, 1])
    time = np.linspace(- np.pi , np.pi , 1000)
    color_list = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    label_list = ['Bx', 'By', 'Bz', 'Sum', 'Cos2w', 'Sin2w', 'Constant']
    file_name=''

    al = Animate4Line(ax, color_list, label_list, time)
    al.set_dipole_position(dipole_position)
    al.set_sensor_position(sensor_position)
    al.set_rotate_degree(degree_default, vary_matrix)
    al.setting(10)
    anim = FuncAnimation(fig, al, frames=np.arange(360), init_func=al.init,
                         interval=50, blit=True)
    if file_name:
        anim.save("{}.gif".format(file_name), writer='imagemagick',dpi=80)
    plt.legend()
    plt.show()

def test():
    test_np = np.ones(5)
    print("The size of the {} : {}".format(type(test_np.size), test_np.size))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # test_fourier()
    # test()
    animation_draw()