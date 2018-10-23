from math import *


class Euler:
    def __init__(self, x0, y0, X, N):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.N = N
        self.delta = (X - x0) / N
        self.x_array = [x0]
        self.y_array = [y0]
        self.name = 'Euler'
        self.evaluate()

    def evaluate(self):
        i = self.x0
        while i < self.X:
            x = i
            y = self.y_array[-1]
            self.x_array.append(i)
            self.y_array.append(y + self.delta * self.calculate_right_part(x, y))
            i += self.delta

    def calculate_right_part(self, x, y):
        return 2 * x * y + 5 - x * x


class ImprovedEuler(Euler):

    def __init__(self, x0, y0, X, N):
        Euler.__init__(self, x0, y0, X, N)
        self.name = 'Improved Euler'
        self.evaluate()

    def evaluate(self):
        i = self.x_array[-1]
        while i < self.X:
            x = i
            y = self.y_array[-1]
            h = self.delta

            f = self.calculate_right_part(x, y)
            x_delta = x + (h / 2)
            y_delta = y + (h / 2) * f

            y_new = y + h * self.calculate_right_part(x_delta, y_delta)
            self.y_array.append(y_new)
            self.x_array.append(i)

            i += self.delta


class Exact(Euler):
    def __init__(self, x0, y0, X, N):
        Euler.__init__(self, x0, y0, X, N)
        self.name = 'Exact'
        self.evaluate()

    def evaluate_constants(self):
        y0 = self.y0
        x0 = self.x0
        return y0 / exp(x0 * x0) + 9 / 4 * sqrt(pi) * erf(x0) + x0 / (2 * exp(x0 * x0))

    def evaluate(self):
        i = self.x_array[-1]
        while i < self.X:
            x = i

            y_new = self.evaluate_constants() * sqrt(pi) * exp(x * x) * erf(x) + exp(x * x) + x / 2
            self.y_array.append(y_new)
            self.x_array.append(i)

            i += self.delta

    def erf(x):
        # save the sign of x
        sign = 1 if x >= 0 else -1
        x = abs(x)

        # constants
        a1 = 0.254829592
        a2 = -0.284496736
        a3 = 1.421413741
        a4 = -1.453152027
        a5 = 1.061405429
        p = 0.3275911

        # A&S formula 7.1.26
        t = 1.0 / (1.0 + p * x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * exp(-x * x)
        return sign * y  # erf(-x) = -erf(x)


class Runge_Kutta(Euler):
    def __init__(self, x0, y0, X, N):
        Euler.__init__(self, x0, y0, X, N)
        self.name = 'Runge-Kutta (4th order)'
        self.evaluate()

    def evaluate(self):
        x = self.x_array[-1]
        h = self.delta
        while x < self.X:
            y = self.y_array[-1]
            k1 = self.calculate_right_part(x, y)
            k2 = self.calculate_right_part(x + h / 2, y + (h * k1 / 2))
            k3 = self.calculate_right_part(x + h / 2, y + (h * k2 / 2))
            k4 = self.calculate_right_part(x + h, y + h * k3)

            y_new = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

            self.y_array.append(y_new)
            self.x_array.append(x)

            x += h


class Error:
    def __init__(self, exact, method):
        self.x_array = method.x_array
        self.y_array = []
        self.compare(exact, method)
        self.name = method.name

    def compare(self, exact, method):
        for i in range(len(self.x_array)):
            self.y_array.append(abs(exact.y_array[i] - method.y_array[i]))
