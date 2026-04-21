import gpiod
from gpiod.line import Direction, Value

from config import CHIP, MOTORS
from motor import StepperMotor


class RobotArm:

    def __init__(self):
        self.motors = {}
        self._request = None

    def connect(self):
        line_config = {}
        for motor_cfg in MOTORS.values():
            for pin_key in ("step_pin", "dir_pin", "ena_pin"):
                line_config[motor_cfg[pin_key]] = gpiod.LineSettings(
                    direction=Direction.OUTPUT,
                    output_value=Value.INACTIVE,
                )

        self._request = gpiod.request_lines(CHIP, consumer="robot-arm", config=line_config)

        for name, cfg in MOTORS.items():
            self.motors[name] = StepperMotor(
                request=self._request,
                name=name,
                step_pin=cfg["step_pin"],
                dir_pin=cfg["dir_pin"],
                ena_pin=cfg["ena_pin"],
                steps_per_rev=cfg["steps_per_rev"],
                gear_ratio=cfg["gear_ratio"],
                max_speed=cfg["max_speed"],
                invert_dir=cfg["invert_dir"],
            )

    def enable_all(self):
        for motor in self.motors.values():
            motor.enable()

    def disable_all(self):
        for motor in self.motors.values():
            motor.disable()

    def move_joint(self, joint_name, degrees, speed=None):
        self.motors[joint_name].move_degrees(degrees, speed)

    def home_all(self):
        for motor in self.motors.values():
            motor.home()

    def emergency_stop(self):
        self.disable_all()

    def status(self):
        lines = []
        for name, motor in self.motors.items():
            lines.append(f"  {name:10s}: {motor.angle:7.1f} deg  (step {motor.position})")
        return "\n".join(lines)

    def disconnect(self):
        if self._request:
            self.disable_all()
            self._request.release()
            self._request = None
