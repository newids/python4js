# Chapter 05. 제어 흐름

> **학습 목표**
> - 들여쓰기 기반 블록 구조와 "블록 스코프 없음"을 이해할 수 있다
> - `for ... in`, `range`, `enumerate`, `zip`으로 Python식 순회를 작성할 수 있다
> - 삼항 표현식의 어순(값-조건-값)과 `while`을 올바르게 쓸 수 있다

## 5.1 들여쓰기 블록 — 중괄호가 없다

Python은 `{}` 대신 **들여쓰기**로 블록을 구분합니다. 조건문 끝에 콜론(`:`)을 붙이고 다음 줄을 들여씁니다. 세미콜론도 쓰지 않습니다.

| JavaScript | Python |
|---|---|
| `if (x > 0) { ... }` | `if x > 0:` + 들여쓰기 |
| `else if` | `elif` |

```python
x = 7
if x > 10:
    print("큼")
elif x > 5:
    print("중간")
else:
    print("작음")
# 출력: 중간
```

`else if`가 아니라 `elif`입니다. 조건에 괄호는 선택 사항이라 보통 생략합니다.

> ⚠️ **JS 함정**: 들여쓰기가 문법입니다. 스페이스 4칸이 관례이며, 탭과 스페이스를 섞으면 `IndentationError`가 납니다. JS처럼 자유롭게 들여써도 되던 감각을 버려야 합니다.

## 5.2 블록 스코프가 없다

JS의 `let`은 `if`/`for` 블록 안에 갇혔지만, Python의 블록은 **스코프를 만들지 않습니다**. 블록 안에서 만든 변수가 블록 밖에서도 살아있습니다(함수 단위 스코프 — 8장에서 심화).

```python
if True:
    leaked = 42        # 블록 안에서 정의했지만
print(leaked)          # 블록 밖에서도 접근됨
# 출력: 42
```

> ⚠️ **JS 함정**: `if`/`for` 블록은 스코프 경계가 아닙니다. `for` 루프가 끝난 뒤에도 루프 변수가 마지막 값으로 남아있습니다. `let`의 블록 격리를 기대하면 안 됩니다.

## 5.3 `for ... in` — for...of의 대응물

JS의 `for...of`가 Python의 기본 `for`입니다. 인덱스 기반 `for(let i=0; ...)`는 거의 쓰지 않고, 값을 직접 순회합니다.

| JavaScript | Python |
|---|---|
| `for (const x of arr)` | `for x in arr:` |
| `for (const k in obj)` | `for k in d:`  # 키 순회 |

```python
for fruit in ["apple", "banana"]:
    print(fruit)
# 출력: apple
```

> ⚠️ **JS 함정**: JS의 `for...in`(키/인덱스)과 `for...of`(값)를 혼동하지 마세요. Python `for x in`은 항상 **값**을 줍니다(리스트면 원소, dict면 키).

## 5.4 range — 인덱스가 필요할 때

C 스타일 카운팅 루프가 필요하면 `range`를 씁니다. `range(stop)` 또는 `range(start, stop, step)` 형태로, `stop`은 포함하지 않습니다.

```python
for i in range(3):        # 0, 1, 2
    print(i)
print(list(range(2, 10, 2)))   # start, stop, step
# 출력: 0
```

## 5.5 enumerate — 인덱스와 값을 함께

JS의 `arr.forEach((v, i) => ...)`나 `arr.entries()`에 대응합니다. `enumerate`는 (인덱스, 값) 쌍을 튜플로 내줍니다.

| JavaScript | Python |
|---|---|
| `arr.forEach((v, i)=>...)` | `for i, v in enumerate(arr):` |
| `arr.entries()` | `enumerate(arr)` |

```python
colors = ["red", "green", "blue"]
for i, color in enumerate(colors):
    print(i, color)
# 출력: 0 red
```

시작 인덱스를 바꾸려면 `enumerate(colors, start=1)`처럼 둘째 인자를 줍니다.

## 5.6 zip — 여러 시퀀스를 나란히

여러 리스트를 인덱스로 맞춰 동시에 순회합니다. JS에는 내장이 없어 `map`으로 흉내 내던 패턴입니다.

```python
names = ["ada", "alan"]
ages = [36, 41]
for name, age in zip(names, ages):
    print(f"{name}: {age}")
# 출력: ada: 36
```

`zip`은 가장 짧은 시퀀스 길이에 맞춰 멈춥니다. 두 리스트를 dict로 묶을 때도 `dict(zip(keys, values))`로 자주 씁니다.

> 🎯 **AICE**: `enumerate`와 `zip`은 컬럼 목록과 값 목록을 짝지어 순회하거나, 결과에 번호를 붙일 때 실기에서 자주 등장합니다.

## 5.7 삼항 표현식 — 어순이 뒤집힌다

JS의 `cond ? a : b`가 Python에서는 **`a if cond else b`**입니다. 참일 때 값이 맨 앞에 오는 값-조건-값 어순입니다.

| JavaScript | Python |
|---|---|
| `x > 0 ? "양" : "음"` | `"양" if x > 0 else "음"` |

```python
score = 72
grade = "pass" if score >= 60 else "fail"
print(grade)
# 출력: pass
```

> ⚠️ **JS 함정**: 어순이 `?:`와 다릅니다. "값을 먼저, 조건을 가운데" 순으로 읽습니다. 조건이 앞에 온다고 착각해 `if score >= 60 "pass" ...`처럼 쓰면 문법 오류입니다.

## 5.8 while

JS와 거의 동일합니다. 괄호가 없고 콜론+들여쓰기라는 점만 다릅니다. `break`/`continue`도 그대로입니다.

```python
n = 0
while n < 3:
    print(n)
    n += 1        # Python엔 n++ 없음, += 사용
# 출력: 0
```

> ⚠️ **JS 함정**: `n++`, `++n` 증감 연산자가 없습니다. `n += 1`을 씁니다.

## 연습문제

**Q1.** 리스트를 (번호, 값) 형태로 1번부터 출력하도록 채우세요.

```python no-run
items = ["a", "b", "c"]
for idx, val in ____(items, start=1):
    print(idx, val)
```

<details><summary>정답</summary>

```python
items = ["a", "b", "c"]
for idx, val in enumerate(items, start=1):
    print(idx, val)
# 출력: 1 a
```

`enumerate`의 `start`로 시작 번호를 바꿉니다.
</details>

**Q2.** 점수가 90 이상이면 "A", 아니면 "B"를 삼항 표현식으로 배정하세요.

```python no-run
score = 95
grade = "A" ____ score >= 90 ____ "B"
```

<details><summary>정답</summary>

```python
score = 95
grade = "A" if score >= 90 else "B"
print(grade)
# 출력: A
```

Python 삼항은 `값 if 조건 else 값` 어순입니다.
</details>

**Q3.** 두 리스트를 짝지어 dict로 만드세요.

```python no-run
keys = ["x", "y"]
vals = [1, 2]
d = dict(____(keys, vals))   # {"x": 1, "y": 2}
```

<details><summary>정답</summary>

```python
keys = ["x", "y"]
vals = [1, 2]
d = dict(zip(keys, vals))
print(d)
# 출력: {'x': 1, 'y': 2}
```

`zip`이 만든 (키, 값) 쌍들을 `dict`가 딕셔너리로 조립합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `if (...) { }` | `if ...:` + 들여쓰기 | 중괄호·세미콜론 없음 |
| `else if` | `elif` | |
| 블록 스코프(`let`) | (없음) | 블록이 스코프 아님 |
| `for (const x of arr)` | `for x in arr:` | 값 순회 |
| `for(let i=0; ...)` | `for i in range(n):` | stop 미포함 |
| `arr.forEach((v,i)=>)` | `enumerate(arr)` | (인덱스, 값) |
| (없음) | `zip(a, b)` | 여러 시퀀스 병렬 |
| `cond ? a : b` | `a if cond else b` | 어순 뒤집힘 |
| `n++` | `n += 1` | 증감 연산자 없음 |
