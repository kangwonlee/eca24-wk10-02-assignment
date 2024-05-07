import random
import numpy as np


import main


def sample_main():
    x1_deg = 0
    x2_deg = 360

    x1_rad, x2_rad = np.deg2rad(x1_deg), np.deg2rad(x2_deg)

    n = random.randint(100, 300)

    result_0 = main.int_cos_0(x1_rad, x2_rad, n)

    a_array = result_0['a_array_0']
    i = random.randint(0, len(a_array)-1)
    rect_i = result_0['a_array_0'][i]

    print(f"area of rect #{i} is {rect_i}")

    print(f"numerical integration result is {result_0['area_0']}")


if "__main__" == __name__:
    sample_main()
