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


def test_result_type(result_dict:RESULT):
    assert isinstance(result_dict, dict), "returned result is not a `dict`\n반환된 결과가 `dict`가 아님"

    assert 'a_array_0' in result_dict, "returned result does not have `a_array_0`\n반환값에 `a_array_0`가 없음"
    assert 'area_0' in result_dict, "returned result does not have `area_0`\n반환값에 `area_0`가 없음"


@pytest.fixture
def result_a_array_0(result_dict:RESULT) -> np.ndarray:
    return result_dict['a_array_0']


@pytest.fixture
def result_area_0(result_dict:RESULT) -> float:
    return result_dict['area_0']


def test_rect_type(result_a_array_0:np.ndarray):
    assert isinstance(result_a_array_0, np.ndarray), "returned result 'a_array_0' is not an instance of `np.ndarray`\n반환된 결과 'a_array_0' 가 `np.ndarray`가 아님"


def test_area_0_type(result_area_0:float):
    assert isinstance(result_area_0, float), "returned result 'area_0' is not an instance of `float`\n반환된 결과 'area_0'가 `float`가 아님"


def test_rect_value(result_a_array_0:np.ndarray, x_rad_array:np.array, delta_x:float):
    q = result_a_array_0 * (1.0/delta_x)
    expected_q = np.sin(x_rad_array)
    nt.assert_allclose(q, expected_q, err_msg='please verify the area of the rectangles<br>직사각형 넓이 계산을 확인 바랍니다')


def test_area_0_value(result_area_0:float, delta_x:float):
    q = result_area_0 * (1.0/delta_x)
    expected_q = np.sum(np.sin(x_rad_array))
    assert math.isclose(q, expected_q), "please verify numerical integration result\n적분 결과를 확인 바랍니다"


if "__main__" == __name__:
    pytest.main([__file__])
