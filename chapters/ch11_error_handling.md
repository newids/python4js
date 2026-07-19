# Chapter 11. 에러 처리

> **학습 목표**
> - `try/except/else/finally` 구조를 JS `try/catch/finally`와 대응해 이해한다
> - `except`에 예외 타입을 명시해 필요한 예외만 잡는다
> - `raise`로 예외를 직접 발생시키고 예외 계층 구조를 활용한다
> - `else` 절의 용도를 이해해 "성공했을 때만" 실행할 코드를 분리한다

## 11.1 try/except — catch가 except다

JS의 `try/catch`는 Python에서 `try/except`가 됩니다. 키워드 이름만 다르고 흐름은 같습니다. 다만 Python은 **잡을 예외 타입을 except 절에 명시**하는 것을 권장합니다.

| JavaScript | Python |
|---|---|
| ```try { risky(); }```<br>```catch (e) { handle(e); }``` | ```try:```<br>```    risky()```<br>```except Exception as e:```<br>```    handle(e)``` |

아래는 리스트 인덱스 초과를 잡는 예입니다. `except IndexError`처럼 타입을 지정하면, 그 종류의 예외만 잡고 나머지는 그대로 위로 전파됩니다.

```python
nums = [10, 20, 30]

try:
    print(nums[5])
except IndexError as e:
    print(f"인덱스 에러: {e}")
# 출력: 인덱스 에러: list index out of range
```

여러 예외를 각각 다르게 처리하려면 `except` 절을 여러 개 둡니다. 위에서 아래로 처음 매칭되는 절이 실행됩니다.

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "0으로 나눌 수 없습니다"
    except TypeError:
        return "숫자만 가능합니다"

print(safe_divide(10, 0))
# 출력: 0으로 나눌 수 없습니다
print(safe_divide(10, "x"))
# 출력: 숫자만 가능합니다
```

> ⚠️ **JS 함정**: JS의 `catch (e)`는 모든 에러를 무차별로 잡습니다. Python에서 `except:`를 타입 없이 쓰면 `KeyboardInterrupt`까지 삼켜 버려 프로그램을 멈출 수 없게 만듭니다. 반드시 `except SomeError:`처럼 타입을 명시하고, 정말 넓게 잡아야 하면 `except Exception:`을 쓰세요.

## 11.2 else와 finally

`finally`는 JS와 동일하게 예외 발생 여부와 무관하게 항상 실행됩니다. Python에는 여기에 더해 JS에 없는 **`else` 절**이 있습니다. `else`는 `try` 블록이 **예외 없이 성공했을 때만** 실행됩니다.

```python
def read_value(data, key):
    try:
        value = data[key]
    except KeyError:
        print("키 없음")
        return None
    else:
        print("조회 성공")   # 예외가 없을 때만
        return value
    finally:
        print("조회 시도 종료")   # 항상

read_value({"a": 1}, "a")
# 출력: 조회 성공
```

`else`의 의미는 "try에서 감쌀 코드는 최소로 두고, 성공 후 이어질 로직은 else로 분리하라"입니다. 이렇게 하면 어느 줄이 예외를 낼 수 있는지가 명확해집니다.

## 11.3 raise — 예외 직접 발생

JS의 `throw`는 Python의 `raise`입니다. JS는 아무 값이나 던질 수 있지만, Python은 예외 클래스의 인스턴스를 발생시키는 것이 원칙입니다.

| JavaScript | Python |
|---|---|
| ```throw new Error("bad");``` | ```raise ValueError("bad")``` |

입력 검증에서 잘못된 값이 들어오면 적절한 예외를 발생시킵니다. `ValueError`는 "값은 맞는 타입이나 부적절할 때" 쓰는 표준 예외입니다.

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"나이는 음수일 수 없습니다: {age}")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)
# 출력: 나이는 음수일 수 없습니다: -5
```

## 11.4 예외 계층 — 상속으로 묶인다

Python 예외는 클래스 계층을 이룹니다. `ValueError`, `TypeError`, `IndexError` 등은 모두 `Exception`을 상속합니다. 따라서 `except Exception`은 이들 대부분을 한꺼번에 잡습니다. 9장의 상속 지식이 여기서 실용적으로 쓰입니다.

```python
errors = [ValueError("v"), IndexError("i"), KeyError("k")]
for e in errors:
    print(isinstance(e, Exception))
# 출력: True
```

계층을 이해하면 잡는 범위를 조절할 수 있습니다. 구체적인 타입(`ZeroDivisionError`)을 먼저 잡고, 넓은 타입(`Exception`)을 나중에 두는 것이 순서 원칙입니다 — 넓은 타입을 먼저 두면 구체 타입 절이 영원히 실행되지 않습니다.

```python
def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return -1

print(parse_int("42"))
# 출력: 42
print(parse_int("hello"))
# 출력: -1
```

> 🎯 **AICE**: 실기에서 예외 처리 자체를 크게 묻지는 않지만, 데이터 로딩·타입 변환 중 `ValueError`, `KeyError`가 자주 등장합니다. 어떤 예외가 왜 났는지 traceback 마지막 줄을 읽고 원인을 짚는 능력이 문제 해결 속도를 좌우합니다.

## 연습문제

**Q1.** 0으로 나누는 경우를 처리하도록 빈칸을 채우세요.

```python no-run
try:
    result = 10 / 0
____ ZeroDivisionError:
    result = None

print(result)   # None
```

<details><summary>정답</summary>

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    result = None

print(result)
# 출력: None
```

`except 예외타입:` 절로 특정 예외를 잡습니다.
</details>

**Q2.** 잘못된 입력에 예외를 발생시키도록 빈칸을 채우세요.

```python no-run
def sqrt_positive(x):
    if x < 0:
        ____ ValueError("음수 불가")
    return x ** 0.5

print(sqrt_positive(16))   # 4.0
```

<details><summary>정답</summary>

```python
def sqrt_positive(x):
    if x < 0:
        raise ValueError("음수 불가")
    return x ** 0.5

print(sqrt_positive(16))
# 출력: 4.0
```

`raise 예외(메시지)`로 예외를 직접 발생시킵니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `try { } catch (e) { }` | `try: ... except E as e:` | 타입 명시 권장 |
| `catch (e)` (전부 잡음) | `except Exception:` | 무타입 except 지양 |
| (없음) | `else:` 절 | 예외 없을 때만 실행 |
| `finally { }` | `finally:` | 항상 실행 |
| `throw new Error()` | `raise ValueError()` | 예외 인스턴스 발생 |
| Error 상속 | Exception 계층 | isinstance로 확인 |
