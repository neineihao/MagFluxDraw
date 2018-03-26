from MagFluxSimulate import Animate4Line
from Batterfly import fft_analysis
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt



class FrequencyAnalysis(Animate4Line):
    def plot_setting(self,y_high):
        self.ax.set_ylim(-y_high, y_high)
        self.ax.set_xlim(self.x_fre.min(), self.x_fre.max())
        self.ax.grid(True)
        self.ax.set_title("The Result of Fourier Analysis")

    def set_fre_data(self):
        rotate_result = self.calculate_data()
        result_list = self.package_data(rotate_result)
        for index, (key, value) in enumerate(result_list):
            self.lines[index].set_data(self.x_fre, value)

    def package_data(self, data):
        result_list = result_package(data, self.x_data)
        return result_list

    def __call__(self, i):
        if i == 0:
            return self.init()
        self.success += 1
        r = 1
        deg = np.deg2rad(self.success)
        self.sensor_position = np.array([r * np.cos(deg), r * np.sin(deg), 0])
        self.set_fre_data()
        print("Degree : {}".format(self.success))

        # self.ax.set_xlabel(self.label.format(self.success))
        return self.lines


def result_package(mag_result, time):
    result_list = []
    row, column = mag_result.shape
    # name_list = ['cos', 'sin', 'contant']
    temp_total = np.zeros(column)
    for i in range(row):
        temp_total += mag_result[i, :] ** 2
    fre, constant, sin, cos = fft_analysis(time, temp_total)
    result_list.append(('cos', cos))
    result_list.append(('sin', sin))
    result_list.append(('constant', constant * np.ones(cos.size)))
    return result_list

def test():
    list = []
    for i in range(10):
        list.append((i,str(i)))
    for i, (key, value) in enumerate(list):
        print("The {}th item: key, value{}, {}".format(i, key, value))
    for i in range(360):
        cos = np.cos(np.deg2rad(i))
        sin = np.sin(np.deg2rad(i))
        print("sin, cos = ({}, {})".format(sin, cos))
    print(np.array([1, 3, 1]))

def animation_draw(file_name=''):
    fig, ax = plt.subplots()
    dipole_position = np.array([0, 0, 0])
    sensor_position = np.array([0, 1, 0])
    degree_default = np.array([0, 0, 0])
    vary_matrix = np.array([0, 0, 1])
    time = np.arange(-np.pi, np.pi, np.pi / 16)
    color_list = ['b', 'r', 'g']
    label_list = ['cos', 'sin', 'constant']

    al = FrequencyAnalysis(ax, color_list, label_list, time)
    # al = FourierAnimate(ax, color_list, label_list, time)
    al.set_dipole_position(dipole_position)
    al.set_sensor_position(sensor_position)
    al.set_rotate_degree(degree_default, vary_matrix)
    al.plot_setting(5)
    anim = FuncAnimation(fig, al, frames=np.arange(360), init_func=al.init,
                         interval=50, blit=True)
    if file_name:
        anim.save("{}.gif".format(file_name), writer='imagemagick',dpi=80)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    print("Hello world")
    # test()
    animation_draw()