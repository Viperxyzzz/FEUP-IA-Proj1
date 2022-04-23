import random
import math

""" Different types of temperature schedules """


class MultMonotonicCooling:
    def get_temperature(self, t0: float, alpha: float, i: int) -> float:
        """Override"""
        pass


class AddMonotonicCooling:
    def get_temperature(self, t0: float, file_name: str) -> str:
        """Override"""
        pass


class NonMonotonicAdaptCooling:
    def get_temperature(self, t0: float, file_name: str) -> str:
        """Override"""
        pass


class ExponentialMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 * (alpha ** i)


class LogarithmicMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * math.log(1 + i, 10))


class LinearMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * i)


class QuadraticMult(MultMonotonicCooling):
    def get_temperature(self, t0, alpha, i):
        return t0 / (1 + alpha * (i ** 2))


""" Simulated Annealing optimization algorithm """


class SimulatedAnnealing:
    def __init__(self, simulation, t_schedule_type):
        self.simulation = simulation
        self.t_schedule_type = t_schedule_type

    def temp_schedule(self, t_schedule_type, t0, i):
        alpha = 0.85

        if t_schedule_type == 1:
            return ExponentialMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 2:
            return LogarithmicMult.get_temperature(self, t0, 2, i)
        elif t_schedule_type == 3:
            return LinearMult.get_temperature(self, t0, alpha, i)
        elif t_schedule_type == 4:
            return QuadraticMult.get_temperature(self, t0, alpha, i)
        else:
            print("ERROR IN TEMP SCHEDULE")

    def random_neighbour(self, inter_prob, light_prob):
        for inter in self.simulation.intersections:
            if random.random() > inter_prob:
                for light in inter.traffic_lights:
                    if random.random() > light_prob:
                        light.time = random.randint(1, self.simulation.duration)

    def accept_with_prob(self, values_diff, t):
        try:
            return random.random() < math.exp(values_diff / t)
        except OverflowError:
            return False

    def value(self, state):
        self.simulation.set_state(state)
        self.simulation.run()
        return self.simulation.score

    def run(self, n_iterations, t0, schedule_type):
        best = self.simulation.output_state_copy()

        for i in range(n_iterations):
            t = self.temp_schedule(schedule_type, t0, i)

            current_state = self.simulation.output_state_copy()
            self.random_neighbour(0.1, 0.1)
            next_state = self.simulation.output_state_copy()

            if self.value(best) < self.value(current_state):
                best = self.simulation.output_state_copy()

            values_diff = self.value(next_state) - self.value(current_state)

            print("iteration: [" + str(i) + "] 🌡️ " + str(t) + " acceptance prob: " +
                str(self.accept_with_prob(values_diff, t)) +
                " curr state: " + self.simulation.print_state(current_state) +
                " next state: " + self.simulation.print_state(next_state), end='\r')

            '''
            print("current value: ", self.value(current_state))
            print("next value: ", self.value(next_state))
            print("temperature: ", t)
            print("acceptance prob: ", self.accept_with_prob(values_diff, t))
            print("values diff: ", values_diff)
            '''

            if values_diff >= 0:
                current_state = next_state
            else:
                if self.accept_with_prob(values_diff, t):
                    current_state = next_state

            self.simulation.set_state(current_state)

        return best, self.value(best)
