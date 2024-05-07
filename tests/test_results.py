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
    result = random.randint(n//2, 2*n)
    result += (result % 2)
    return result


@pytest.fixture
def x_deg_array2(x1_deg:int, x2_deg:int, n_rect:int) -> np.ndarray:
    return np.linspace(x1_deg, x2_deg, (n_rect+1))


@pytest.fixture
def x_deg_array(x_deg_array2) -> np.ndarray:
    return x_deg_array2[:-1]


@pytest.fixture
def x_rad_array2(x_deg_array2:np.ndarray) -> np.ndarray:
    return np.deg2rad(x_deg_array2)


@pytest.fixture
def x_rad_array(x_deg_array:np.ndarray) -> np.ndarray:
    return np.deg2rad(x_deg_array)


@pytest.fixture
def delta_x_rad(x_rad_array:np.ndarray) -> float:
    return x_rad_array[1] - x_rad_array[0]


@pytest.fixture
def result_dict_0(x1_rad, x2_rad, n_rect) -> RESULT:
    return main.int_cos_0(x1_rad, x2_rad, n_rect)


def test_result_0_type(result_dict_0:RESULT):
    assert isinstance(result_dict_0, dict), (
        "returned result is not a `dict`\n"
        "반환된 결과가 `dict`가 아님\n"
        f"{result_dict_0}"
    )

    assert 'a_array_0' in result_dict_0, (
        "returned result does not have `a_array_0`\n"
        "반환값에 `a_array_0`가 없음\n"
        f"{result_dict_0}"
    )
    assert 'area_0' in result_dict_0, (
        "returned result does not have `area_0`\n"
        "반환값에 `area_0`가 없음\n"
        f"{result_dict_0}"
    )


@pytest.fixture
def result_a_array_0(result_dict_0:RESULT) -> np.ndarray:
    return result_dict_0['a_array_0']


@pytest.fixture
def result_area_0(result_dict_0:RESULT) -> float:
    return result_dict_0['area_0']


def test_rect_type(result_a_array_0:np.ndarray):
    assert isinstance(result_a_array_0, np.ndarray), (
        "returned result 'a_array_0' is not an instance of `np.ndarray`\n"
        "반환된 결과 'a_array_0' 가 `np.ndarray`가 아님\n"
        f"{result_a_array_0}"
    )


def test_area_0_type(result_area_0:float):
    assert isinstance(result_area_0, float), (
        "returned result 'area_0' is not an instance of `float`\n"
        "반환된 결과 'area_0'가 `float`가 아님\n"
        f"{result_area_0}"
    )


def test_rect_value(result_a_array_0:np.ndarray, x_rad_array:np.array, delta_x_rad:float, x1_deg:int, x2_deg:int,):
    q = result_a_array_0 * (1.0/delta_x_rad)
    expected_q = np.cos(x_rad_array)
    nt.assert_allclose(
        q, expected_q,
        err_msg=(
            f'please verify the area of the rectangles\n'
            f'직사각형 넓이 계산을 확인 바랍니다\n'
            f'({x1_deg} deg ~ {x2_deg} deg)'
        )
    )


def test_area_0_value(result_area_0:float, delta_x_rad:float, x_rad_array:np.ndarray):
    q = result_area_0 * (1.0/delta_x_rad)
    expected_qq = np.cos(x_rad_array)
    expected_q = np.sum(expected_qq)
    assert math.isclose(q, expected_q), (
        "please verify numerical integration result\n"
        "적분 결과를 확인 바랍니다\n"
        f"({x1_deg} deg ~ {x2_deg} deg) result = {result_area_0}"
    )


@pytest.fixture
def expected_exact_int(x1_rad:float, x2_rad:float) -> float:
    return np.sin(x2_rad) - np.sin(x1_rad)


@pytest.fixture
def epsilon() -> float:
    return 1e-5


@pytest.fixture
def result_compare_int_cos(x1_rad:float, x2_rad:float, n_rect:int, epsilon:float) -> RESULT:
    return main.compare_int_cos(x1_rad, x2_rad, n_rect, epsilon)


def test_compare_int_cos_type(result_compare_int_cos:RESULT):
    assert isinstance(result_compare_int_cos, dict), (
        "returned result is not a `dict`\n"
        "반환된 결과가 `dict`가 아님\n"
        f"{result_compare_int_cos}"
    )

    assert 'area_0' in result_compare_int_cos, (
        "returned result does not have `area_0`\n"
        "반환값에 `area_0`가 없음\n"
        f"{result_compare_int_cos}"
    )
    assert 'area_exact' in result_compare_int_cos, (
        "returned result does not have `area_exact`\n"
        "반환값에 `area_exact`가 없음\n"
        f"{result_compare_int_cos}"
    )
    assert 'diff_0' in result_compare_int_cos, (
        "returned result does not have `diff_0`\n"
        "반환값에 `diff_0`가 없음\n"
        f"{result_compare_int_cos}"
    )
    assert 'is_close_0' in result_compare_int_cos, (
        "returned result does not have `is_close_0`\n"
        "반환값에 `is_close_0`가 없음\n"
        f"{result_compare_int_cos}"
    )


@pytest.fixture
def result_compare_numint(result_compare_int_cos:RESULT) -> float:
    return result_compare_int_cos['area_0']


def test_compare_int_cos__numint_type(result_compare_numint:float):
    assert isinstance(result_compare_numint, float), (
        f"returned result 'area_0' ({result_compare_numint}) is not an instance of `float`\n"
        f"반환된 결과 'area_exact' ({result_compare_numint}) 가 `float`가 아님"
    )


def test_compare_int_cos__numint(result_compare_numint:float, result_area_0:float):
    assert result_compare_numint == result_area_0, (
        f"'area_0' of compare_int_cos() ({result_compare_numint}) is not same as int_cos_0() ({result_area_0}) \n"
        f"compare_int_cos() 가 반환된 결과 'area_exact' ({result_compare_numint}) 가 int_cos_0() 반환 결과 ({result_area_0}) 와 다름"
    )


def test_compare_int_cos_area_exact(x1_deg:int, x2_deg:int, result_area_exact:float, expected_exact_int:float):
    assert math.isclose(result_area_exact, expected_exact_int), (
        f"please verify exact integration result ({x1_deg:d}deg~{x2_deg:d}deg returned : {result_area_exact:f}, expected : {expected_exact_int:f})\n"
        f"정적분 이론값 확인 바랍니다  ({x1_deg:d}deg~{x2_deg:d}deg 반환값 : {result_area_exact:f}, 예상값 : {expected_exact_int:f})"
    )


@pytest.fixture
def result_area_exact(result_compare_int_cos:RESULT) -> float:
    return result_compare_int_cos['area_exact']


def test_compare_int_cos_area_exact_type(result_area_exact:float):
    assert isinstance(result_area_exact, float), (
        f"returned result 'area_exact' ({result_area_exact}) is not an instance of `float`\n"
        f"반환된 결과 'area_exact' ({result_area_exact}) 가 `float`가 아님"
    )


def test_compare_int_cos_area_exact(x1_deg:int, x2_deg:int, result_area_exact:float, expected_exact_int:float):
    assert math.isclose(result_area_exact, expected_exact_int), (
        f"please verify exact integration result ({x1_deg:d}deg~{x2_deg:d}deg returned : {result_area_exact:f}, expected : {expected_exact_int:f})\n"
        f"정적분 이론값 확인 바랍니다  ({x1_deg:d}deg~{x2_deg:d}deg 반환값 : {result_area_exact:f}, 예상값 : {expected_exact_int:f})"
    )


@pytest.fixture
def result_diff(result_compare_int_cos:RESULT) -> float:
    return result_compare_int_cos['diff_0']


def test_result_diff_type(result_diff:float):
    assert isinstance(result_diff, float), "returned result 'diff_0' is not an instance of `float`\n반환된 결과 'diff_0'가 `float`가 아님"

    assert result_diff >= 0, (
        f"returned result 'diff_0' {result_diff} is supposed to be an absolute value.\n"
        f"반환된 결과 'diff_0' {result_diff} 는 절대값이어야 함."
    )


@pytest.fixture
def result_is_close(result_compare_int_cos:RESULT) -> bool:
    return result_compare_int_cos['is_close_0']


def test_result_is_close_type(result_is_close:bool):
    assert isinstance(result_is_close, (np.bool_, bool)), (
        f"returned result 'is_close_0' ({result_is_close}) is not an instance of `bool` ({type(result_is_close)}).\n"
        f"반환된 결과 'is_close_0' ({result_is_close})가 `bool`가 아님 ({type(result_is_close)})."
    )


@pytest.fixture
def expected_diff_div_delta_x(expected_exact_int:float, delta_x_rad:float, x_rad_array:np.ndarray) -> float:
    # diff_0 = exact - numerical
    # diff_0 / delta_x = exact / delta_x - numerical / delta_x
    expected_exact_int_div_delta_x = expected_exact_int / delta_x_rad
    expected_qq = np.cos(x_rad_array)
    expected_q = np.sum(expected_qq)

    return abs(expected_exact_int_div_delta_x - expected_q)


def test_compare_int_cos_diff(
        result_diff:float,
        expected_diff_div_delta_x:float,
        delta_x_rad:float,
    ):

    expected_diff = expected_diff_div_delta_x * delta_x_rad

    assert math.isclose(result_diff, expected_diff), (
        f"please verify `diff_0` (result : {result_diff}, expected : {expected_diff}).\n"
        f"`diff_0` 값을 확인 바람. (반환된 값 : {result_diff}, 예상된 값 : {expected_diff})"
    )


def test_compare_int_cos_is_close(
        epsilon:float, result_diff:float, result_is_close:bool
    ):
    b_is_close = result_diff < epsilon
    assert result_is_close == b_is_close, (
        "please verify the comparison result\n비교 결과를 확인 바랍니다"
    )


if "__main__" == __name__:
    pytest.main([__file__])
