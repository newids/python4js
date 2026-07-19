# Chapter 12. 이터레이터와 제너레이터

> **학습 목표**
> - iterable과 iterator를 구분하고 `iter()`/`next()`의 동작을 이해한다
> - `yield`로 제너레이터 함수를 만들어 값을 지연 생산한다
> - 지연 평가(lazy evaluation)가 대용량 데이터 처리에 왜 유리한지 안다
> - JS의 `function*`/`Symbol.iterator`와의 대응을 파악한다

## 12.1 iterable과 iterator — 순회의 두 역할

JS에서 `for...of`가 도는 대상은 `Symbol.iterator`를 가진 iterable입니다. Python도 같은 구조입니다. **iterable**은 `iter()`로 iterator를 만들 수 있는 객체(list·dict·문자열)이고, **iterator**는 `next()`로 값을 하나씩 꺼내는 객체입니다.

| JavaScript | Python |
|---|---|
| ```const it = arr[Symbol.iterator]();``` | ```it = iter(lst)``` |
| ```it.next().value``` | ```next(it)``` |

`iter()`로 iterator를 얻고 `next()`로 값을 하나씩 꺼냅니다. 값이 소진되면 `StopIteration` 예외가 납니다 — JS의 `{ done: true }`에 해당합니다.

```python
lst = [10, 20, 30]
it = iter(lst)

print(next(it))
# 출력: 10
print(next(it))
# 출력: 20
print(next(it))
# 출력: 30
```

`for x in lst`는 내부적으로 `iter()`를 호출하고 `StopIteration`이 날 때까지 `next()`를 반복하는 문법 설탕입니다. JS `for...of`와 동작 원리가 완전히 같습니다.

## 12.2 yield — 제너레이터 함수

`yield`가 들어간 함수는 일반 함수가 아니라 **제너레이터 함수**가 됩니다. JS의 `function*`와 정확히 대응합니다. 호출해도 본문이 즉시 실행되지 않고, 제너레이터 객체를 반환합니다. `next()`를 부를 때마다 다음 `yield`까지 실행되고 값을 내놓은 뒤 그 자리에서 멈춥니다.

| JavaScript | Python |
|---|---|
| ```function* gen() {```<br>```  yield 1; yield 2;```<br>```}``` | ```def gen():```<br>```    yield 1```<br>```    yield 2``` |

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

gen = count_up_to(3)
print(list(gen))
# 출력: [1, 2, 3]
```

제너레이터는 그 자체가 iterator이므로 `for`로 순회하거나 `list()`로 한꺼번에 모을 수 있습니다. 함수의 실행 상태(지역 변수 `i`)가 `yield` 사이에 그대로 보존된다는 점이 핵심입니다.

```python
def fibonacci(count):
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b

print(list(fibonacci(7)))
# 출력: [0, 1, 1, 2, 3, 5, 8]
```

## 12.3 지연 평가 — 필요할 때 하나씩

제너레이터의 진짜 가치는 **값을 미리 다 만들지 않는다**는 데 있습니다. 리스트는 모든 원소를 메모리에 올리지만, 제너레이터는 요청받을 때마다 한 개씩 계산합니다. 백만 개를 다뤄도 메모리에는 한 번에 하나만 있습니다.

6장에서 본 제너레이터 표현식이 바로 이 지연 평가입니다. 대괄호 대신 소괄호를 쓰면 리스트가 아니라 제너레이터가 됩니다.

```python
squares_list = [x ** 2 for x in range(5)]     # 즉시 다 계산
squares_gen = (x ** 2 for x in range(5))      # 지연 — 아직 계산 안 함

print(squares_list)
# 출력: [0, 1, 4, 9, 16]
print(squares_gen)
# 출력: <generator object
print(sum(squares_gen))
# 출력: 30
```

`squares_gen`을 출력하면 값이 아니라 제너레이터 객체가 보입니다. `sum()`이 순회하는 순간 비로소 값이 하나씩 만들어집니다.

> ⚠️ **JS 함정**: 제너레이터는 **한 번만** 순회할 수 있습니다. JS 배열은 몇 번이고 다시 돌 수 있지만, Python 제너레이터는 소진되면 끝입니다. 아래처럼 두 번째 순회는 빈 결과가 됩니다.

```python
gen = (x for x in range(3))
print(list(gen))
# 출력: [0, 1, 2]
print(list(gen))   # 이미 소진됨
# 출력: []
```

> 🎯 **AICE**: Professional 트랙의 대용량 데이터 처리에서 제너레이터 사고가 바탕이 됩니다. pandas의 `read_csv(..., chunksize=1000)`은 DataFrame을 통째로 올리지 않고 청크 단위로 내주는 iterator를 반환하는데, 이것이 지연 평가의 실전 응용입니다. 메모리에 다 못 올리는 데이터를 조각내 처리하는 관점을 여기서 익혀 둡니다.

## 연습문제

**Q1.** iterator에서 값을 하나씩 꺼내도록 빈칸을 채우세요.

```python no-run
it = ____([100, 200])
print(____(it))   # 100
print(next(it))   # 200
```

<details><summary>정답</summary>

```python
it = iter([100, 200])
print(next(it))
# 출력: 100
print(next(it))
# 출력: 200
```

`iter()`로 iterator를 만들고 `next()`로 값을 꺼냅니다.
</details>

**Q2.** 0부터 n까지 짝수를 지연 생산하는 제너레이터입니다. 빈칸을 채우세요.

```python no-run
def evens(n):
    for i in range(0, n + 1, 2):
        ____ i

print(list(evens(8)))   # [0, 2, 4, 6, 8]
```

<details><summary>정답</summary>

```python
def evens(n):
    for i in range(0, n + 1, 2):
        yield i

print(list(evens(8)))
# 출력: [0, 2, 4, 6, 8]
```

`yield`가 함수를 제너레이터로 바꿔 값을 하나씩 내보냅니다.
</details>

**Q3.** 메모리를 아끼는 제너레이터 표현식으로 빈칸을 채우세요. (리스트가 아니어야 합니다)

```python no-run
big_sum = sum____x * 2 for x in range(1000)____
print(big_sum)   # 999000
```

<details><summary>정답</summary>

```python
big_sum = sum(x * 2 for x in range(1000))
print(big_sum)
# 출력: 999000
```

`sum()` 안에 소괄호 제너레이터 표현식을 넣으면 값을 하나씩 만들어 더해 메모리를 절약합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `arr[Symbol.iterator]()` | `iter(lst)` | iterator 생성 |
| `it.next().value` | `next(it)` | 다음 값 꺼내기 |
| `{ done: true }` | `StopIteration` | 소진 신호 |
| `function* () { yield }` | `def f(): yield` | 제너레이터 함수 |
| (배열은 재순회 가능) | 제너레이터 1회 소진 | 다시 못 돎 |
| (없음 — 즉시 평가) | 지연 평가 `(x for x in ...)` | 대용량 데이터 |
