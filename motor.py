import time
from gpiod.line import Value


class StepperMotor:

    def __init__(self, request, name, step_pin, dir_pin, ena_pin,
                 steps_per_rev=1600, gear_ratio=1.0, max_speed=500, invert_dir=False):
        self.request = request
        self.name = name
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.ena_pin = ena_pin
        self.steps_per_rev = steps_per_rev
        self.gear_ratio = gear_ratio
        self.max_speed = max_speed
        self.invert_dir = invert_dir
        self.position = 0

    @property
    def steps_per_degree(self):
        return (self.steps_per_rev * self.gear_ratio) / 360.0

    @property
    def angle(self):
        return self.position / self.steps_per_degree

    def enable(self):
        self.request.set_value(self.ena_pin, Value.INACTIVE)

    def disable(self):
        self.request.set_value(self.ena_pin, Value.ACTIVE)

    def move_steps(self, steps, speed=None):
        if steps == 0:
            return

        speed = speed or self.max_speed
        delay = 1.0 / (2 * speed)

        if steps > 0:
            dir_val = Value.INACTIVE if self.invert_dir else Value.ACTIVE
        else:
            dir_val = Value.ACTIVE if self.invert_dir else Value.INACTIVE

        self.request.set_value(self.dir_pin, dir_val)
        time.sleep(0.001)

        for _ in range(abs(steps)):
            self.request.set_value(self.step_pin, Value.ACTIVE)
            time.sleep(delay)
            self.request.set_value(self.step_pin, Value.INACTIVE)
            time.sleep(delay)

        self.position += steps

    def move_degrees(self, degrees, speed=None):
        steps = int(degrees * self.steps_per_degree)
        self.move_steps(steps, speed)

    def move_to_angle(self, target_degrees, speed=None):
        target_steps = int(target_degrees * self.steps_per_degree)
        delta = target_steps - self.position
        self.move_steps(delta, speed)

    def home(self, speed=None):
        self.move_to_angle(0, speed)
