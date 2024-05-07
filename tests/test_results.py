import math
import pathlib
import random
import sys


from typing import Callable, Tuple


PDF = Callable[[float], float]
CDF = Callable[[float], float]
PARAM = Tuple[PDF, CDF, float, float]

PDF_CDF = Tuple[PDF, CDF]

import pytest
import scipy.stats


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = test_folder.parent.absolute()


sys.path.insert(0, str(proj_folder))


import main


random.seed()


def get_uniform(x_min:float, x_max:float) -> PDF_CDF:
    def pdf(x:float)->float:
        return scipy.stats.uniform.pdf(x, loc=x_min, scale=(x_max - x_min))
    def cdf(x:float)->float:
        return scipy.stats.uniform.cdf(x, loc=x_min, scale=(x_max - x_min))
    return pdf, cdf


def get_normal(ave:float, std:float) -> PDF_CDF:
    def pdf(x:float)->float:
        return scipy.stats.norm.pdf(x, loc=ave, scale=std)
    def cdf(x:float)->float:
        return scipy.stats.norm.cdf(x, loc=ave, scale=std)
    return pdf, cdf


def get_exponential(lam) -> PDF_CDF:
    def pdf(x:float)->float:
        return scipy.stats.expon.pdf(x, scale=1/lam)
    def cdf(x:float)->float:
        return scipy.stats.expon.cdf(x, scale=1/lam)
    return pdf, cdf


def get_gamma(alpha, beta) -> PDF_CDF:
    def pdf(x:float)->float:
        return scipy.stats.gamma.pdf(x, a=alpha, scale=1/beta)
    def cdf(x:float)->float:
        return scipy.stats.gamma.cdf(x, a=alpha, scale=1/beta)
    return pdf, cdf


def get_beta(alpha, beta) -> PDF_CDF:
    def pdf(x:float)->float:
        return scipy.stats.beta.pdf(x, a=alpha, b=beta)
    def cdf(x:float)->float:
        return scipy.stats.beta.cdf(x, a=alpha, b=beta)
    return pdf, cdf


def get_beta_param()->PARAM:
    alpha = random.uniform(1, 3)
    beta = random.uniform(1, 3)       
    pdf, cdf = get_beta(alpha, beta)
    x_i = random.uniform(0.1, 0.9)
    x_j = random.uniform(0.1, 0.9)
    return pdf, cdf, x_i, x_j


def get_gamma_param()->PARAM:
    alpha = random.uniform(1, 3)
    beta = random.uniform(0.5, 1.5)
    pdf, cdf = get_gamma(alpha, beta)
    x_i = random.uniform(0.5, 2)
    x_j = random.uniform(0.5, 2)
    return pdf, cdf, x_i, x_j


def get_uniform_param()->PARAM:
    param = random.uniform(0.5, 1.5)
    pdf, cdf = get_exponential(param)
    x_i = random.uniform(0.1, 1)
    x_j = random.uniform(0.1, 1)
    return pdf, cdf, x_i, x_j


def get_normal_param()->PARAM:
    ave = random.uniform(0.3, 0.4)
    std = random.uniform(0.07, 0.12)
    pdf, cdf = get_normal(ave, std)
    x_i = random.uniform(ave+std*(-2), ave+std*(2))
    x_j = random.uniform(ave+std*(-2), ave+std*(2))
    return pdf, cdf, x_i, x_j


def get_uniform_param()->PARAM:
    x_min = random.uniform(0.2, 0.5)
    x_max = random.uniform(0.6, 0.9)
    pdf, cdf = get_uniform(x_min, x_max)
    x_i = random.uniform(x_min, x_max)
    x_j = random.uniform(x_min, x_max)
    return pdf, cdf, x_i, x_j


def get_x1_x2(x_i:float, x_j:float) -> Tuple[float, float]:
    '''
    0 < x1 < x2
    '''
    x_1 = max(0, min(x_i, x_j))
    x_2 = max(x_i, x_j)

    if x_1 > x_2:
        x_2 = x_1 + random.uniform(0.1, 0.3)

    return x_1, x_2


@pytest.fixture(params=["uniform", "normal", "exponential", "gamma", "beta"])
def dist(request) -> str:
    return request.param


@pytest.fixture
def p_c_1_2(dist: str) -> PARAM:
    d = {
        "uniform":get_uniform_param,
        "normal":get_normal_param,
        "exponential":get_uniform_param,
        "gamma":get_gamma_param,
        "beta":get_beta_param,
    }
    get_param = d.get(dist, get_normal_param)
    pdf, cdf, x_i, x_j = get_param()

    x_1, x_2 = get_x1_x2(x_i, x_j)

    return (pdf, cdf, x_1, x_2)


def test_probability_between(p_c_1_2):
    pdf, cdf, x1, x2 = p_c_1_2

    # Calculate expected probability using the CDF
    expected_probability = cdf(x2) - cdf(x1)

    result = main.probability_between(pdf, x1, x2)

    # Allow for numerical approximation tolerance
    assert math.isclose(result, expected_probability, rel_tol=0.01), (
        f"expected={expected_probability}, result={result}"
    )


if "__main__" == __name__:
    pytest.main([__file__])
