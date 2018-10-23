from matplotlib.figure import Figure
from methods import *


class Plotter:
    def __init__(self, title):
        self.figure = Figure(dpi=70)
        self.figure.suptitle(title)

    def add_graph(self, method):
        """
        Method that adds the graph onto a Plotter
        :param method: name of method used
        :return:
        """
        a = self.figure.add_subplot(111)
        a.set_xlabel('x values')
        a.set_ylabel('y values')
        a.plot(method.x_array, method.y_array, label=method.name)
        a.legend(loc='upper left')

    def add_error_graph(self, errors, method):
        """
        Method that adds the error graph onto a Plotter
        :param errors: ErrorAnalysis
        :param method: name of method used
        :return
        """
        a = self.figure.add_subplot(111)
        a.set_xlabel('N')
        a.set_ylabel('Maximum error')
        a.plot(errors.x_array, errors.y_array[method], label=method)
        a.legend(loc='upper left')

    def add_local_error_graph(self, x, y, method):
        """
        Method that adds the error graph onto a Plotter
        :param x: x-values of graph
        :param y: y-values of graph
        :param method:  name of method used
        :return:
        """
        a = self.figure.add_subplot(111)
        a.set_xlabel('x values')
        a.set_ylabel('cError')
        a.plot(x, y, label=method)
        a.legend(loc='upper left')


class MagicSolver:
    """
    This class is used for checking all solutions
    for each of methods:
    - exact
    - Runge-Kutta
    - Euler
    - Improved Euler
    """

    def __init__(self, x0, y0, X, N):
        """
        Initializer
        :param x0: x0
        :param y0: y0
        :param X: X
        :param N: N
        """
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        self.solutions = {}
        self.find_solution()

    def find_solution(self):
        """
        Calculate solutions of each of methods and save to solutions dictionary
        :return:
        """
        euler = Euler(int(self.x0), int(self.y0), int(self.X),
                      int(self.N))
        improved_euler = ImprovedEuler(int(self.x0), int(self.y0), int(self.X),
                                       int(self.N))
        exact = Exact(int(self.x0), int(self.y0), int(self.X),
                      int(self.N))
        runge_kutta = RungeKutta(int(self.x0), int(self.y0), int(self.X),
                                 int(self.N))

        self.solutions['euler'] = euler
        self.solutions['improved_euler'] = improved_euler
        self.solutions['exact'] = exact
        self.solutions['runge_kutta'] = runge_kutta

    def generate_plot(self):
        """
        Method that generates a plot of solutions calculated
        :return: Plotter
        """
        plotter_methods = Plotter('Graphs')
        # Plotting methods
        plotter_methods.add_graph(self.solutions['euler'])
        plotter_methods.add_graph(self.solutions['improved_euler'])
        plotter_methods.add_graph(self.solutions['exact'])
        plotter_methods.add_graph(self.solutions['runge_kutta'])

        return plotter_methods

    def generate_error_array(self, method):
        """
        Method that generates an array of y-values for error
        :param method: name of specific method used
        :return: list of y-values
        """
        x_array = self.solutions[method].x_array
        result_list = []
        for i in range(len(x_array)):
            result_list.append(abs(self.solutions['exact'].y_array[i] - self.solutions[method].y_array[i]))
        return result_list

    def find_max_error(self, method):
        """
        Method that finds the highest error in the current method
        :param method: name of specific method used
        :return: max value
        """
        return max(self.generate_error_array(method))

    def create_local_error_graph(self):
        """
        Method that generates a plot of local errors calculated

        :return: Plotter
        """
        plot = Plotter('Local errors')
        for method in ('euler', 'improved_euler', 'runge_kutta'):
            x_array = self.solutions['euler'].x_array
            result_list = []
            for i in range(len(x_array)):
                result_list.append(abs(self.solutions['exact'].y_array[i] - self.solutions[method].y_array[i]))
            plot.add_local_error_graph(x_array, result_list, method)
        return plot


class ErrorAnalysis:
    """
    ErrorAnalysis is a class used for plotting
    a graph of changing error in comparison with N.
    """

    def __init__(self, x0, y0, X, N):
        """
        Initializer
        :param x0: x0
        :param y0: y0
        :param X: X
        :param N: X
        """
        self.x_array = []  # Array of x-values
        self.y_array = {}  # Dictionary of different y-values, depending on a method
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        for i in range(1, N + 1):  # Fill x_array with values from 1 to N
            self.x_array.append(i)

    def find_error(self, method):
        self.y_array[method] = []   # Initialize empty array
        for i in self.x_array:      # Fill it with values
            solution = MagicSolver(self.x0, self.y0, self.X, i)
            self.y_array[method].append(solution.find_max_error(method))

    def generate_plot(self):
        """
        Method that generates a plot of errors
        :return: Plotter
        """
        plotter_errors = Plotter('Errors from N')
        plotter_errors.add_error_graph(self, 'euler')
        plotter_errors.add_error_graph(self, 'improved_euler')
        plotter_errors.add_error_graph(self, 'runge_kutta')

        return plotter_errors
