# Chapter 02. 변수·타입·연산자

> **학습 목표**
> - Python의 동적 타이핑과 변수 할당(상수 관례 포함)을 JS 대응으로 설명할 수 있다
> - `==`와 `is`, 그리고 `is None` 관용구를 올바르게 구분해 쓸 수 있다
> - `/`와 `//`, 그리고 JS와 반대로 동작하는 truthiness 함정을 피할 수 있다

## 2.1 동적 타이핑과 변수 할당

JS의 `let x = 1`처럼 Python도 타입을 미리 선언하지 않습니다. 다만 `let`/`const` 키워드 없이 이름에 바로 할당합니다.

| JavaScript | Python |
|---|---|
| `let count = 3;` | `count = 3` |
| `const MAX = 100;` | `MAX = 100  # 관례상 대문자` |
| `typeof count` | `type(count)` |

Python에는 `const`가 없습니다. 상수는 **대문자 이름**이라는 관례로만 표현하며, 언어가 재할당을 막지는 않습니다.

```python
count = 3
count = "three"   # 다른 타입 재할당도 허용 (동적 타이핑)
print(type(count).__name__)
# 출력: str
```

> ⚠️ **JS 함정**: `const`가 없으므로 대문자 상수도 실수로 재할당됩니다. 불변을 강제하고 싶다면 튜플(4장)이나 언어 관례에 의존해야 합니다.

## 2.2 `==` vs `is` — 값 비교와 정체성 비교

JS의 `===`는 값과 타입을 함께 비교했습니다. Python의 `==`가 그 역할(값 비교)이고, `is`는 **같은 객체인지(정체성)**를 봅니다. 둘을 혼동하면 미묘한 버그가 납니다.

| JavaScript | Python |
|---|---|
| `a === b` | `a == b`  # 값 비교 |
| `a === b`(동일 참조) | `a is b`  # 정체성 비교 |

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # 값이 같은가?
print(a is b)   # 같은 객체인가?
# 출력: True
```

`a == b`는 `True`(내용이 같음)지만 `a is b`는 `False`(서로 다른 리스트 객체)입니다.

> ⚠️ **JS 함정**: 값을 비교하고 싶을 땐 언제나 `==`입니다. `is`를 값 비교에 쓰면 작은 정수·짧은 문자열에서는 우연히 맞다가, 다른 값에서 갑자기 틀립니다.

## 2.3 `is None` — `== null` 습관을 버리기

JS에서 `x == null`로 null/undefined를 한 번에 잡던 패턴은 Python에 없습니다. Python의 "값 없음"은 `None` 하나뿐이고, 이것과의 비교는 관용적으로 `is`를 씁니다.

| JavaScript | Python |
|---|---|
| `if (x == null)` | `if x is None:` |
| `if (x != null)` | `if x is not None:` |

```python
value = None
print(value is None)
print(value is not None)
# 출력: True
```

`None`은 프로그램 전체에 단 하나만 존재하는 싱글턴이라 정체성 비교(`is`)가 가장 정확하고 빠릅니다.

> 🎯 **AICE**: 결측치 처리(15장)에서 `df['col'].isnull()`을 쓰지만, 순수 파이썬 값의 존재 확인은 `is None`이 표준입니다. `== None`은 관례에 어긋나 감점 요소가 될 수 있습니다.

## 2.4 나눗셈: `/`와 `//`

JS의 `/`는 항상 실수 나눗셈이었습니다. Python의 `/`도 **항상 float**를 반환합니다(정수끼리 나눠도). 대신 정수 나눗셈용 `//` 연산자가 새로 있습니다.

| JavaScript | Python |
|---|---|
| `7 / 2  // 3.5` | `7 / 2   # 3.5` |
| `Math.floor(7 / 2)` | `7 // 2  # 3` |
| `7 % 2` | `7 % 2   # 1` |

```python
print(7 / 2)     # 항상 float
print(7 // 2)    # 정수 몫(내림)
print(7 % 2)     # 나머지
# 출력: 3.5
```

`//`는 몫을 내림(floor)합니다. 음수에서는 `-7 // 2 == -4`처럼 0쪽이 아니라 아래로 내려가니 주의합니다.

> ⚠️ **JS 함정**: `5 / 2`가 `2`가 아니라 `2.5`인 건 JS와 같지만, 정수 결과가 필요할 때 `Math.floor` 대신 `//`를 쓴다는 점이 새롭습니다. 인덱스 계산 등에서 자주 씁니다.

## 2.5 truthiness — JS와 반대로 동작하는 함정

가장 위험한 차이입니다. JS에서 빈 배열 `[]`과 빈 객체 `{}`는 **truthy**였습니다. Python에서 빈 컬렉션은 모두 **falsy**입니다.

| 값 | JavaScript | Python |
|---|---|---|
| `[]` / `{}` | truthy | **falsy** |
| `""` / `0` | falsy | falsy |
| `None` / `null` | falsy | falsy |

```python
items = []
if items:
    print("데이터 있음")
else:
    print("비어 있음")
# 출력: 비어 있음
```

JS 습관대로 `if (arr)`로 "배열이 존재하는가"를 검사하면, Python에서는 **빈 리스트일 때 분기가 반대로** 갑니다.

> ⚠️ **JS 함정**: `if items:`는 "items가 비어있지 않은가"를 뜻합니다. "변수가 존재/할당되었는가"를 확인하려면 `if items is not None:`을 써야 빈 리스트와 `None`을 구분할 수 있습니다.

```python
# 존재 여부와 비어있음을 구분해야 할 때
data = []
print("할당됨" if data is not None else "None임")   # 삼항 어순은 5장에서
# 출력: 할당됨
```

## 연습문제

**Q1.** 변수 `user`가 `None`인지 관용적으로 검사하는 조건을 채우세요.

```python no-run
user = None
if user ____ None:
    print("사용자 없음")
```

<details><summary>정답</summary>

```python
user = None
if user is None:
    print("사용자 없음")
# 출력: 사용자 없음
```

`None` 비교는 `==`가 아니라 `is`를 쓰는 것이 표준 관용구입니다.
</details>

**Q2.** 두 정수의 몫(정수)과 나머지를 각각 구하도록 연산자를 채우세요.

```python no-run
q = 17 ____ 5    # 몫: 3
r = 17 ____ 5    # 나머지: 2
print(q, r)
```

<details><summary>정답</summary>

```python
q = 17 // 5
r = 17 % 5
print(q, r)
# 출력: 3 2
```

`/`는 float(3.4)를 주므로 정수 몫에는 `//`를 씁니다.
</details>

**Q3.** 리스트가 비어 있으면 "empty"를 출력합니다. Python truthiness에 맞게 채우세요.

```python no-run
nums = []
if ____ nums:
    print("empty")
```

<details><summary>정답</summary>

```python
nums = []
if not nums:
    print("empty")
# 출력: empty
```

빈 리스트는 falsy이므로 `not nums`가 `True`입니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `let` / `const` | 그냥 할당 / 대문자 관례 | `const` 없음 — 재할당 막지 못함 |
| `===` (값+타입) | `==` | 값 비교 |
| 동일 참조 비교 | `is` | 정체성(같은 객체) 비교 |
| `x == null` | `x is None` | `None`은 싱글턴 |
| `Math.floor(a/b)` | `a // b` | 정수 나눗셈(내림) |
| `[]`/`{}` truthy | `[]`/`{}` **falsy** | 빈 컬렉션 분기 반대 |
