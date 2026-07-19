# Chapter 04. 컬렉션: list·dict·set·tuple

> **학습 목표**
> - list·dict·set·tuple 4대 컬렉션을 JS 자료구조에 매핑해 쓸 수 있다
> - `[start:stop:step]`과 `[::-1]` 슬라이싱을 자유롭게 다룰 수 있다(pandas 인덱싱 선수 지식)
> - `in` 멤버십 연산과 튜플의 불변성·언패킹을 이해한다

## 4.1 list — Array의 대응물

JS 배열과 거의 같습니다. 다만 메서드 이름이 다릅니다 — 특히 `push`가 아니라 `append`입니다.

| JavaScript | Python |
|---|---|
| `arr.push(4)` | `lst.append(4)` |
| `arr.pop()` | `lst.pop()` |
| `arr.length` | `len(lst)` |
| `arr.includes(3)` | `3 in lst` |

```python
nums = [1, 2, 3]
nums.append(4)        # push 아님!
nums.pop()            # 마지막 제거
print(len(nums), nums)
# 출력: 3 [1, 2, 3]
```

> ⚠️ **JS 함정**: `push`는 Python에 없습니다. `append`입니다 — JS 개발자 최다 오타. 길이도 `.length` 속성이 아니라 `len(lst)` 함수입니다.

## 4.2 슬라이싱 — `[start:stop:step]`

Python 컬렉션의 핵심 무기입니다. JS의 `slice`보다 훨씬 강력하며, pandas의 `iloc` 인덱싱이 이 문법을 그대로 씁니다. **철저히** 익혀둡니다.

| JavaScript | Python |
|---|---|
| `arr.slice(1, 4)` | `lst[1:4]` |
| `arr.slice(-2)` | `lst[-2:]` |
| `[...arr].reverse()` | `lst[::-1]` |

```python
xs = [0, 10, 20, 30, 40, 50]
print(xs[1:4])     # 인덱스 1,2,3 (stop 미포함)
print(xs[:3])      # 처음부터 3개
print(xs[3:])      # 3번부터 끝까지
print(xs[-2:])     # 마지막 2개
# 출력: [10, 20, 30]
```

`stop`은 포함되지 않습니다(JS `slice`와 동일). 세 번째 값 `step`은 건너뛰기 간격입니다.

```python
xs = [0, 10, 20, 30, 40, 50]
print(xs[::2])     # 2칸씩 (짝수 인덱스)
print(xs[1::2])    # 1부터 2칸씩 (홀수 인덱스)
print(xs[::-1])    # 역순 (step -1)
# 출력: [0, 20, 40]
```

> ⚠️ **JS 함정**: `lst[::-1]`이 리스트를 뒤집는 관용구입니다. JS의 `reverse()`는 원본을 in-place로 뒤집었지만, 슬라이싱은 **새 리스트**를 반환하고 원본은 그대로 둡니다. 복사(`lst[:]`)로도 자주 씁니다.

> 🎯 **AICE**: `df.iloc[0:5]`, `arr[:, 0]` 같은 pandas·NumPy 인덱싱이 이 슬라이싱 문법의 확장입니다(13장, 14장). 여기서 손에 익히지 않으면 Part 2에서 막힙니다.

## 4.3 dict — Object/Map의 대응물

JS 객체와 Map을 합친 역할입니다. 키로 임의 타입을 쓸 수 있어 Map에 가깝지만, 리터럴 문법은 객체와 닮았습니다.

| JavaScript | Python |
|---|---|
| `{ name: "ada" }` | `{"name": "ada"}` |
| `obj.name` / `obj["name"]` | `d["name"]` |
| `Object.keys(obj)` | `d.keys()` |
| `Object.entries(obj)` | `d.items()` |

```python
user = {"name": "ada", "age": 36}
print(user["name"])        # 대괄호 접근 (점 접근 없음)
user["email"] = "a@x.io"   # 추가
print(list(user.keys()))
# 출력: ada
```

> ⚠️ **JS 함정**: `user.name` 같은 점 접근은 안 됩니다. 언제나 `user["name"]` 대괄호입니다. 키 문자열도 반드시 따옴표로 감쌉니다(`{name: ...}` 아님).

없는 키를 대괄호로 접근하면 `KeyError`가 납니다. JS는 `undefined`를 줬지만 Python은 예외를 던지므로, 안전 접근엔 `get`을 씁니다.

```python
user = {"name": "ada"}
print(user.get("age"))          # 없으면 None (KeyError 아님)
print(user.get("age", 0))       # 기본값 지정
# 출력: None
```

## 4.4 set — Set의 대응물

중복 없는 모음. JS `Set`과 대응하지만 리터럴 `{}`과 집합 연산자를 지원합니다.

| JavaScript | Python |
|---|---|
| `new Set([1,1,2])` | `{1, 1, 2}` |
| `set.has(x)` | `x in s` |
| `set.add(x)` | `s.add(x)` |

```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)    # 교집합
print(a | b)    # 합집합
print(a - b)    # 차집합
# 출력: {2, 3}
```

> ⚠️ **JS 함정**: 빈 중괄호 `{}`는 set이 아니라 **빈 dict**입니다. 빈 set은 `set()`으로 만듭니다.

## 4.5 tuple — JS에 없는 불변 시퀀스

Python 고유 개념입니다. list와 같지만 **불변(immutable)**이라 생성 후 수정할 수 없습니다. 소괄호로 만들며, 함수의 다중 반환·언패킹에 광범위하게 쓰입니다.

```python
point = (3, 4)       # 불변 시퀀스
print(point[0])      # 인덱싱은 됨
# point[0] = 9       # TypeError — 수정 불가
x, y = point         # 언패킹 (JS 구조분해와 유사)
print(x, y)
# 출력: 3
```

JS의 배열 구조분해 `const [a, b] = arr`가 Python의 튜플 언패킹에 대응합니다. 두 값 교환도 임시 변수 없이 한 줄입니다.

```python
a, b = 1, 2
a, b = b, a          # 스왑 (JS: [a, b] = [b, a])
print(a, b)
# 출력: 2 1
```

> ⚠️ **JS 함정**: 함수가 여러 값을 반환하면 사실 **튜플 하나**를 반환하는 것입니다. `return x, y`는 `return (x, y)`와 같고, 받는 쪽에서 `a, b = f()`로 언패킹합니다.

## 4.6 `in` 멤버십 — 자료구조 공통

`includes`/`has`/`in`(객체 키)로 나뉘던 JS와 달리, Python은 모든 컬렉션에 `in` 하나로 통일됩니다.

```python
print(3 in [1, 2, 3])            # 리스트: 값 존재?
print("name" in {"name": "a"})   # dict: 키 존재?
print("y" in "python")           # 문자열: 부분 문자열?
# 출력: True
```

> ⚠️ **JS 함정**: dict에 `in`을 쓰면 **키**를 검사합니다(값이 아님). JS의 `key in obj`와 같고, 값 검사는 `v in d.values()`로 합니다.

## 연습문제

**Q1.** 리스트 `xs`를 역순으로 뒤집는 슬라이싱을 채우세요.

```python no-run
xs = [1, 2, 3, 4]
reversed_xs = xs[____]   # [4, 3, 2, 1]
```

<details><summary>정답</summary>

```python
xs = [1, 2, 3, 4]
reversed_xs = xs[::-1]
print(reversed_xs)
# 출력: [4, 3, 2, 1]
```

`step`을 `-1`로 주면 끝에서부터 훑어 역순 리스트를 새로 만듭니다.
</details>

**Q2.** dict에서 없을 수도 있는 키를 안전하게(예외 없이) 꺼내고, 없으면 0을 반환하세요.

```python no-run
counts = {"a": 3}
value = counts.____("b", 0)   # 0
```

<details><summary>정답</summary>

```python
counts = {"a": 3}
value = counts.get("b", 0)
print(value)
# 출력: 0
```

`get`은 키가 없으면 `KeyError` 대신 기본값(여기선 0)을 반환합니다.
</details>

**Q3.** 두 변수 값을 임시 변수 없이 교환하세요.

```python no-run
a, b = 10, 20
____ = b, a
print(a, b)   # 20 10
```

<details><summary>정답</summary>

```python
a, b = 10, 20
a, b = b, a
print(a, b)
# 출력: 20 10
```

우변이 튜플 `(b, a)`로 묶였다가 좌변으로 언패킹됩니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `arr.push(x)` | `lst.append(x)` | push 없음 |
| `arr.length` | `len(lst)` | 함수 호출 |
| `arr.slice(1,4)` | `lst[1:4]` | stop 미포함 |
| `[...arr].reverse()` | `lst[::-1]` | 새 리스트 반환 |
| `{name:"a"}` | `{"name":"a"}` | 키에 따옴표 |
| `obj["k"]`(없음→undefined) | `d["k"]`(없음→KeyError) | 안전 접근은 `d.get(k)` |
| `new Set([...])` | `{...}` / `set()` | 빈 set은 `set()` |
| (없음) | tuple `(x, y)` | 불변 시퀀스·언패킹 |
| `includes`/`has`/`in` | `in` | 컬렉션 공통 |
