import tkinter as tk
from tkinter import simpledialog
from vrp import VRP
from truck import Truck
from delivery_point import DeliveryPoint

class VRPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRP Optimizer")

        self.delivery_points = []
        self.trucks = []
        self.depot_added = False

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.add_delivery_point)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.fields_frame = tk.Frame(self.control_frame)
        self.fields_frame.pack(side=tk.TOP, pady=5)

        tk.Label(self.fields_frame, text="Truck Capacity:").pack(side=tk.LEFT, padx=5)
        self.truck_capacity_entry = tk.Entry(self.fields_frame, width=10)
        self.truck_capacity_entry.insert(0, "4")
        self.truck_capacity_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.fields_frame, text="Number of Trucks:").pack(side=tk.LEFT, padx=5)
        self.num_trucks_entry = tk.Entry(self.fields_frame, width=10)
        self.num_trucks_entry.insert(0, "10")
        self.num_trucks_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.fields_frame, text="Temperature:").pack(side=tk.LEFT, padx=5)
        self.temperature_entry = tk.Entry(self.fields_frame, width=10)
        self.temperature_entry.insert(0, "1000")
        self.temperature_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.fields_frame, text="Cooling Rate:").pack(side=tk.LEFT, padx=5)
        self.cooling_rate_entry = tk.Entry(self.fields_frame, width=10)
        self.cooling_rate_entry.insert(0, "0.995")
        self.cooling_rate_entry.pack(side=tk.LEFT, padx=5)

        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(side=tk.TOP, pady=5)

        self.start_button = tk.Button(self.button_frame, text="Start Optimization", command=self.start_optimization)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.single_step_button = tk.Button(self.button_frame, text="Single Step", command=self.single_step)
        self.single_step_button.pack(side=tk.LEFT, padx=5)

        self.hundred_steps_button = tk.Button(self.button_frame, text="100 Steps", command=self.hundreds_step_button)
        self.hundred_steps_button.pack(side=tk.LEFT, padx=5)

        self.thousands_step_button = tk.Button(self.button_frame, text="1000 Steps", command=self.thousands_step_button)
        self.thousands_step_button.pack(side=tk.LEFT, padx=5)

        self.status_frame = tk.Frame(self.control_frame)
        self.status_frame.pack(side=tk.BOTTOM, pady=5)

        tk.Label(self.status_frame, text="Iteration:").pack(side=tk.LEFT, padx=5)
        self.iteration_entry = tk.Entry(self.status_frame, width=10, state='readonly')
        self.iteration_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.status_frame, text="Current Distance:").pack(side=tk.LEFT, padx=5)
        self.current_distance_entry = tk.Entry(self.status_frame, width=15, state='readonly')
        self.current_distance_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.status_frame, text="Best Distance:").pack(side=tk.LEFT, padx=5)
        self.best_distance_entry = tk.Entry(self.status_frame, width=15, state='readonly')
        self.best_distance_entry.pack(side=tk.LEFT, padx=5)

    def add_delivery_point(self, event):
        x, y = event.x, event.y
        if not self.depot_added:
            self.add_depot(x, y)
            self.depot_added = True
        else:
            demand = simpledialog.askinteger("Demand", "Enter demand for this point:")
            if demand is not None:
                self.delivery_points.append(DeliveryPoint(x, y, demand))
                oval_size = 12
                self.canvas.create_oval(x - oval_size, y - oval_size, x + oval_size, y + oval_size, fill='blue')
                text_size = 12
                self.canvas.create_text(x, y, text=str(demand), font=("Helvetica", text_size), fill="white")

    def add_depot(self, x, y):
        self.depot_x = x
        self.depot_y = y
        oval_size = 15
        self.canvas.create_oval(x - oval_size, y - oval_size, x + oval_size, y + oval_size, fill='red', tags="depot")

    def start_optimization(self):
        import sys
        cooling_rate = float(self.cooling_rate_entry.get())

        depot = DeliveryPoint(self.depot_x, self.depot_y, 0)

        truck_capacity = int(self.truck_capacity_entry.get())
        num_trucks = int(self.num_trucks_entry.get())
        temperature = float(self.temperature_entry.get())

        self.trucks = [Truck(truck_capacity) for _ in range(num_trucks)]


        self.vrp = VRP(self.trucks, self.delivery_points, depot, temperature, cooling_rate, self.canvas)

        self.vrp.simulated_annealing(steps=1)
        self.update_status_fields()

    def single_step(self):
        self.vrp.simulated_annealing(steps=1)
        self.update_status_fields()

    def hundreds_step_button(self):
        self.vrp.simulated_annealing(steps=100)
        self.update_status_fields()

    def thousands_step_button(self):
        self.vrp.simulated_annealing(steps=1000)
        self.update_status_fields()

    def update_status_fields(self):
        self.iteration_entry.config(state='normal')
        self.iteration_entry.delete(0, tk.END)
        self.iteration_entry.insert(0, str(self.vrp.iteration))
        self.iteration_entry.config(state='readonly')

        self.current_distance_entry.config(state='normal')
        self.current_distance_entry.delete(0, tk.END)
        self.current_distance_entry.insert(0, str(self.vrp.current_distance))
        self.current_distance_entry.config(state='readonly')

        self.best_distance_entry.config(state='normal')
        self.best_distance_entry.delete(0, tk.END)
        self.best_distance_entry.insert(0, str(self.vrp.best_distance))
        self.best_distance_entry.config(state='readonly')


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x650")
    app = VRPApp(root)
    root.mainloop()
