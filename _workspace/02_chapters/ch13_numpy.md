# Chapter 13. NumPy 기초

> **학습 목표**
> - ndarray를 생성하고 dtype·shape로 배열의 구조를 파악할 수 있다
> - 인덱싱·슬라이싱과 불리언 마스크로 원하는 원소를 선택할 수 있다
> - for 루프 없이 벡터화 연산과 브로드캐스팅으로 배열을 계산할 수 있다
> - axis 인자로 행·열 방향 집계를 구분해 수행할 수 있다

JS에는 대응이 없는 첫 개념입니다. `Array`는 있지만 "숫자 n차원 배열을 한 번에 계산하는" 도구는 없습니다(`TypedArray`가 가장 가깝지만 벡터 연산은 없습니다). NumPy의 `ndarray`는 pandas와 scikit-learn이 딛고 선 토대이고, AICE 실기의 모든 데이터가 결국 이 배열 위에서 움직입니다. 이 챕터에서 얻어야 할 단 하나는 **"루프 대신 배열 통째로 계산한다"**는 사고 전환입니다.

## 13.1 ndarray 생성 — 리스트를 배열로

Python 리스트는 벡터 연산을 못 합니다. `[1,2,3] * 2`는 원소가 2배가 아니라 리스트가 2번 반복됩니다(JS의 배열과 같은 함정). 계산이 목적이면 `np.array`로 감쌉니다.

| JavaScript | Python (NumPy) |
|---|---|
| `const a = new Float64Array([1,2,3]);` | `a = np.array([1, 2, 3])` |
| `a.length` | `a.shape` |

```python
import numpy as np

nums = [1, 2, 3]
print(nums * 2)          # 리스트: 반복
# 출력: [1, 2, 3, 1, 2, 3]

arr = np.array([1, 2, 3])
print(arr * 2)           # 배열: 원소별 2배
# 출력: [2 4 6]
```

자주 쓰는 생성 함수들입니다. AICE 실기에서 초기 배열·가중치·더미 데이터를 만들 때 등장합니다.

```python
z = np.zeros(3)                 # [0. 0. 0.]
o = np.ones((2, 3))             # 2행 3열 1로 채움
r = np.arange(0, 10, 2)         # range의 배열판
print(r)
# 출력: [0 2 4 6 8]

lin = np.linspace(0, 1, 5)      # 0~1 균등 5개
print(lin)
# 출력: [0.   0.25 0.5  0.75 1.  ]
```

> ⚠️ **함정**: `arr * 2`가 원소별 연산인 것은 NumPy 배열일 때만입니다. 순수 Python 리스트에 `* 2`를 쓰면 JS `Array.prototype.concat`처럼 **이어붙이기**가 됩니다. 벡터 연산이 필요하면 먼저 `np.array`로 변환하세요.

## 13.2 dtype와 shape — 배열의 신분증

배열은 리스트와 달리 **원소 타입이 하나로 고정**됩니다. `dtype`이 그 타입, `shape`가 차원 구조입니다.

```python
mat = np.array([[1, 2, 3],
                [4, 5, 6]])
print(mat.shape)     # (행, 열)
# 출력: (2, 3)
print(mat.ndim)      # 차원 수
# 출력: 2
print(mat.dtype)     # 원소 타입
# 출력: int64
```

정수 배열에 실수를 섞으면 전체가 `float64`로 올라갑니다. 타입을 바꾸려면 `astype`을 씁니다.

```python
f = np.array([1, 2, 3], dtype="float64")
print(f)
# 출력: [1. 2. 3.]

i = f.astype("int64")
print(i.dtype)
# 출력: int64
```

`reshape`로 shape를 바꿉니다. 원소 수만 맞으면 됩니다. `-1`은 "나머지 자동 계산"입니다.

```python
a = np.arange(6)
print(a.reshape(2, 3))
# 출력: [[0 1 2]
print(a.reshape(3, -1).shape)   # -1 = 자동
# 출력: (3, 2)
```

> 🎯 **AICE**: 모델에 데이터를 넣기 전 `X.shape`를 찍어 `(샘플 수, 특성 수)`를 확인하는 것은 실기의 기본 습관입니다. shape가 맞지 않아 나는 에러가 가장 흔하므로, 배열을 만들 때마다 shape를 눈으로 확인하세요.

## 13.3 인덱싱과 슬라이싱 — 리스트 문법의 확장

1차원 인덱싱·슬라이싱은 4장에서 배운 리스트와 똑같습니다. 새로운 것은 **2차원을 쉼표로 접근**하는 문법입니다. JS에서 `mat[i][j]`로 쓰던 것을 NumPy는 `mat[i, j]` 한 쌍으로 씁니다.

| JavaScript | Python (NumPy) |
|---|---|
| `mat[0][1]` | `mat[0, 1]` |
| `mat.map(row => row[0])` | `mat[:, 0]` (0열 전체) |

```python
mat = np.array([[10, 20, 30],
                [40, 50, 60]])
print(mat[0, 1])       # 0행 1열
# 출력: 20
print(mat[:, 0])       # 모든 행의 0열
# 출력: [10 40]
print(mat[1, :])       # 1행 전체
# 출력: [40 50 60]
print(mat[:, 1:])      # 1열부터 끝까지
# 출력: [[20 30]
```

**불리언 인덱싱**은 pandas의 핵심 전환점으로 이어지는 가장 중요한 문법입니다. 조건식이 True/False 배열을 만들고, 그 마스크로 원소를 골라냅니다.

```python
data = np.array([12, 5, 30, 8, 21])
mask = data > 10
print(mask)
# 출력: [ True False  True False  True]
print(data[data > 10])     # 마스크로 필터
# 출력: [12 30 21]

data[data > 10] = 0        # 조건부 대입도 가능
print(data)
# 출력: [ 0  5  0  8  0]
```

> ⚠️ **함정**: 조건을 여러 개 결합할 때 `and`/`or`가 아니라 `&`/`|`를 쓰고, 각 조건을 **괄호로 감싸야** 합니다. `(data > 10) & (data < 25)`가 맞고, `data > 10 and data < 25`는 에러입니다. 연산자 우선순위 때문에 괄호를 빠뜨리면 조용히 틀립니다.

```python
d = np.array([12, 5, 30, 8, 21])
print(d[(d > 10) & (d < 25)])
# 출력: [12 21]
```

## 13.4 벡터화 연산 — 루프를 지운다

이 챕터의 핵심입니다. JS라면 `for`나 `map`으로 돌 계산을, NumPy는 배열 통째로 한 줄에 씁니다. C 레벨에서 실행되므로 빠르고, 무엇보다 코드가 수식 그대로입니다.

**JavaScript**

```javascript
const celsius = [0, 25, 100];
const fahrenheit = celsius.map(c => c * 9 / 5 + 32);
// [32, 77, 212]
```

**Python (NumPy)**

```python
celsius = np.array([0, 25, 100])
fahrenheit = celsius * 9 / 5 + 32     # 루프 없음
print(fahrenheit)
# 출력: [ 32.  77. 212.]
```

배열끼리의 연산도 원소별로 정렬되어 계산됩니다. 내장 함수(`np.sqrt`, `np.exp`, `np.log` 등)도 전부 벡터화되어 있습니다.

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print(a + b)
# 출력: [11 22 33]
print(np.sqrt(np.array([1, 4, 9])))
# 출력: [1. 2. 3.]
```

> 🎯 **AICE**: 파생 변수를 만들 때 `df['bmi'] = df['weight'] / (df['height'] ** 2)`처럼 열 전체를 한 번에 계산하는 것이 이 벡터화 사고입니다. pandas의 열(Series)이 내부적으로 NumPy 배열이라, 여기서 익힌 감각이 그대로 이어집니다.

## 13.5 브로드캐스팅 — 모양이 다른 배열의 연산

shape가 다른 배열끼리 연산할 때, NumPy는 작은 쪽을 자동으로 "펼쳐" 맞춥니다. 이것이 브로드캐스팅입니다. 가장 흔한 경우는 배열과 스칼라(위에서 `* 2`가 이미 브로드캐스팅입니다)이고, 그다음이 행렬의 각 행/열에 벡터를 더하는 경우입니다.

```python
mat = np.array([[1, 2, 3],
                [4, 5, 6]])
col_mean = mat.mean(axis=0)     # 열별 평균: [2.5 3.5 4.5]
centered = mat - col_mean       # (2,3) - (3,) → 행마다 빼기
print(centered)
# 출력: [[-1.5 -1.5 -1.5]
#        [ 1.5  1.5  1.5]]
```

규칙은 "뒤 차원부터 맞춰보고, 크기가 같거나 한쪽이 1이면 늘린다"입니다. 표준화(각 열에서 평균을 빼고 표준편차로 나누기)가 정확히 이 패턴이며, 15장 스케일링의 밑그림입니다.

```python
std = mat.std(axis=0)
standardized = (mat - col_mean) / std
print(standardized.mean(axis=0).round(1))   # 각 열 평균 0
# 출력: [0. 0. 0.]
```

> ⚠️ **함정**: 브로드캐스팅은 shape가 규칙에 맞을 때만 동작합니다. `(2,3)` 배열에 크기 2인 벡터를 더하면 `ValueError`가 납니다. "한쪽이 1이거나 크기가 같아야 한다"를 기억하세요. 열 방향으로 맞추고 싶으면 `(2,1)` 모양으로 `reshape`해야 합니다.

## 13.6 축(axis) 집계 — 행이냐 열이냐

`sum`, `mean`, `max` 같은 집계 함수에 `axis`를 주면 방향이 정해집니다. **`axis=0`은 행을 따라 아래로(→ 열별 결과), `axis=1`은 열을 따라 옆으로(→ 행별 결과)**입니다. 이 방향 감각이 pandas `groupby`까지 이어집니다.

```python
mat = np.array([[1, 2, 3],
                [4, 5, 6]])
print(mat.sum())            # 축 없음: 전체 합
# 출력: 21
print(mat.sum(axis=0))      # 열별 합 (세로로 접기)
# 출력: [5 7 9]
print(mat.sum(axis=1))      # 행별 합 (가로로 접기)
# 출력: [ 6 15]
```

> 🎯 **AICE**: "각 특성(열)의 평균"이 필요하면 `axis=0`, "각 샘플(행)의 합"이 필요하면 `axis=1`입니다. 헷갈릴 때는 "없어지는 축이 axis"라고 외우세요. `axis=0`을 주면 행 방향이 접혀 사라지고 열별 결과가 남습니다.

## 연습문제

**Q1.** 1부터 12까지의 정수를 3행 4열 배열로 만들려고 합니다. 빈칸을 채우세요.

```python no-run
import numpy as np
arr = np.arange(1, ____).____(3, 4)
print(arr.shape)   # (3, 4)
```

<details><summary>정답</summary>

```python
import numpy as np
arr = np.arange(1, 13).reshape(3, 4)
print(arr.shape)
# 출력: (3, 4)
```

`arange(1, 13)`은 1~12(끝값 제외)로 12개를 만들고, `reshape(3, 4)`로 3×4에 담습니다.
</details>

**Q2.** 배열 `scores`에서 60점 이상인 값만 골라내려 합니다. 빈칸을 채우세요.

```python no-run
scores = np.array([50, 72, 88, 41, 65])
passed = scores[____ >= 60]
print(passed)   # [72 88 65]
```

<details><summary>정답</summary>

```python
scores = np.array([50, 72, 88, 41, 65])
passed = scores[scores >= 60]
print(passed)
# 출력: [72 88 65]
```

불리언 마스크 `scores >= 60`이 True/False 배열을 만들고, 대괄호 안에 넣으면 True 위치만 남습니다.
</details>

**Q3.** 2차원 배열 `mat`의 **열별 평균**을 구하려 합니다. 빈칸을 채우세요.

```python no-run
mat = np.array([[1, 2], [3, 4], [5, 6]])
col_avg = mat.mean(axis=____)
print(col_avg)   # [3. 4.]
```

<details><summary>정답</summary>

```python
mat = np.array([[1, 2], [3, 4], [5, 6]])
col_avg = mat.mean(axis=0)
print(col_avg)
# 출력: [3. 4.]
```

열별 결과를 원하므로 행 방향(axis=0)을 접습니다. "없어지는 축이 axis"를 기억하세요.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python (NumPy) | 비고 |
|----|--------|------|
| `new Float64Array([...])` | `np.array([...])` | 벡터 연산 가능한 배열 |
| `arr.length` | `arr.shape` | shape는 튜플(다차원) |
| `mat[i][j]` | `mat[i, j]` | 쉼표로 다차원 접근 |
| `arr.map(f)` | `arr` 통째 벡터 연산 | 루프·map 불필요 |
| `arr.filter(x => x > 10)` | `arr[arr > 10]` | 불리언 인덱싱 |
| 조건 결합 `&&` / `\|\|` | `&` / `\|` (괄호 필수) | `and`/`or` 아님 |
| `arr.reduce((a,b)=>a+b)` | `arr.sum()` / `arr.sum(axis=0)` | axis로 방향 지정 |
