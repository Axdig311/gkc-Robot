"""
Test one NEMA 17 stepper motor via TMC2209 driver on Raspberry Pi 5.

Wiring (first motor / base joint):
    GPIO 17 -> STEP
    GPIO 27 -> DIR
    GPIO 22 -> EN
    GND     -> GND (shared with PSU)
    24V PSU -> VM + GND on TMC2209
"""

import time
import gpiod
from gpiod.line import Direction, Value

from config import CHIP, MOTORS

MOTOR_NAME = "base"


def main():
    cfg = MOTORS[MOTOR_NAME]
    step_pin = cfg["step_pin"]
    dir_pin = cfg["dir_pin"]
    ena_pin = cfg["ena_pin"]
    steps_per_rev = cfg["steps_per_rev"]

    line_config = {
        step_pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        dir_pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        ena_pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    }

    with gpiod.request_lines(CHIP, consumer="test-motor", config=line_config) as req:
        req.set_value(ena_pin, Value.INACTIVE)  # Enable

        try:
            print(f"Motor test - {MOTOR_NAME} ({steps_per_rev} steps/rev)")
            print("=" * 40)

            print("1. One revolution CW...")
            req.set_value(dir_pin, Value.ACTIVE)
            for _ in range(steps_per_rev):
                req.set_value(step_pin, Value.ACTIVE)
                time.sleep(0.001)
                req.set_value(step_pin, Value.INACTIVE)
                time.sleep(0.001)
            time.sleep(1)

            print("2. One revolution CCW...")
            req.set_value(dir_pin, Value.INACTIVE)
            for _ in range(steps_per_rev):
                req.set_value(step_pin, Value.ACTIVE)
                time.sleep(0.001)
                req.set_value(step_pin, Value.INACTIVE)
                time.sleep(0.001)
            time.sleep(1)

            print("3. Slow (50 steps)...")
            req.set_value(dir_pin, Value.ACTIVE)
            for _ in range(50):
                req.set_value(step_pin, Value.ACTIVE)
                time.sleep(0.01)
                req.set_value(step_pin, Value.INACTIVE)
                time.sleep(0.01)
            time.sleep(1)

            print("4. Fast revolution...")
            for _ in range(steps_per_rev):
                req.set_value(step_pin, Value.ACTIVE)
                time.sleep(0.0005)
                req.set_value(step_pin, Value.INACTIVE)
                time.sleep(0.0005)

            print("\nDone!")

        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            req.set_value(ena_pin, Value.ACTIVE)  # Disable


if __name__ == "__main__":
    main()
