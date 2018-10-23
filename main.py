"""
Differential equation solver
Implemented by Mikhail Tkachenko
BS17-7
"""


from tkinter import *
from PIL import ImageTk, Image
from plotter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DEApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('900x700')  # Set Size
        self.title = "[DE] Solver"  # Set Title
        self.resizable(width=False, height=False)  # Turn off resizing

        # Place labels
        Label(self, text="Differential equation solver").place(x=70, y=0)
        Label(self, text="Here will be a graph with methods").place(x=470, y=100)
        Label(self, text="Here will be a graph with local errors").place(x=70, y=500)
        Label(self, text="Here will be a graph with N errors").place(x=470, y=500)

        # Place image with equation
        pil_image = Image.open("equation.png").resize((120, 25), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pil_image)
        a = Label(image=image)
        a.image = image
        a.place(x=80, y=210)

        # Place form

        # Place labels
        Label(self, text="x0").grid(row=0, padx=50, pady=(70,0))
        Label(self, text="y0").grid(row=1, padx=50,)
        Label(self, text="X").grid(row=2, padx=50)
        Label(self, text="N").grid(row=3, padx=50)

        # Initialize fields (entries)
        self.x0_field = Entry(self, width=3)
        self.y0_field = Entry(self, width=3)
        self.X_field = Entry(self, width=3)
        self.N_field = Entry(self, width=3)

        # Place fields
        self.x0_field.grid(row=0, column=1, pady=(70,0))
        self.y0_field.grid(row=1, column=1)
        self.X_field.grid(row=2, column=1)
        self.N_field.grid(row=3, column=1)
        b = Button(self, text="Calculate", command=self.calculate)
        b.grid(row=4, column=0, padx=50)

    def calculate(self):
        # Find a solution
        solution = MagicSolver(float(self.x0_field.get()), float(self.y0_field.get()), float(self.X_field.get()),
                               float(self.N_field.get()))

        # Put it in Canvas1
        canvas1 = FigureCanvasTkAgg(solution.generate_plot().figure, self)
        canvas1.get_tk_widget().place(x=470, y=20)

        # Put local errors graph on Canvas2
        canvas2 = FigureCanvasTkAgg(solution.create_local_error_graph().figure, self)
        canvas2.get_tk_widget().place(x=0, y=370)

        # Get Errors
        errors = ErrorAnalysis(float(self.x0_field.get()), float(self.y0_field.get()), float(self.X_field.get()),
                               int(self.N_field.get()))

        # Calculate each of errors
        errors.find_error('euler')
        errors.find_error('improved_euler')
        errors.find_error('runge_kutta')

        # Put errors N graph on Canvas3
        canvas3 = FigureCanvasTkAgg(errors.generate_plot().figure, self)
        canvas3.get_tk_widget().place(x=470, y=370)


if __name__ == '__main__':
    app = DEApp()
    while True:
        try:
            app.mainloop()
        except UnicodeDecodeError:
            continue
