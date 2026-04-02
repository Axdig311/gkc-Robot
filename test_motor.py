"""
Test-script for JSS57P2N stepper motor with Raspberry Pi 5.
Uses gpiod v2 API.

Wiring:
    GPIO 17 -> PUL+
    GPIO 27 -> DIR+
    GPIO 22 -> ENA+
    GND     -> PUL-, DIR-, ENA-
    24V PSU -> +Vdc and GND on motor
"""

import time
import gpiod
from gpiod.line import Direction, Value

# Pin setup
PUL_PIN = 17  # Pulse - each pulse = one step
DIR_PIN = 27  # Direction - HIGH=CW, LOW=CCW
ENA_PIN = 22  # Enable - LOW=enabled

# Motor config
STEPS_PER_REV = 800  # Default setting (all DIP switches ON)
DELAY = 0.001        # Seconds between pulses (1ms = moderate speed)

CHIP = "/dev/gpiochip4"  # Pi 5 uses gpiochip4


def step(request, steps, direction, delay=DELAY):
    """Move motor a number of steps in given direction."""
    request.set_value(DIR_PIN, Value.ACTIVE if direction == "cw" else Value.INACTIVE)
    for _ in range(steps):
        request.set_value(PUL_PIN, Value.ACTIVE)
        time.sleep(delay)
        request.set_value(PUL_PIN, Value.INACTIVE)
        time.sleep(delay)


def main():
    config = {
        PUL_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        DIR_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
        ENA_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE),
    }

    with gpiod.request_lines(CHIP, consumer="motor", config=config) as request:
        request.set_value(ENA_PIN, Value.INACTIVE)  # Enable motor

        try:
            print("Motor test - JSS57P2N")
            print("=" * 30)

            print("1. One revolution CW (clockwise)...")
            step(request, STEPS_PER_REV, "cw")
            time.sleep(1)

            print("2. One revolution CCW (counter-clockwise)...")
            step(request, STEPS_PER_REV, "ccw")
            time.sleep(1)

            print("3. Slow rotation (50 steps)...")
            step(request, 50, "cw", delay=0.01)
            time.sleep(1)

            print("4. Fast rotation (one revolution)...")
            step(request, STEPS_PER_REV, "cw", delay=0.0005)

            print("\nDone! Motor test complete.")

        except KeyboardInterrupt:
            print("\nStopped by user.")
        finally:
            request.set_value(ENA_PIN, Value.ACTIVE)  # Disable motor


if __name__ == "__main__":
    main()
