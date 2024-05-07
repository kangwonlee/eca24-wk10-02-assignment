import math
import pathlib
import random
import sys

from typing import Dict, Union


import numpy as np
import numpy.testing as nt
import pytest

RESULT = Dict[str, Union[float, np.ndarray]]


file_path = pathlib.Path(__file__)
test_folder = file_path.parent.absolute()
proj_folder = test_folder.parent.absolute()


sys.path.insert(0, str(proj_folder))


import main


random.seed()


@pytest.fixture
def x1_deg() -> float:
    return random.randint(0, 90)


@pytest.fixture
def x2_deg() -> float:
    return random.randint(270, 360)


@pytest.fixture
def delta_x() -> float:
    return random.uniform(0.1, 1.9)


@pytest.fixture
def x_deg_array(x1_deg:int, x2_deg:int, delta_x:float) -> np.ndarray:
    return np.arange(x1_deg, x2_deg, delta_x)


@pytest.fixture
def x_rad_array(x_deg_array:np.ndarray) -> np.ndarray:
    return np.deg2rad(x_deg_array)


@pytest.fixture
def result_dict(x_rad_array) -> RESULT:
    return main.int_sin_0(x_rad_array)


@pytest.fixture
def result_a_array_0(result_dict:RESULT) -> nd.ndarray:
    return result_dict['a_array_0']


@pytest.fixture
def result_area(result_dict:RESULT) -> float:
    return result_dict['area']


def test_result_type(result_dict:RESULT):
    assert isinstance(result_dict, dict), "returned result is not a `dict`\n반환된 결과가 `dict`가 아님"

    assert 'a_array_0' in result_dict, "returned result does not have `a_array_0`\n반환값에 `a_array_0`가 없음"
    assert 'area' in result_dict, "returned result does not have `area`\n반환값에 `area`가 없음"


def test_rect_type(result_a_array_0:nd.ndarray):
    assert isinstance(result_a_array_0, nd.ndarray), "returned result is not a `nd.ndarray`\n반환된 결과가 `nd.ndarray`가 아님"


def test_area_type(result_area:float):
    assert isinstance(result_area, float), "returned result is not a `float`\n반환된 결과가 `float`가 아님"


def test_rect_value(result_a_array_0:nd.ndarray, x_rad_array:nd.array, delta_x:float):
    q = result_a_array_0 * (1.0/delta_x)
    expected_q = np.sin(x_rad_array)
    np.assert_allclose(q, expected_q)


def test_area_value(result_area:float, delta_x:float):
    q = result_area / delta_x
    expected_q = np.sum(np.sin(x_rad_array))
    assert math.isclose(q, expected_q), "please verify numerical integration result\n적분 결과를 확인 바랍니다"


if "__main__" == __name__:
    pytest.main([__file__])
