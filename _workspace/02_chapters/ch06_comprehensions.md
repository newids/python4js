# Chapter 06. 컴프리헨션

> **학습 목표**
> - 리스트 컴프리헨션으로 `map`/`filter` 체인을 대체할 수 있다
> - 조건부·중첩 컴프리헨션을 읽고 쓸 수 있다
> - dict/set 컴프리헨션과 제너레이터 표현식의 차이를 이해한다

## 6.1 리스트 컴프리헨션 — map의 대체

JS에서 `arr.map(f)`로 변환하던 것을 Python은 **컴프리헨션** 문법으로 씁니다. `[표현식 for 변수 in 반복가능]` 형태입니다.

| JavaScript | Python |
|---|---|
| `nums.map(n => n * 2)` | `[n * 2 for n in nums]` |
| `words.map(w => w.length)` | `[len(w) for w in words]` |

```python
nums = [1, 2, 3, 4]
doubled = [n * 2 for n in nums]
print(doubled)
# 출력: [2, 4, 6, 8]
```

`for n in nums`로 원소를 하나씩 꺼내 앞쪽 `n * 2`를 적용한 결과를 새 리스트로 모읍니다. 왼쪽이 "무엇을 담을지", 오른쪽이 "어디서 꺼낼지"입니다.

> ⚠️ **JS 함정**: `map`은 콜백 함수를 받았지만 컴프리헨션은 **표현식**을 직접 씁니다. `return`도 화살표도 없습니다. 함수 호출 오버헤드가 없어 더 빠르고, Python에서 이쪽이 관용적입니다.

## 6.2 조건부 컴프리헨션 — filter의 대체

뒤에 `if 조건`을 붙이면 `filter` 역할을 합니다. `filter`와 `map`을 한 줄에 합칠 수 있어 체이닝이 사라집니다.

| JavaScript | Python |
|---|---|
| `nums.filter(n => n > 0)` | `[n for n in nums if n > 0]` |
| `nums.filter(n=>n>0).map(n=>n*2)` | `[n * 2 for n in nums if n > 0]` |

```python
nums = [-2, -1, 0, 1, 2]
positives = [n for n in nums if n > 0]
doubled_pos = [n * 2 for n in nums if n > 0]
print(positives)
print(doubled_pos)
# 출력: [1, 2]
```

> 🎯 **AICE**: 이 "필터+변환" 사고가 pandas 벡터화(`df[df.col > 0]['col'] * 2`)의 토대입니다. 반복문 대신 한 표현식으로 컬렉션을 변환하는 감각을 여기서 만들어야 Part 2가 수월합니다.

## 6.3 뒤쪽 if와 앞쪽 if-else 구분

`if`의 위치로 의미가 갈립니다. **뒤쪽 `if`**는 원소를 걸러내고(filter), **앞쪽 `if-else`**는 값을 고릅니다(삼항 표현식, 5장).

```python
nums = [-2, -1, 1, 2]
# 뒤쪽 if: 음수를 걸러냄 (개수가 줄어듦)
kept = [n for n in nums if n > 0]
# 앞쪽 if-else: 모든 원소를 변환 (개수 유지)
signs = ["+" if n > 0 else "-" for n in nums]
print(kept)
print(signs)
# 출력: [1, 2]
```

> ⚠️ **JS 함정**: 걸러내기(뒤쪽 `if`)와 값 고르기(앞쪽 `if-else`)를 혼동하면 결과 개수가 달라집니다. "걸러내려면 뒤, 바꾸려면 앞"으로 기억하세요.

## 6.4 dict / set 컴프리헨션

같은 문법을 중괄호로 쓰면 dict나 set이 나옵니다. dict는 `키: 값` 쌍을, set은 단일 값을 담습니다.

| JavaScript | Python |
|---|---|
| `Object.fromEntries(arr.map(...))` | `{k: v for k, v in pairs}` |
| `new Set(arr.map(...))` | `{f(x) for x in arr}` |

```python
words = ["ada", "alan", "grace"]
# dict 컴프리헨션: 단어 → 길이
lengths = {w: len(w) for w in words}
# set 컴프리헨션: 중복 없는 길이 집합
unique_lengths = {len(w) for w in words}
print(lengths)
print(unique_lengths)
# 출력: {'ada': 3, 'alan': 4, 'grace': 5}
```

> ⚠️ **JS 함정**: `{w: len(w) ...}`처럼 `키: 값`이면 dict, `{len(w) ...}`처럼 값 하나면 set입니다. 콜론 유무가 자료구조를 가릅니다.

## 6.5 제너레이터 표현식 — 지연 평가

대괄호 대신 **소괄호**를 쓰면 리스트가 아니라 **제너레이터**가 됩니다. 전체를 메모리에 만들지 않고 필요할 때 하나씩 계산합니다(12장에서 심화). 큰 데이터의 합계·최댓값 등에 유리합니다.

```python
# 리스트를 만들지 않고 곧바로 합산 (메모리 절약)
total = sum(n * n for n in range(1, 5))   # sum() 인자로 직접 전달
print(total)
# 출력: 30
```

`sum()`, `max()`, `any()`, `all()` 같은 집계 함수에 제너레이터 표현식을 직접 넘기면 중간 리스트 없이 처리됩니다.

> ⚠️ **JS 함정**: 제너레이터는 **한 번만** 소비됩니다. 리스트처럼 재사용하려고 두 번 순회하면 두 번째는 비어 있습니다. 여러 번 쓸 값이면 리스트 컴프리헨션(`[...]`)으로 만드세요.

## 6.6 중첩 컴프리헨션

이중 반복문을 한 줄로 폅니다. `for`가 **바깥→안** 순서로 나열됩니다(중첩 for문을 위에서 아래로 읽는 순서 그대로).

```python
matrix = [[1, 2], [3, 4]]
# 2차원 리스트를 1차원으로 평탄화
flat = [x for row in matrix for x in row]
print(flat)
# 출력: [1, 2, 3, 4]
```

`for row in matrix`(바깥)가 먼저, `for x in row`(안)가 나중입니다. 일반 중첩 for문을 그대로 옮겨 적은 순서라 생각하면 헷갈리지 않습니다.

> ⚠️ **JS 함정**: 중첩 `for`의 순서는 바깥이 왼쪽입니다. 결과를 만드는 표현식(`x`)만 맨 앞에 오고, 반복은 읽는 순서대로 이어 붙입니다. 너무 깊어지면 가독성이 나빠지니 2단까지만 권합니다.

## 연습문제

**Q1.** `nums`에서 짝수만 골라 제곱한 리스트를 컴프리헨션으로 만드세요.

```python no-run
nums = [1, 2, 3, 4, 5, 6]
result = [____ for n in nums ____ n % 2 == 0]   # [4, 16, 36]
```

<details><summary>정답</summary>

```python
nums = [1, 2, 3, 4, 5, 6]
result = [n * n for n in nums if n % 2 == 0]
print(result)
# 출력: [4, 16, 36]
```

앞쪽 `n * n`이 변환, 뒤쪽 `if n % 2 == 0`이 짝수 필터입니다.
</details>

**Q2.** 단어 리스트를 {단어: 대문자단어} 딕셔너리로 만드세요.

```python no-run
words = ["ada", "alan"]
upper_map = {w: ____ for w in words}   # {'ada': 'ADA', 'alan': 'ALAN'}
```

<details><summary>정답</summary>

```python
words = ["ada", "alan"]
upper_map = {w: w.upper() for w in words}
print(upper_map)
# 출력: {'ada': 'ADA', 'alan': 'ALAN'}
```

`키: 값` 형태라 dict 컴프리헨션입니다.
</details>

**Q3.** `range(1, 101)`의 제곱합을 중간 리스트 없이 구하세요.

```python no-run
total = sum(____ for n in range(1, 101))
```

<details><summary>정답</summary>

```python
total = sum(n * n for n in range(1, 101))
print(total)
# 출력: 338350
```

소괄호 제너레이터 표현식을 `sum`에 직접 넘겨 메모리를 아낍니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `arr.map(f)` | `[f(x) for x in arr]` | 표현식 직접 |
| `arr.filter(p)` | `[x for x in arr if p(x)]` | 뒤쪽 if |
| `arr.filter().map()` | `[f(x) for x in arr if p(x)]` | 한 줄로 합침 |
| `arr.map(x=>cond?a:b)` | `[a if cond else b for x in arr]` | 앞쪽 if-else |
| `Object.fromEntries(...)` | `{k: v for ...}` | dict 컴프리헨션 |
| `new Set(arr.map(...))` | `{f(x) for x in arr}` | set 컴프리헨션 |
| (지연 평가 없음) | `(f(x) for x in arr)` | 제너레이터, 1회 소비 |
| 이중 `for` + push | `[x for row in m for x in row]` | 중첩(바깥이 왼쪽) |
