import random
import numpy as np


import main


def sample_main():
    x1_deg = 0
    x2_deg = 360

    delta_x = random.uniform(0.5, 1.5)

    x_deg_array = np.arange(x1_deg, x2_deg, delta_x)
    x_rad_array = np.deg2rad(x_deg_array)

    d = main.int_sin(x_rad_array)

    i = random.randint(0, len(x_deg_array)-1)
    x_i = x_deg_array[i]
    rect_i = d['a_array'][i]
    print(f"area at x = {x_i} deg is {rect_i}")

    print(f"numerical integration result is {d['area']}")


if "__main__" == __name__:
    sample_main()
