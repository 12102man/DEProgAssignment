from matplotlib.figure import Figure
from methods import *


class Plotter:
    def __init__(self, title):
        self.figure = Figure(figsize=(5, 5), dpi=70)
        self.figure.suptitle(title)

    def add_graph(self, method):
        a = self.figure.add_subplot(111)
        a.plot(method.x_array, method.y_array, label=method.name)
        a.legend(loc='upper left')

    def add_error_graph(self, errors, method):
        a = self.figure.add_subplot(111)
        a.plot(errors.x_array, errors.y_array[method], label=method)
        a.legend(loc='upper left')


class MagicSolver:
    def __init__(self, x0, y0, X, N):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        self.solutions = {}
        self.find_solution()

    def find_solution(self):
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
        plotter_methods = Plotter('Graphs')
        # Plotting methods
        plotter_methods.add_graph(self.solutions['euler'])
        plotter_methods.add_graph(self.solutions['improved_euler'])
        plotter_methods.add_graph(self.solutions['exact'])
        plotter_methods.add_graph(self.solutions['runge_kutta'])

        return plotter_methods

    def find_max_error(self, method):
        x_array = self.solutions[method].x_array
        result_list = []
        for i in range(len(x_array)):
            result_list.append(abs(self.solutions['exact'].y_array[i] - self.solutions[method].y_array[i]))
        return max(result_list)


class ErrorAnalysis:
    def __init__(self, x0, y0, X, N):
        self.x_array = []
        self.y_array = {}
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        for i in range(N):
            self.x_array.append(i)

    def find_error(self, method):
        self.y_array[method] = []
        for i in range(1, self.N + 1):
            solution = MagicSolver(self.x0, self.y0, self.X, i)
            self.y_array[method].append(solution.find_max_error(method))
