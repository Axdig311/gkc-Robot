"""
Test-script for JSS57P2N stepper motor with Raspberry Pi 5.
Uses gpiod (libgpiod) which supports Pi 5.

Wiring:
    GPIO 17 -> PUL+
    GPIO 27 -> DIR+
    GPIO 22 -> ENA+
    GND     -> PUL-, DIR-, ENA-
    24V PSU -> +Vdc and GND on motor

Install: sudo apt install python3-gpiod
"""

import time
import gpiod

# Pin setup
PUL_PIN = 17  # Pulse - each pulse = one step
DIR_PIN = 27  # Direction - HIGH=CW, LOW=CCW
ENA_PIN = 22  # Enable - LOW=enabled

# Motor config
STEPS_PER_REV = 800  # Default setting (all DIP switches ON)
DELAY = 0.001        # Seconds between pulses (1ms = moderate speed)

CHIP = "/dev/gpiochip4"  # Pi 5 uses gpiochip4


def step(pul_line, dir_line, steps, direction, delay=DELAY):
    """Move motor a number of steps in given direction."""
    dir_line.set_value(1 if direction == "cw" else 0)
    for _ in range(steps):
        pul_line.set_value(1)
        time.sleep(delay)
        pul_line.set_value(0)
        time.sleep(delay)


def main():
    chip = gpiod.Chip(CHIP)

    pul_line = chip.get_line(PUL_PIN)
    dir_line = chip.get_line(DIR_PIN)
    ena_line = chip.get_line(ENA_PIN)

    pul_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
    dir_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)
    ena_line.request(consumer="motor", type=gpiod.LINE_REQ_DIR_OUT)

    ena_line.set_value(0)  # Enable motor

    try:
        print("Motor test - JSS57P2N")
        print("=" * 30)

        # Test 1: One full revolution clockwise
        print("1. One revolution CW (clockwise)...")
        step(pul_line, dir_line, STEPS_PER_REV, "cw")
        time.sleep(1)

        # Test 2: One full revolution counter-clockwise
        print("2. One revolution CCW (counter-clockwise)...")
        step(pul_line, dir_line, STEPS_PER_REV, "ccw")
        time.sleep(1)

        # Test 3: Slow rotation (easy to see steps)
        print("3. Slow rotation (50 steps)...")
        step(pul_line, dir_line, 50, "cw", delay=0.01)
        time.sleep(1)

        # Test 4: Fast rotation
        print("4. Fast rotation (one revolution)...")
        step(pul_line, dir_line, STEPS_PER_REV, "cw", delay=0.0005)

        print("\nDone! Motor test complete.")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ena_line.set_value(1)  # Disable motor
        pul_line.release()
        dir_line.release()
        ena_line.release()


if __name__ == "__main__":
    main()
