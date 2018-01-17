import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
from matplotlib.animation import FuncAnimation


class Animate4Line(object):
    def __init__(self, ax, color, label, dipole_position, sensor_position, x_data):
        self.success = 0
        self.x_data = x_data
        self.ax = ax
        self.dipole_position = dipole_position
        self.sensor_position = sensor_position
        self.lines = []
        for i, color_item in enumerate(color):
            color_setting = '{}-'.format(color_item)
            self.lines.append(ax.plot([], [], color_setting, label=label[i])[0])


        # self.title = "When Rotating {} degree"

    def setting(self,y_high):
        self.ax.set_ylim(0, y_high)
        self.ax.set_xlim(-2 * np.pi, 2 * np.pi)
        self.ax.grid(True)
        self.ax.set_title("Variation of Signal Amplitude")

    def init(self):
        self.success = 0
        for i,item in enumerate(self.lines):
            item.set_data([],[])

        return self.lines

    def __call__(self, i):
        if i == 0:
            return self.init()
        self.success += 1
        rotate_result= calculate_amplitude(self.success, 0, self.success, self.dipole_position, self.sensor_position,self.x_data)
        result_dict = result_package(rotate_result)
        for index, (key, value) in enumerate(result_dict.items()):
            self.lines[index].set_data(self.x_data, value)
        print("Degree : {}".format(self.success))

        return self.lines

def animation_simulate():
    dipole_position = np.array([0, 0, 0])
    sensor_position = np.array([1, 2, 3])
    time = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    color_list = ['b', 'r', 'g', 'm','y']
    label_list = ['Bx', 'By', 'Bz', 'Split_Total', 'Combine_Total']
    # animation_draw(color_list, dipole_position, sensor_position, time, file_name="./fig/line")
    animation_draw(color_list, label_list, dipole_position, sensor_position, time)



def animation_draw(color_list, label_list, dipole_position, sensor_position, time, file_name=""):
    fig, ax = plt.subplots()
    al = Animate4Line(ax, color_list, label_list, dipole_position, sensor_position, time)
    al.setting(200)

    anim = FuncAnimation(fig, al, frames=np.arange(360), init_func=al.init,
                         interval=50, blit=True)
    if file_name:
        anim.save("{}.gif".format(file_name), writer='imagemagick',dpi=80)
    plt.legend()
    plt.show()


def dipole_mag(dipole_position, sensor_position, dipole_signal):
    position_matrix = sensor_position - dipole_position
    t_position_matrix = position_matrix.reshape(1, 3)
    result = t_position_matrix.dot(dipole_signal)
    result = position_matrix.reshape(3,1).dot(result)
    return result

def print_shape(numpy_matrix, name):
    print("The size of {} : {}".format(name, numpy_matrix.shape))

def rotate_mag_flux(matrix, x_degree, y_degree, z_degree):
    # print_shape(matrix.transpose(), 'Matrix')
    rotateX_matrix = np.array([(1, 0, 0), (0, cos(x_degree), -sin(x_degree)), (0, sin(x_degree), cos(x_degree))])
    rotateY_matrix = np.array([(cos(y_degree), 0, sin(y_degree)), (0, 1, 0), (-sin(y_degree), 0, cos(x_degree))])
    rotateZ_matrix = np.array([(cos(z_degree), -sin(z_degree), 0), (sin(z_degree), cos(z_degree), 0),(0, 0, 1)])
    rotate_matrix = rotateX_matrix.dot(np.dot(rotateY_matrix, rotateZ_matrix))
    # print_shape(rotate_matrix,"Rotate Matrix")
    result_matrix = np.dot(matrix.transpose(), rotate_matrix)
    return result_matrix.transpose()

def two_dimension_plot(ax, xAxis, yAxis, line, color='b'):
    ax.plot(xAxis, yAxis, '{}-'.format(color), label=line)


def sin(theta):
    return np.sin(np.radians(theta))

def cos(theta):
    return np.cos(np.radians(theta))


def result_package(mag_result):
    result_dict = {}
    row, column = mag_result.shape
    name_list = ['Bx', 'By', 'Bz']
    temp_total = np.zeros(column)
    for i in range(row):
        result_dict[name_list[i]] = mag_result[i, :] ** 2
        temp_total += result_dict[name_list[i]]
    result_dict['Bsplit'] =  (mag_result[0, :] + mag_result[1, :] + mag_result[2, :]) ** 2
    result_dict['Btotal'] = temp_total
    return result_dict

def calculate_amplitude(x_degree, y_degree, z_degree, dipole_position, sensor_position,
                        time_range):
    """
    :param x_degree: The degree rotate along x-axis
    :param y_degree: The degree rotate along y-axis
    :param z_degree: The degree rotate along z-axis
    :param dipole_position: The position of dipole (The numpy matrix)
    :param sensor_position: The position of sensor (The numpy matrix)
    :return: The numpy matrix of y value
    """
    data_number = time_range.size
    signal_array = np.zeros((3, data_number))
    signal_array[0, :] = np.sin(time_range)
    signal_array[1, :] = np.cos(time_range)
    # signal_array[1, :] = np.zeros(data_number)
    signal_array[2, :] = np.zeros(data_number)
    # signal_array[2, :] = np.sin(time_range) + np.cos(time_range)
    B2signal = dipole_mag(dipole_position, sensor_position, signal_array)
    rotate_result = rotate_mag_flux(B2signal, x_degree, y_degree, z_degree)
    return rotate_result

def set_ax_data(ax, title='Title', xName='x-axis', yName='y-axis'):
    ax.set_title(title)
    ax.set_ylabel(xName)
    ax.set_xlabel(yName)
    ax.grid(True)

def main():
    fig = plt.figure()
    dipole_position = np.array([0, 0, 0])
    sensor_position = np.array([1, 2, 3])
    time = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    rotate_result = calculate_amplitude(30, 30, 30, dipole_position, sensor_position, time)
    result_dict = result_package(rotate_result)
    ax = fig.add_subplot(111)
    set_ax_data(ax)
    color_list = ['b', 'r', 'g', 'y']
    for index, (key, value) in enumerate(result_dict.items()):
        two_dimension_plot(ax, time, value, key, color= color_list[index])
    # two_dimension_plot(ax, time, By, color='r')
    # two_dimension_plot(ax, time, Bz, color='g')
    # two_dimension_plot(ax, time, Bx+By+Bz, color='y')
    plt.tight_layout()
    plt.legend()
    plt.show()

def test_function():
    test_array = np.ones((3,4)).shape
    print("The row, column : ({}, {})".format(test_array[0], test_array[1]))
    print(np.ones((3,4)))


if __name__ == '__main__':
    # test_function()
    # main()
    animation_simulate()