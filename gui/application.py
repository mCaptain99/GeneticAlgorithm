import tkinter as tk
import numpy as np
import time
from tkinter import ttk

from oe.data import MUTATION, CROSS, SELECTIONS, goldstein_prize, GlobalData
from oe.gui.placeholder import Placeholder
from oe.utils.plots import Plots
from oe.utils.bin_converter import Converter
from oe.utils.generator import Generator
from oe.model.population import Population


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Genetic Algorithm")
        self.create_widgets()

    def create_widgets(self):

        self.title = tk.Label(text="Begin population range:")
        self.title.grid(row=1, column=0, pady=3)
        self.begin = Placeholder(master=self.master, placeholder=-2, width=50)
        self.begin.grid(row=2, column=0, pady=5, padx=10)

        self.title = tk.Label(text="End population range:")
        self.title.grid(row=3, column=0, pady=3)
        self.end = Placeholder(master=self.master, placeholder=2, width=50)
        self.end.grid(row=4, column=0, pady=5)

        self.title = tk.Label(text="Population size:")
        self.title.grid(row=5, column=0, pady=3)
        self.population = Placeholder(master=self.master, placeholder=100, width=50)
        self.population.grid(row=6, column=0, pady=5)

        self.title = tk.Label(text="Epochs amount:")
        self.title.grid(row=7, column=0, pady=3)
        self.epochs = Placeholder(master=self.master, placeholder="70", width=50)
        self.epochs.grid(row=8, column=0, pady=10)

        self.app_title = tk.Label(text="Generic Algorithm", font=("Courier 32 bold"))
        self.app_title.grid(row=0, column=1, pady=3)

        self.title = tk.Label(text="Selection Method: ")
        self.title.grid(row=1, column=1, pady=3)
        self.selection_menu = ttk.Combobox(values=SELECTIONS)
        self.selection_menu.current(0)
        self.selection_menu.config(width=45)
        self.selection_menu.grid(row=2, column=1, pady=5)

        self.title = tk.Label(text="Selection percent: ")
        self.title.grid(row=3, column=1, pady=3)
        self.selection = Placeholder(master=self.master, placeholder="50", width=50)
        self.selection.grid(row=4, column=1, pady=5)

        self.title = tk.Label(text="Cross probability:")
        self.title.grid(row=5, column=1, pady=3)
        self.cross_probab = Placeholder(master=self.master, placeholder="0.5", width=50)
        self.cross_probab.grid(row=6, column=1, pady=5)

        self.title = tk.Label(text="Mutation probability:")
        self.title.grid(row=7, column=1, pady=3)
        self.mutation_probab = Placeholder(master=self.master, placeholder="0.2", width=50)
        self.mutation_probab.grid(row=8, column=1, pady=5)

        self.title = tk.Label(text="Cross method", justify='center')
        self.title.grid(row=1, column=2, pady=3)
        self.cross_menu = ttk.Combobox(values=CROSS)
        self.cross_menu.current(0)
        self.cross_menu.config(width=45)
        self.cross_menu.grid(row=2, column=2, pady=3)

        self.title = tk.Label(text="Mutation method", justify='center')
        self.title.grid(row=3, column=2, pady=3)
        self.mutation_menu = ttk.Combobox(values=MUTATION)
        self.mutation_menu.current(0)
        self.mutation_menu.config(width=45)
        self.mutation_menu.grid(row=4, column=2, pady=3)

        self.max_value = tk.BooleanVar()
        self.max_value.set(True)
        self.max_checbox = tk.Checkbutton(text='Maximalization', var=self.max_value)
        self.max_checbox.grid(row=5, column=2)

        self.start = tk.Button(text="START", font=('calibri', 10, 'bold', 'underline'), command=self.start,
                               foreground='Green', height=2, width=10)
        self.start.grid(row=6, column=2)

        self.title = tk.Label(text="Result:", font=("Courier 16 bold"))
        self.title.grid(row=7, column=2, pady=3)

        self.title = tk.Label(text="Execute time:", font=("Courier 16 bold"))
        self.title.grid(row=9, column=2, pady=3)

    def start(self):
        begin_range = self.begin.value()
        end_range = self.end.value()
        population_amount = self.population.value()
        epochs_amount = self.epochs.value()
        start = time.time()

        GlobalData.set(begin_range=begin_range,
                       end_range=end_range,
                       function=goldstein_prize,
                       population_amount=population_amount)
        population_generator = Generator(population_amount, begin_range, end_range)
        chromosome_pairs = population_generator.get_population()
        bests_from_epochs = []
        average_from_epochs = []
        std_from_epochs = []

        population = Population(chromosome_pairs=chromosome_pairs,
                                mutation_method=self.mutation_menu.get(),
                                cross_method=self.cross_menu.get(),
                                selection_method=self.selection_menu.get(),
                                cross_probability=float(self.cross_probab.get()),
                                mutation_probability=float(self.mutation_probab.get()),
                                selection_percent=int(self.selection.value()),
                                maximalization=self.max_value.get()
                                )

        for i in range(epochs_amount):
            population.epoch()
            bests_from_epochs.append(population.best.get_function_value())
            fun_result = 0
            stds = []
            for chromosome_pair in population:
                goldstein_prize_result = chromosome_pair.get_function_value()
                fun_result += goldstein_prize_result
                stds.append(goldstein_prize_result)
            average_from_epochs.append(fun_result // population.population_size)
            std_from_epochs.append(np.std(stds))

        end = time.time()
        Plots.best_plot(bests_from_epochs)
        Plots.average_plot(average_from_epochs)
        Plots.std_plot(std_from_epochs)

        self.title = tk.Label(text=population.best.get_function_value(), font=("Courier 16 bold"))
        self.title.grid(row=8, column=2, pady=3)

        self.title = tk.Label(text=str(end - start), font=("Courier 16 bold"))
        self.title.grid(row=10, column=2, pady=3)
