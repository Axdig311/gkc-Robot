CHIP = "/dev/gpiochip4"

MOTORS = {
    "base": {
        "step_pin": 17,
        "dir_pin": 27,
        "ena_pin": 22,
        "steps_per_rev": 3200,  # 200 * 16 microstepping (A4988 1/16)
        "gear_ratio": 4.0,
        "max_speed": 500,
        "invert_dir": False,
    },
    "shoulder": {
        "step_pin": 23,
        "dir_pin": 24,
        "ena_pin": 25,
        "steps_per_rev": 3200,
        "gear_ratio": 5.0,
        "max_speed": 300,
        "invert_dir": False,
    },
    "elbow": {
        "step_pin": 5,
        "dir_pin": 6,
        "ena_pin": 12,
        "steps_per_rev": 3200,
        "gear_ratio": 3.0,
        "max_speed": 400,
        "invert_dir": False,
    },
    "gripper": {
        "step_pin": 13,
        "dir_pin": 19,
        "ena_pin": 26,
        "steps_per_rev": 3200,
        "gear_ratio": 1.0,
        "max_speed": 600,
        "invert_dir": False,
    },
}

STEP_DEGREES = 5.0
