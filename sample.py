import random
import numpy as np


import main


def sample_main():
    x1_deg = 0
    x2_deg = 360

    x_deg_array = np.arange(x1_deg, x2_deg)
    x_rad_array = np.deg2rad(x_deg_array)

    d = main.int_sin(x_rad_array)

    i = random.choice(x_deg_array)
    print(f"area at x = {i} deg is {d['a_array'][int(i)]}")

    print(f"numerical integration result is {d['area']}")


if "__main__" == __name__:
    sample_main()
