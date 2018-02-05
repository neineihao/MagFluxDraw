import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
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

        # self.title = "When Rotating {} degree"

    def set_rotate_degree(self, degree_default, vary_matrix):
        self.degree_default = degree_default
        self.vary_matrix = vary_matrix

    def set_dipole_position(self, dipole_position):
        self.dipole_position = dipole_position

    def set_sensor_position(self, sensor_position):
        self.sensor_position = sensor_position

    def plot_setting(self,y_high):
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

    def set_data(self):
        rotate_result = self.calculate_data()
        result_dict = self.package_data(rotate_result)
        for index, (key, value) in enumerate(result_dict.items()):
            self.lines[index].set_data(self.x_data, value)

    def calculate_data(self):
        degree_matrix = degree_setting(self.degree_default, self.vary_matrix, self.success)
        rotate_result = calculate_amplitude(degree_matrix, self.dipole_position, self.sensor_position, self.x_data)
        return rotate_result

    def package_data(self, data):
        result_dict = result_package(data)
        return result_dict

    def __call__(self, i):
        if i == 0:
            return self.init()
        self.success += 1
        self.set_data()
        print("Degree : {}".format(self.success))

        # self.ax.set_xlabel(self.label.format(self.success))
        return self.lines

def degree_setting(degree_default, vary_matrix, vary_value):
    return vary_matrix * vary_value + degree_default

def dipole_mag(dipole_position, sensor_position, dipole_signal):
    Bt = 0.03
    position_matrix = sensor_position - dipole_position
    t_position_matrix = position_matrix.reshape(1, 3)
    r = ((position_matrix ** 2).sum()) ** 1/2
    child = position_matrix.reshape(3,1).dot(t_position_matrix.dot(dipole_signal))
    result = Bt * (3 * child / (r ** 5) - dipole_signal / (r ** 3))

    return result

def print_shape(numpy_matrix, name):
    print("The size of {} : {}".format(name, numpy_matrix.shape))

# def rotate_mag_flux(x_degree, y_degree, z_degree):
def rotate_mag_flux(degree_matrix):
    x_degree, y_degree, z_degree = degree_matrix[0], degree_matrix[1], degree_matrix[2]
    # print_shape(matrix.transpose(), 'Matrix')
    rotateX_matrix = np.array([(1, 0, 0), (0, cos(x_degree), -sin(x_degree)), (0, sin(x_degree), cos(x_degree))])
    rotateY_matrix = np.array([(cos(y_degree), 0, sin(y_degree)), (0, 1, 0), (-sin(y_degree), 0, cos(y_degree))])
    rotateZ_matrix = np.array([(cos(z_degree), -sin(z_degree), 0), (sin(z_degree), cos(z_degree), 0),(0, 0, 1)])
    rotate_matrix = rotateX_matrix.dot(np.dot(rotateY_matrix, rotateZ_matrix))
    # print_shape(rotate_matrix,"Rotate Matrix")
    return rotate_matrix

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
        result_dict[name_list[i]] = mag_result[i, :]
        temp_total += result_dict[name_list[i]] ** 2
    result_dict['CombineSum'] =  (mag_result[0, :] + mag_result[1, :] + mag_result[2, :]) ** 2
    result_dict['SplitSum'] = temp_total
    return result_dict

def calculate_amplitude(degree_matrix, dipole_position, sensor_position,
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
    # signal_array[0, :] = np.zeros(data_number)
    signal_array[0, :] = np.sin(time_range)
    signal_array[1, :] = np.cos(time_range)

    # signal_array[1, :] = np.zeros(data_number)
    signal_array[2, :] = np.zeros(data_number)
    # signal_array[2, :] = np.sin(time_range)
    B2signal = dipole_mag(dipole_position, sensor_position, signal_array)
    rotate_matrix = rotate_mag_flux(degree_matrix)
    rotate_result = np.dot(rotate_matrix, B2signal)
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

def animation_draw():
    fig, ax = plt.subplots()
    dipole_position = np.array([0, 0, 0])
    sensor_position = np.array([0, 1, 0])
    degree_default = np.array([0, 0, 0])
    vary_matrix = np.array([0, 0, 1])
    time = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    color_list = ['b', 'r', 'g', 'm', 'y']
    label_list = ['Bx', 'By', 'Bz', 'Split_Total', 'Combine_Total']
    file_name=''

    al = Animate4Line(ax, color_list, label_list, time)
    al.set_dipole_position(dipole_position)
    al.set_sensor_position(sensor_position)
    al.set_rotate_degree(degree_default, vary_matrix)
    al.plot_setting(20)
    anim = FuncAnimation(fig, al, frames=np.arange(360), init_func=al.init,
                         interval=50, blit=True)
    if file_name:
        anim.save("{}.gif".format(file_name), writer='imagemagick',dpi=80)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # test_function()
    # main()
    animation_draw()