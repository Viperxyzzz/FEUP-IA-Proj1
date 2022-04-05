import queue


class TrafficLight:
    def __init__(self, street, time):
        self.queue = queue.Queue
        self.time = time
        self.street = street
        self.current_time = time
        self.green_light = False

    def add_car(self, car):
        self.queue.put(car)

    def remove_car(self):
        return self.queue.get()

    def swap_light(self):
        self.green_light = not self.green_light

    def update(self):
        if not self.green_light:
            return
        self.current_time -= 1

        # greenlight time is out now
        if self.current_time == 0:
            self.swap_light()
            self.current_time = self.time