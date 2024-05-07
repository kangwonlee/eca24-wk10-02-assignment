
# Integrating $cos\theta$ instead of $sin \theta$<br>$sin \theta$ 대신 $cos \theta$ 적분

## Description<br>설명

* Using numerical integration of 0th order, please integrate a period of $cos \theta$ (instead of $sin \theta$ in the video).<br>0차 수치 적분을 사용하여 (비디오에서는 $sin \theta$ 였지만) $cos \theta$의 한 주기를 적분하시오.

## Implementation<br>구현

* Implement `int_cos_0()` function in `main.py` file.<br>`int_cos_0()` 함수를 `main.py` 파일에 구현하시오.
* Please see `sample.py` file for an example.<br>사용 예에 대해서는 `sample.py` 파일을 참고하시오.
* Function `int_cos_0()` has three argument : `theta_rad_begin`, `theta_rad_end`, and `n`.<br>함수 `int_cos_0()` 의 매개변수는 `theta_begin`, `theta_end`, 그리고 `n` 이다.

| argument<br>매개변수 | type<br>형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `theta_rad_begin` | `float` | rad | lower bound of the integral<br>적분구간의 하한 |
| `theta_rad_end` | `float` | rad | upper bound of the integral<br>적분구간의 상한 |
| `n` | `int` | - | number of equally spaced rectangles between the bounds<br>적분 구간을 등간격으로 나눈 직사각형 갯수 |

* Please return a `dict` containing `numpy` array of the area of each rectangle of 0th order integration and the sum of all rectangles as the numerical integration in `float`.<br>`dict`를 반환하시오. value 로 0차 적분의 각 직사각형의 넓이를 담은 배열과 해당 직사각형의 넓이의 합을 `float`로 담으시오.

| key (str)<br>키 (문자열) | type of value<br>value 의 형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `'a_array_0'` | `numpy` array | - | the `n` areas of rectangles of 0th order integration<br>0차 적분의 `n`개의 직사각형의 넓이 |
| `'area_0'` | `float` | - | the numerical integration<br>해당 수치 적분 값 |
