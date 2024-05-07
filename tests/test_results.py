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
def x1_rad(x1_deg:int) -> float:
    return math.radians(x1_deg)


@pytest.fixture
def x2_rad(x2_deg:int) -> float:
    return math.radians(x2_deg)


@pytest.fixture
def n_rect(x1_deg:int, x2_deg:int) -> int:
    n = x2_deg - x1_deg
    return random.randint(n//2, 2*n)


@pytest.fixture
def x_deg_array(x1_deg:int, x2_deg:int, n_rect:int) -> np.ndarray:
    return np.linspace(x1_deg, x2_deg, (n_rect+1))[:-1]


@pytest.fixture
def x_rad_array(x_deg_array:np.ndarray) -> np.ndarray:
    return np.deg2rad(x_deg_array)


@pytest.fixture
def delta_x_rad(x_rad_array:np.ndarray) -> float:
    return x_rad_array[1] - x_rad_array[0]


@pytest.fixture
def result_dict(x1_rad, x2_rad, n_rect) -> RESULT:
    return main.int_cos_0(x1_rad, x2_rad, n_rect)


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


def test_rect_value(result_a_array_0:np.ndarray, x_rad_array:np.array, delta_x_rad:float):
    q = result_a_array_0 * (1.0/delta_x_rad)
    expected_q = np.cos(x_rad_array)
    nt.assert_allclose(q, expected_q, err_msg='please verify the area of the rectangles<br>직사각형 넓이 계산을 확인 바랍니다')


def test_area_0_value(result_area_0:float, delta_x_rad:float, x_rad_array:np.ndarray):
    q = result_area_0 * (1.0/delta_x_rad)
    expected_qq = np.cos(x_rad_array)
    expected_q = np.sum(expected_qq)
    assert math.isclose(q, expected_q), "please verify numerical integration result\n적분 결과를 확인 바랍니다"


@pytest.fixture
def expected_exact_int(x1_rad:float, x2_rad:float) -> float:
    return np.sin(x2_rad) - np.sin(x1_rad)


@pytest.fixture
def result_exact_int(x1_rad:float, x2_rad:float) -> float:
    return main.exact_int_cos(x1_rad, x2_rad)


def test_exact_int_cos(x1_deg:int, x2_deg:int, result_exact_int:float, expected_exact_int:float):
    assert math.isclose(result_exact_int, expected_exact_int), (
        f"please verify exact integration result.({x1_deg:d}deg~{x2_deg:d}deg)\n"
        f"정적분 이론값 확인 바랍니다.({x1_deg:d}deg~{x2_deg:d}deg)"
    )


if "__main__" == __name__:
    pytest.main([__file__])
