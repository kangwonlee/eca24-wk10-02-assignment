
# Integrating $sin \theta$<br>$sin \theta$ 적분

## Description<br>설명

* Using numerical integration of 0th order, please integrate a period of $sin \theta$.<br>0차 수치 적분을 사용하여 $sin \theta$의 한 주기를 적분하시오.

## Implementation<br>구현

* Implement `int_sin_0()` function in `main.py` file.<br>`int_sin_0()` 함수를 `main.py` 파일에 구현하시오.
* Please see `sample.py` file for an example.<br>사용 예에 대해서는 `sample.py` 파일을 참고하시오.
* Arguments of function `int_sin_0()` has one argument : `numpy` array `x_array`.<br>함수 `int_sin_0()` 의 매개변수는 `numpy` 배열 `x_array` 이다.

| argument<br>매개변수 | type<br>형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `x_array` | `numpy` array | rad | coordinates of `x` to calculate sin function<br>sin 값을 계산할 `x` 좌표 |

* Please return a `dict` containing `numpy` array of the area of each rectangle of 0th order integration and the sum of all rectangles as the numerical integration in `float`.<br>`dict`를 반환하시오. value 로 0차 적분의 각 직사각형의 넓이를 담은 배열과 해당 직사각형의 넓이의 합을 `float`로 담으시오.

| key (str)<br>키 (문자열) | type of value<br>value 의 형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `'a_array'` | `numpy` array | - | the area of each rectangle of 0th order integration at `x_array`<br>`x_array`에서의 0차 적분의 각 직사각형의 넓이 |
| `'area'` | `float` | - | the numerical integration<br>해당 수치 적분 값 |
