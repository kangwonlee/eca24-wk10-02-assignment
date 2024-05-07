import scipy.stats

import main


def f(x, ave=1.0, std=0.1):
    return scipy.stats.norm.pdf(x, loc=ave, scale=std)


def sample_main():
    x1 = 0.9
    x2 = 1.1

    p = main.probability_between(f, 0.9, 1.1)
    print(f"probability that x is between {x1} and {x2} will be {p:.4f}")


if "__main__" == __name__:
    sample_main()
