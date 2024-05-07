import random
import numpy as np


import main


def sample_main():
    x1_deg = 0
    x2_deg = 360

    x1_rad, x2_rad = np.deg2rad(x1_deg), np.deg2rad(x2_deg)

    n = random.randint(100, 300)

    result_0 = main.int_cos_0(x1_rad, x2_rad, n)

    a_array_0 = result_0['a_array_0']
    i = random.randint(0, len(a_array_0)-1)
    rect_i = a_array_0[i]

    print(f"area of rect #{i} is {rect_i}")


    result_1 = main.int_cos_1(x1_rad, x2_rad, n)
    a_array_1 = result_1['a_array_1']
    j = random.randint(0, len(a_array_1)-1)
    trapz_j = a_array_1[j]

    print(f"area of trapz #{j} is {trapz_j}")

    print(f"0th order result is {result_0['area_0']}")
    print(f"1st order result is {result_1['area_1']}")

    epsilon = 1e-6
    print(main.compare_int_cos(x1_rad, x2_rad, n, epsilon))


if "__main__" == __name__:
    sample_main()
