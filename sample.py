import random
import numpy as np


import main


def sample_main():
    x1_deg = 0
    x2_deg = 360

    delta_x = random.uniform(0.5, 1.5)

    x_deg_array = np.arange(x1_deg, x2_deg, delta_x)
    x_rad_array = np.deg2rad(x_deg_array)

    result_0 = main.int_sin_0(x_rad_array)

    i = random.randint(0, len(x_deg_array)-1)
    x_i = x_deg_array[i]
    rect_i = result_0['a_array_0'][i]
    print(f"area at x = {x_i} deg is {rect_i}")

    print(f"numerical integration result is {result_0['area_0']}")


if "__main__" == __name__:
    sample_main()
