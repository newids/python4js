# Chapter 08. 스코프와 클로저

> **학습 목표**
> - Python이 함수 단위 스코프(LEGB)를 쓰며 if/for 블록은 스코프를 만들지 않음을 이해한다
> - `global`/`nonlocal`로 바깥 스코프 변수를 재할당할 수 있다
> - 클로저를 만들어 상태를 캡처하고, JS와 같은 렉시컬 캡처 원리를 확인한다
> - 루프 안 클로저의 늦은 바인딩 함정을 `lambda x=x:` 트릭으로 회피할 수 있다

## 8.1 스코프의 단위 — 블록이 아니라 함수

JS는 `let`/`const` 도입 후 블록 스코프를 씁니다. `{ }` 안에서 선언한 변수는 그 블록을 벗어나면 사라집니다. Python은 다릅니다. **스코프의 단위는 함수**이며, `if`·`for`·`while` 블록은 새 스코프를 만들지 않습니다.

| JavaScript | Python |
|---|---|
| ```if (true) { let x = 1; }```<br>```// x는 여기서 접근 불가``` | ```if True:```<br>```    x = 1```<br>```# x는 여기서 접근 가능``` |

아래 코드에서 `for` 블록 안에서 만든 변수가 루프 밖에서도 살아 있습니다. JS라면 블록 스코프 변수가 새어 나오지 않지만, Python에서는 정상입니다.

```python
for i in range(3):
    last = i

print(last)
# 출력: 2
print(i)
# 출력: 2
```

Python의 스코프 탐색 규칙을 **LEGB**라고 부릅니다. 이름을 찾을 때 Local(현재 함수) → Enclosing(감싸는 함수) → Global(모듈) → Built-in(내장) 순으로 올라갑니다. JS의 렉시컬 스코프 체인과 개념이 같되, 계층 이름이 정해져 있다고 보면 됩니다.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)   # Local에 없으니 Enclosing에서 찾음
    inner()

outer()
# 출력: enclosing
```

> 🎯 **AICE**: 실기는 Jupyter 노트북에서 진행되며, **모든 셀이 하나의 전역(Global) 네임스페이스를 공유**합니다. 앞 셀에서 만든 `df`, `model` 같은 변수가 뒤 셀에 그대로 남아 있어 편리하지만, 셀을 위아래로 오가며 실행하면 이전 값이 살아 있어 엉뚱한 결과가 나오는 실수가 잦습니다. 채점 전에는 반드시 `Kernel → Restart & Run All`로 위에서 아래로 한 번에 다시 실행해, 전역 네임스페이스를 깨끗한 상태에서 재구성했는지 확인하세요.

## 8.2 읽기는 되지만 재할당은 막힌다 — global과 nonlocal

여기서 JS 개발자가 놀라는 지점이 나옵니다. 바깥 스코프 변수를 **읽는 것**은 자유지만, 함수 안에서 그 변수에 **값을 재할당**하면 Python은 그것을 새로운 지역 변수로 간주합니다.

```python
count = 0

def increment():
    # count = count + 1  # 이렇게 하면 UnboundLocalError
    return count + 1     # 읽기만 하면 문제없음

print(increment())
# 출력: 1
```

바깥 변수를 진짜로 재할당하려면 의도를 명시해야 합니다. 모듈 전역 변수는 `global`, 감싸는 함수의 변수는 `nonlocal`을 선언합니다.

```python
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)
# 출력: 2
```

```python
def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step

counter = make_counter()
print(counter())
# 출력: 1
print(counter())
# 출력: 2
```

> ⚠️ **JS 함정**: JS는 `count++`로 바깥 변수를 그냥 수정합니다. Python에서 함수 안 `count += 1`은 `global`/`nonlocal` 선언이 없으면 "지역 변수 count를 읽어서 더한다"로 해석되어 `UnboundLocalError`가 납니다. 재할당 의도가 있으면 반드시 선언하세요. 단, 리스트에 `.append()`처럼 **객체를 변형**하는 것은 재할당이 아니므로 선언이 필요 없습니다.

## 8.3 클로저 — 렉시컬 캡처는 JS와 같다

`make_counter`가 이미 클로저입니다. 안쪽 함수가 바깥 함수의 지역 변수를 기억한 채 반환되는 구조로, JS의 클로저와 원리가 동일합니다. 함수 팩토리 패턴도 그대로 옮겨집니다.

```python
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(10), triple(10))
# 출력: 20 30
```

각 클로저가 자기만의 `factor`를 캡처합니다. 여기까지는 JS 개발자에게 익숙한 그림입니다.

## 8.4 루프 클로저 늦은 바인딩 함정

JS `var` 시절의 악명 높은 함정이 Python에 그대로 존재합니다. 반복문에서 클로저를 만들면, 클로저는 루프 변수의 **값**이 아니라 **변수 자체**를 캡처합니다. 루프가 끝난 뒤 함수를 호출하면 모두 마지막 값을 봅니다.

```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
# 출력: [2, 2, 2]
```

`[0, 1, 2]`를 기대했지만 `[2, 2, 2]`가 나옵니다. 세 클로저가 모두 같은 `i`를 참조하고, 루프가 끝났을 때 `i`는 2이기 때문입니다. JS의 `for (var i ...)` 함정과 완전히 같은 현상입니다.

> ⚠️ **JS 함정**: JS는 `let`으로 루프마다 새 바인딩을 만들어 이 문제를 해결했습니다. Python에는 그런 마법이 없습니다. 값을 그 시점에 고정하려면 기본 인자를 이용하는 관용구 `lambda i=i:`를 씁니다 — 기본값은 정의 시점에 평가되므로 현재 값이 즉시 캡처됩니다.

```python
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)   # 기본 인자로 현재 값을 고정

print([f() for f in funcs])
# 출력: [0, 1, 2]
```

`lambda i=i:`에서 오른쪽 `i`는 루프의 현재 값으로 즉시 평가되어 기본값으로 박제됩니다. 7장의 "기본값은 정의 시점에 한 번 평가된다" 규칙이 여기서는 오히려 해결책이 됩니다.

## 연습문제

**Q1.** 함수 안에서 전역 변수 `total`을 누적하려 합니다. 빈칸을 채우세요.

```python no-run
total = 0

def add(n):
    ____ total
    total += n

add(5)
add(3)
print(total)   # 8
```

<details><summary>정답</summary>

```python
total = 0

def add(n):
    global total
    total += n

add(5)
add(3)
print(total)
# 출력: 8
```

전역 변수를 재할당하려면 `global` 선언이 필요합니다.
</details>

**Q2.** 루프에서 만든 클로저가 각자 다른 값을 반환하도록 빈칸을 채우세요.

```python no-run
adders = []
for n in range(3):
    adders.append(lambda x, ____: x + n)

print(adders[0](10), adders[1](10), adders[2](10))   # 10 11 12
```

<details><summary>정답</summary>

```python
adders = []
for n in range(3):
    adders.append(lambda x, n=n: x + n)

print(adders[0](10), adders[1](10), adders[2](10))
# 출력: 10 11 12
```

`n=n` 기본 인자가 루프의 현재 값을 즉시 캡처해 늦은 바인딩을 막습니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| 블록 스코프(`let`/`const`) | 함수 스코프(LEGB) | if/for는 스코프 아님 |
| 렉시컬 스코프 체인 | LEGB 탐색 순서 | 개념 동일 |
| 바깥 변수 그냥 수정 | `global`/`nonlocal` 선언 | 재할당엔 선언 필수 |
| 클로저(함수 팩토리) | 클로저(동일 원리) | 렉시컬 캡처 |
| `let`이 루프마다 새 바인딩 | 늦은 바인딩 함정 존재 | `lambda x=x:` 트릭 |
