from tkinter import *
from PIL import ImageTk, Image
from plotter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class DE_App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('500x700')
        self.title = "[DE] Solver"
        self.resizable(width=False, height=False)

        Label(self, text="Differential equation solver").place(x=200, y=0)
        Label(self, text="Here will be a graph with methods").place(x=200, y=100)
        Label(self, text="Here will be a graph with errors").place(x=200, y=500)

        pilImage = Image.open("equation.png").resize((120, 30), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pilImage)

        a = Label(image=image)
        a.image = image
        a.place(x=0, y=150)

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
        b = Button(self, text="Calculate", command=self.calculate)
        b.grid(row=4, column=0)

    def calculate(self):
        # Methods
        solution = MagicSolver(float(self.x0_field.get()), float(self.y0_field.get()), float(self.X_field.get()),
                               float(self.N_field.get()))

        canvas1 = FigureCanvasTkAgg(solution.generate_plot().figure, self)
        canvas1.get_tk_widget().place(x=150, y=20)

        errors = ErrorAnalysis(float(self.x0_field.get()), float(self.y0_field.get()), float(self.X_field.get()),
                               int(self.N_field.get()))

        errors.find_error('euler')
        errors.find_error('improved_euler')
        errors.find_error('runge_kutta')

        plotter_errors = Plotter('errors')
        plotter_errors.add_error_graph(errors, 'euler')
        plotter_errors.add_error_graph(errors, 'improved_euler')
        plotter_errors.add_error_graph(errors, 'runge_kutta')

        canvas2 = FigureCanvasTkAgg(plotter_errors.figure, self)
        canvas2.get_tk_widget().place(x=150, y=370)


if __name__ == '__main__':
    app = DE_App()
    app.mainloop()
