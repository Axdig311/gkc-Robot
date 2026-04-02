"""
Test-script for JSS57P2N stepper motor with Raspberry Pi.

Wiring:
    GPIO 17 -> PUL+
    GPIO 27 -> DIR+
    GND     -> PUL- and DIR-
    24V PSU -> +Vdc and GND on motor
"""

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not found - this script must run on a Raspberry Pi")
    print("Install with: sudo apt install python3-rpi.gpio")
    exit(1)

# Pin setup
PUL_PIN = 17  # Pulse - each pulse = one step
DIR_PIN = 27  # Direction - HIGH=CW, LOW=CCW
ENA_PIN = 22  # Enable (optional) - LOW=enabled

# Motor config
STEPS_PER_REV = 800  # Default setting (all DIP switches ON)
DELAY = 0.001        # Seconds between pulses (1ms = moderate speed)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUL_PIN, GPIO.OUT)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(ENA_PIN, GPIO.OUT)
    GPIO.output(ENA_PIN, GPIO.LOW)  # Enable motor


def step(steps, direction, delay=DELAY):
    """Move motor a number of steps in given direction."""
    GPIO.output(DIR_PIN, GPIO.HIGH if direction == "cw" else GPIO.LOW)
    for _ in range(steps):
        GPIO.output(PUL_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL_PIN, GPIO.LOW)
        time.sleep(delay)


def main():
    setup()
    try:
        print("Motor test - JSS57P2N")
        print("=" * 30)

        # Test 1: One full revolution clockwise
        print("1. One revolution CW (clockwise)...")
        step(STEPS_PER_REV, "cw")
        time.sleep(1)

        # Test 2: One full revolution counter-clockwise
        print("2. One revolution CCW (counter-clockwise)...")
        step(STEPS_PER_REV, "ccw")
        time.sleep(1)

        # Test 3: Slow rotation (easy to see steps)
        print("3. Slow rotation (50 steps)...")
        step(50, "cw", delay=0.01)
        time.sleep(1)

        # Test 4: Fast rotation
        print("4. Fast rotation (one revolution)...")
        step(STEPS_PER_REV, "cw", delay=0.0005)

        print("\nDone! Motor test complete.")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        GPIO.output(ENA_PIN, GPIO.HIGH)  # Disable motor
        GPIO.cleanup()


if __name__ == "__main__":
    main()
