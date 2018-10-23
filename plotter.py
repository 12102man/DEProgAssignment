from matplotlib.figure import Figure


class Plotter:
    def __init__(self):
        self.figure = Figure(figsize=(5, 5), dpi=70)

    def add_graph(self, method):
        a = self.figure.add_subplot(111)
        a.plot(method.x_array, method.y_array, label=method.name)
        a.legend(loc='upper left')
