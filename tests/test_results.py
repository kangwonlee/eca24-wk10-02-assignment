import math
import pathlib
import random
import sys


from typing import Callable, Dict, Union


import numpy as np
import numpy.testing as nt
import pytest


RESULT = Dict[str, Union[float, np.ndarray]]
METHOD = Callable[[float, float, int], RESULT]
TABLE = Dict[str, np.array]


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
def f_array(x_rad_array2:np.ndarray) -> np.ndarray:
    return np.cos(x_rad_array2)


@pytest.fixture
def c_table(f_array:np.ndarray) -> TABLE:
    return {
        '0': f_array[:-1],
        '1': np.array((1, 1)) @ np.vstack((f_array[:-1], f_array[1:])),
        '2': np.array((1, 4, 1)) @ np.vstack((f_array[:-1:2], f_array[1::2], f_array[2::2])),
    }


@pytest.fixture
def delta_x_rad(x_rad_array2:np.ndarray) -> float:
    return x_rad_array2[1] - x_rad_array2[0]


@pytest.fixture(params=[main.int_cos_0, main.int_cos_1, main.int_cos_2])
def int_method(request):
    return request.param


@pytest.fixture
def method_number(int_method:METHOD) -> str:
    return int_method.__name__[-1]


@pytest.fixture
def c_array(c_table:TABLE, method_number:str) -> np.array:
    return c_table[method_number]


@pytest.fixture
def division(method_number:np.ndarray, delta_x_rad:float) -> float:
    return (int(method_number) + 1) / delta_x_rad


@pytest.fixture
def result_dict(int_method:METHOD, x1_rad:float, x2_rad:float, n_rect:int) -> RESULT:
    return int_method(x1_rad, x2_rad, n_rect)


def test_result_type(result_dict:RESULT,):
    assert isinstance(result_dict, dict), (
        "returned result is not a `dict`\n"
        "반환된 결과가 `dict`가 아님\n"
        f"{result_dict}"
    )


@pytest.fixture(params=["a_array", "area"])
def dict_key_prefix(request) -> str:
    return request.param


@pytest.fixture
def dict_value_type(dict_key_prefix) -> type:
    return {
        "a_array": np.ndarray,
        "area": float,
    }[dict_key_prefix]


def test_result_has_key(result_dict:RESULT, dict_key_prefix:str, method_number:str,):
    dict_key = '_'.join((dict_key_prefix, method_number))

    assert dict_key in result_dict, (
        f"returned result does not have `{dict_key}`\n"
        f"반환값에 `{dict_key}`가 없음\n"
        f"{result_dict}"
    )


@pytest.fixture
def result_a_array(result_dict:RESULT, method_number:str) -> np.ndarray:
    return result_dict[f'a_array_{method_number}']


@pytest.fixture
def result_area(result_dict:RESULT, method_number:str) -> float:
    return result_dict[f'area_{method_number}']


def test_a_array_type(result_a_array:np.ndarray, method_number:str):
    dict_key = '_'.join(('a_array', method_number))

    assert isinstance(result_a_array, np.ndarray,), (
        f"returned result '{dict_key}' is not an instance of `np.ndarray`\n"
        f"반환된 결과 '{dict_key}' 가 `np.ndarray`가 아님\n"
        f"{result_a_array}"
    )


def test_a_array_dim(result_a_array:np.ndarray, method_number:str, n_rect:int):
    dict_key = '_'.join(('a_array', method_number))

    if method_number in '01':
        expected_len = n_rect
    elif method_number == '2':
        expected_len = n_rect // 2
    else:
        raise NotImplementedError

    msg = (
        f"returned result '{dict_key}' has {len(result_a_array)} areas. expected {expected_len}\n"
        f"반환된 결과 '{dict_key}' 에 {len(result_a_array)} 개의 넓이가 저장됨. 예상 갯수 {expected_len}\n"
        f"{result_a_array}"
    )

    assert len(result_a_array) == (expected_len), msg


def test_area_type(result_area:float, method_number:str):
    dict_key = '_'.join(('area', method_number))

    assert isinstance(result_area, float), (
        f"returned result '{dict_key}' is not an instance of `float`\n"
        f"반환된 결과 '{dict_key}'가 `float`가 아님\n"
        f"{result_area}"
    )


def test_a_array_value(method_number:str, result_a_array:np.ndarray, c_array:np.array, division:float, x1_deg:int, x2_deg:int, n_rect:int):
    q = result_a_array * division

    nt.assert_allclose(
        actual=q, desired=c_array,
        err_msg=(
            f'int_cos_{method_number}(): please verify the area of at each coordinate\n'
            f'int_cos_{method_number}(): 각각의 좌표값에서 넓이 계산을 확인 바랍니다\n'
            f'({x1_deg} deg ~ {x2_deg} deg, {n_rect} areas)'
        )
    )


def test_area_value(method_number:str, result_area:float, c_array:np.array, division:float, x1_deg:int, x2_deg:int, n_rect:int):
    q = result_area * division
    expected_q = np.sum(c_array)

    assert math.isclose(q, expected_q), (
        f"int_cos_{method_number}(): please verify numerical integration result\n"
        f"int_cos_{method_number}(): 적분 결과를 확인 바랍니다\n"
        f"({x1_deg} deg ~ {x2_deg} deg, {n_rect} areas) result = {result_area}"
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
        "compare_int_cos() returned result is not a `dict`\n"
        "compare_int_cos() 가 반환값이 `dict`가 아님\n"
        f"{result_compare_int_cos}"
    )

    assert 'area_exact' in result_compare_int_cos, (
        "compare_int_cos() returned result without `area_exact`\n"
        "compare_int_cos() 반환값에 `area_exact`가 없음\n"
        f"{result_compare_int_cos}"
    )


def test_compare_int_cos_has_area(result_compare_int_cos:RESULT, area_key:str):
    assert area_key in result_compare_int_cos, (
        f"compare_int_cos() returned result without {area_key}\n"
        f"compare_int_cos() 반환값에 `{area_key}`가 없음\n"
        f"{result_compare_int_cos}"
    )


def test_compare_int_cos_has_diff(result_compare_int_cos:RESULT, diff_key:str):
    assert diff_key in result_compare_int_cos, (
        f"compare_int_cos() returned result without `{diff_key}`\n"
        f"compare_int_cos() 반환값에 `{diff_key}`가 없음\n"
        f"{result_compare_int_cos}"
    )


def test_compare_int_cos_has_is_close(result_compare_int_cos:RESULT, is_close_key:str):
    assert is_close_key in result_compare_int_cos, (
        f"compare_int_cos() returned result without `{is_close_key}`\n"
        f"compare_int_cos() 반환값에 `{is_close_key}`가 없음\n"
        f"{result_compare_int_cos}"
    )


@pytest.fixture
def area_key(method_number:str) -> str:
    return 'area_' + method_number


@pytest.fixture
def result_compare_numint(result_compare_int_cos:RESULT, area_key:str) -> float:
    return result_compare_int_cos[area_key]


def test_compare_int_cos__numint_type(result_compare_numint:float, area_key:str):
    assert isinstance(result_compare_numint, float), (
        f"returned result '{area_key}' ({result_compare_numint}) is not an instance of `float`\n"
        f"반환된 결과 '{area_key}' ({result_compare_numint}) 가 `float`가 아님"
    )


def test_compare_int_cos__numint(result_compare_numint:float, result_area:float, method_number:str, area_key:str):
    assert result_compare_numint == result_area, (
        f"'{area_key}' of compare_int_cos() ({result_compare_numint}) is not same as int_cos_{method_number}() ({result_area}) \n"
        f"compare_int_cos() 가 반환된 결과 'area_exact' ({result_compare_numint}) 가 int_cos_{method_number}() 반환 결과 ({result_area}) 와 다름"
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
def diff_key(method_number:str) -> str:
    return 'diff_' + method_number


@pytest.fixture
def result_diff(result_compare_int_cos:RESULT, diff_key:str) -> float:
    return result_compare_int_cos[diff_key]


def test_result_diff_type(result_diff:float, result_area_exact:float, diff_key:str):
    assert isinstance(result_diff, float), f"returned result '{diff_key}' is not an instance of `float`\n반환된 결과 '{diff_key}'가 `float`가 아님"

    assert result_diff >= 0, (
        f"returned result '{diff_key}' {result_diff} is supposed to be an absolute value.\n"
        f"반환된 결과 ' {result_area_exact} = {diff_key}' {result_diff} 는 절대값이어야 함."
    )


@pytest.fixture
def is_close_key(method_number:str) -> str:
    return 'is_close_' + method_number


@pytest.fixture
def result_is_close(result_compare_int_cos:RESULT, is_close_key:str) -> bool:
    return result_compare_int_cos[is_close_key]


def test_result_is_close_type(result_is_close:bool):
    assert isinstance(result_is_close, (np.bool_, bool)), (
        f"returned result 'is_close_0' ({result_is_close}) is not an instance of `bool` ({type(result_is_close)}).\n"
        f"반환된 결과 'is_close_0' ({result_is_close})가 `bool`가 아님 ({type(result_is_close)})."
    )


def test_compare_int_cos_diff(
        result_diff:float,
        expected_exact_int:float,
        c_array:np.array,
        division:float,
        diff_key:str,
    ):

    expected_diff = abs(expected_exact_int - (c_array.sum() / division))

    assert math.isclose(result_diff, expected_diff, rel_tol=0.001), (
        f"please verify `{diff_key}` (result : {result_diff}, expected : {expected_diff}).\n"
        f"`{diff_key}` 값을 확인 바람. (반환된 값 : abs({result_compare_numint} - {result_area_exact})  = {result_diff}, 예상된 값 : abs({(c_array.sum() / division)} - {expected_exact_int})= {expected_diff})"
    )


def test_compare_int_cos_is_close(
        epsilon:float, result_diff:float, result_is_close:bool, is_close_key:str):
    b_is_close = (result_diff < epsilon)
    assert result_is_close == b_is_close, (
        "please verify the comparison result\n"
        "비교 결과를 확인 바랍니다\n"
        f"{result_diff} < {epsilon} ?"
    )


if "__main__" == __name__:
    pytest.main([__file__])
