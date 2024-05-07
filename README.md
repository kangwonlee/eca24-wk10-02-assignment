
# Probability of the length<br>길이의 확률

## Description<br>설명

* There is a machine cutting a long wire into shorter pieces.<br>철사를 잘게 자르는 기계가 있다.
* The length of each cut piece `x`[m] would follow a probability distribution whose probability distribution function (PDF) is `f(x)`.<br>자른 철사의 길이 `x`[m] 는 확률 밀도 함수가 `f(x)`인 확률 분포를 따른다.
* Using numerical integration, calculate the probability that the length be between `x1`[m] and `x2`[m].<br>수치 적분을 사용하여 길이가 `x1`[m] 과 `x2`[m] 사이에 있을 확률을 계산하시오.

## Implementation<br>구현

* Implement `probability_between()` function in `main.py` file.<br>`probability_between()` 함수를 `main.py` 파일에 구현하시오.
* Please see `sample.py` file for an example.<br>사용 예에 대해서는 `sample.py` 파일을 참고하시오.
* Arguments of function `probability_between()` are `Callable` `f`, `x1` in `float`, and `x2` in `float`.<br>함수 `probability_between()` 의 매개변수는 함수 `f`, `float` 형 `x1`, `float` 형 `x2` 이다.

| argument<br>매개변수 | type<br>형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `f` | `Callable[[float], float]` | probability<br>확률 | `f(x)` is the probability distribution function of length `x` [m]<br>`f(x)` 는 길이 `x` [m]의 확률 밀도 함수 |
| `x1` | `float` | m | lower bound of length `x` [m]<br>길이 `x` [m]의 하한 |
| `x2` | `float` | m | upper bound of length `x` [m]<br>길이 `x` [m]의 상한 |

* The function `f(x)` is the probability distribution function (PDF) of the length `x`[m] of the cut piece.<br>`f(x)` 함수는 자른 철사의 길이 `x`[m]의 확률 분포 함수(PDF)이다.

| argument<br>매개변수 | type<br>형 | unit<br>단위 | description<br>설명 |
|:-----------------:|:----------:|:----------:|:------------------:|
| `x` | `float` | m | length `x` [m]<br>길이 `x` |

* Please return the probability that the length be between `x1` and `x2` in `float`.<br>길이가 `x1` 과 `x2` 사이에 있을 확률을 `float` 형으로 반환하시오.
* You can use `scipy.integrate` for numerical integration.<br>수치 적분을 위해 `scipy.integrate` 를 사용할 수 있다.

## Example<br>예시
```python
import scipy.stats

def f(x, ave=1.0, std=0.1):
    return scipy.stats.norm.pdf(x, loc=ave, scale=std)

p = probability_between(f, 0.9, 1.1)
```
* `p` is the probability that the length be between 0.9 and 1.1.<br>`p` 는 길이가 0.9 와 1.1 사이에 있을 확률이다.
