

class Fitness():
    def __init__(self, graph):
        fitness_value = 0

        return fitness_value

    def display(self):
        for ws, cfg in zip(self.ws_list, self.configs):
            print(f"Workstation number: {ws.num} Coordinates x={cfg.x} y={cfg.y} active={ws.active}")
        print(f"The topology number is {self.num}")