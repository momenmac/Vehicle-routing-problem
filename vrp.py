import math
import random



class VRP:
    def __init__(self, trucks, delivery_points, depot, temperature, cooling_rate, canvas):
        self.trucks = trucks
        self.delivery_points = delivery_points
        self.depot = depot
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.canvas = canvas
        self.min_temperature = 1e-10
        self.colors = ["red", "green", "blue", "orange", "purple", "yellow", "cyan", "magenta", "pink", "brown",
                       "black", "gray", "turquoise", "maroon", "olive"]

        self.iteration = 0
        self.current_routes = None
        self.current_distance = float('inf')
        self.best_routes = None
        self.best_distance = float('inf')

    def simulated_annealing(self, steps=1):
        if not self.delivery_points or not self.trucks:
            return

        if self.iteration == 0:
            self.current_routes = self.initial_solution()
            self.current_distance = self.calculate_total_distance(self.current_routes)
            self.best_routes = self.current_routes
            self.best_distance = self.current_distance
            self.update_canvas(self.best_routes)
            # print(
            #     f"Iteration: {self.iteration}, Current Distance: {self.current_distance}, Best Distance: {self.best_distance}")
            self.iteration+=1
            return

        for _ in range(steps):
            if self.temperature <= self.min_temperature:
                break

            new_routes = self.neighbor_solution(self.current_routes)
            if not new_routes:
                continue

            new_distance = self.calculate_total_distance(new_routes)
            delta_d = new_distance - self.current_distance
            r = random.random()
            e = math.exp(-delta_d / self.temperature)
            if delta_d < 0 or r < e:
                self.current_routes = new_routes
                self.current_distance = new_distance
                if new_distance < self.best_distance:
                    self.best_routes = new_routes
                    self.best_distance = new_distance

            self.temperature = self.temperature * self.cooling_rate
            # print(self.temperature)
            self.iteration += 1

            self.update_canvas(self.best_routes)
            print(
                f"Iteration: {self.iteration}, Current Distance: {self.current_distance}, Best Distance: {self.best_distance}")

    def neighbor_solution(self, routes):
        if len(routes) < 2:
            return None

        new_routes = [route[:] for route in routes]
        route1, route2 = random.sample(range(len(new_routes)), 2)

        if new_routes[route1] and new_routes[route2]:
            delPoint1 = random.choice(new_routes[route1])
            delPoint2 = random.choice(new_routes[route2])

            route1_capacity = sum(point.demand for point in new_routes[route1]) - delPoint1.demand + delPoint2.demand
            route2_capacity = sum(point.demand for point in new_routes[route2]) - delPoint2.demand + delPoint1.demand

            if route1_capacity <= self.trucks[route1].capacity and route2_capacity <= self.trucks[route2].capacity:
                index1 = new_routes[route1].index(delPoint1)
                index2 = new_routes[route2].index(delPoint2)
                new_routes[route1][index1], new_routes[route2][index2] = new_routes[route2][index2], new_routes[route1][index1]

        return new_routes

    def initial_solution(self):
        indices = list(range(len(self.delivery_points)))
        random.shuffle(indices)
        routes = [[] for _ in range(len(self.trucks))]
        capacities_used = [0] * len(self.trucks)

        for index in indices:
            point = self.delivery_points[index]
            for i in range(len(self.trucks)):
                if capacities_used[i] + point.demand <= self.trucks[i].capacity:
                    routes[i].append(point)
                    capacities_used[i] += point.demand
                    break

        return routes

    def calculate_total_distance(self, solution):
        total_distance = 0
        for route in solution:
            total_distance += self.calculate_route_distance(route)
        return total_distance

    def calculate_route_distance(self, route):
        if not route:
            return 0
        distance = self.calculate_distance(self.depot, route[0])
        for i in range(len(route) - 1):
            distance += self.calculate_distance(route[i], route[i + 1])
        distance += self.calculate_distance(route[-1], self.depot)
        return distance

    def calculate_distance(self, point_a, point_b):
        return math.sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)

    def update_canvas(self, solution):
        self.canvas.delete("route")
        for i, route in enumerate(solution):
            current_color = self.colors[i % len(self.colors)]
            current_point = self.depot
            for point in route:
                self.canvas.create_line(current_point.x, current_point.y, point.x, point.y,
                                        fill=current_color, tags="route")
                current_point = point
            self.canvas.create_line(current_point.x, current_point.y, self.depot.x, self.depot.y,
                                    fill=current_color, tags="route")
