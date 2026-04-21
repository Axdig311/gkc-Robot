"""
Interactive keyboard control for the robot arm.

Controls:
    A/D  = Base rotate left/right
    W/S  = Shoulder up/down
    Q/E  = Elbow up/down
    O/P  = Gripper open/close
    +/-  = Increase/decrease step size
    H    = Home all joints
    X    = Emergency stop
    ESC  = Quit
"""

import sys
import tty
import termios

from arm import RobotArm
from config import STEP_DEGREES

KEY_MAP = {
    "a": ("base", -1),
    "d": ("base", 1),
    "w": ("shoulder", 1),
    "s": ("shoulder", -1),
    "q": ("elbow", 1),
    "e": ("elbow", -1),
    "o": ("gripper", -1),
    "p": ("gripper", 1),
}


def read_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def main():
    arm = RobotArm()
    arm.connect()
    arm.enable_all()

    step_deg = STEP_DEGREES

    print("Robot Arm - Interactive Control")
    print("=" * 35)
    print("  A/D = Base left/right")
    print("  W/S = Shoulder up/down")
    print("  Q/E = Elbow up/down")
    print("  O/P = Gripper open/close")
    print("  +/- = Step size (now {:.1f} deg)".format(step_deg))
    print("  H   = Home all")
    print("  X   = Emergency stop")
    print("  ESC = Quit")
    print()

    try:
        while True:
            key = read_key().lower()

            if key == "\x1b":  # ESC
                print("\nQuitting...")
                break

            if key == "x":
                arm.emergency_stop()
                print("\n*** EMERGENCY STOP ***")
                break

            if key == "h":
                print("Homing all joints...")
                arm.home_all()
                print("Done.")

            elif key == "+" or key == "=":
                step_deg = min(step_deg + 1.0, 45.0)
                print(f"Step size: {step_deg:.1f} deg")

            elif key == "-":
                step_deg = max(step_deg - 1.0, 1.0)
                print(f"Step size: {step_deg:.1f} deg")

            elif key in KEY_MAP:
                joint, direction = KEY_MAP[key]
                arm.move_joint(joint, step_deg * direction)
                print(f"\r{arm.status()}", end="")

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        arm.disconnect()


if __name__ == "__main__":
    main()
