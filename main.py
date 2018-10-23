from tkinter import *
import methods as methods
import plotter as Plotter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class DE_App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('500x700')
        self.resizable(width=False, height=False)

        Label(self, text="DE App").place(x=200,y=0)

        Label(self, text="x0").grid(row=0)
        Label(self, text="y0").grid(row=1)
        Label(self, text="X").grid(row=2)
        Label(self, text="N").grid(row=3)

        self.x0_field = Entry(self, width=3)
        self.y0_field = Entry(self, width=3)
        self.X_field = Entry(self, width=3)
        self.N_field = Entry(self, width=3)

        self.x0_field.grid(row=0, column=1)
        self.y0_field.grid(row=1, column=1)
        self.X_field.grid(row=2, column=1)
        self.N_field.grid(row=3, column=1)
        b = Button(self, text="OK", command=self.calculate)
        b.grid(row=4, column=0)

    def calculate(self):
        # Methods
        plotter_methods = Plotter.Plotter()

        euler = methods.Euler(int(self.x0_field.get()), int(self.y0_field.get()), int(self.X_field.get()),
                              int(self.N_field.get()))
        improved_euler = methods.ImprovedEuler(int(self.x0_field.get()), int(self.y0_field.get()),
                                               int(self.X_field.get()), int(self.N_field.get()))
        exact = methods.Exact(int(self.x0_field.get()), int(self.y0_field.get()),
                              int(self.X_field.get()), int(self.N_field.get()))
        runge_kutta = methods.Runge_Kutta(int(self.x0_field.get()), int(self.y0_field.get()),
                                          int(self.X_field.get()), int(self.N_field.get()))

        # Plotting methods
        plotter_methods.add_graph(euler)
        plotter_methods.add_graph(improved_euler)
        plotter_methods.add_graph(exact)
        plotter_methods.add_graph(runge_kutta)
        canvas1 = FigureCanvasTkAgg(plotter_methods.figure, self)
        canvas1.get_tk_widget().place(x=150, y=20)

        # Errors
        plotter_errors = Plotter.Plotter()
        euler_error = methods.Error(exact, euler)
        runge_kutta_error = methods.Error(exact, runge_kutta)
        improved_euler_error = methods.Error(exact, improved_euler)

        # Plotting errors
        plotter_errors.add_graph(euler_error)
        plotter_errors.add_graph(improved_euler_error)
        plotter_errors.add_graph(runge_kutta_error)
        canvas2 = FigureCanvasTkAgg(plotter_errors.figure, self)
        canvas2.get_tk_widget().place(x=150, y=370)


if __name__ == '__main__':
    app = DE_App()
    app.mainloop()
