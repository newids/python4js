# Chapter 03. 문자열과 포매팅

> **학습 목표**
> - f-string으로 값을 삽입하고 포맷 스펙(`:.2f` 등)으로 출력 형식을 제어할 수 있다
> - split/join/strip/replace 등 핵심 문자열 메서드를 JS 대응으로 쓸 수 있다
> - 문자열 슬라이싱의 기본 문법을 이해한다(4장에서 심화)

## 3.1 f-string — 템플릿 리터럴의 대응물

JS의 템플릿 리터럴 `` `${x}` ``에 정확히 대응하는 것이 f-string입니다. 문자열 앞에 `f`를 붙이고 `{}` 안에 표현식을 씁니다.

| JavaScript | Python |
|---|---|
| `` `Hi ${name}` `` | `f"Hi {name}"` |
| `` `${a + b}` `` | `f"{a + b}"` |

```python
name = "Ada"
age = 36
print(f"{name} is {age}")
print(f"next year: {age + 1}")   # 중괄호 안에 표현식도 가능
# 출력: Ada is 36
```

> ⚠️ **JS 함정**: 백틱이 아니라 따옴표를 씁니다. `f`를 빼먹으면 그냥 `"{name}"` 리터럴 문자열이 출력됩니다. JS에서 `${}`를 백틱 없는 문자열에 넣으면 치환 안 되던 것과 같은 실수입니다.

## 3.2 포맷 스펙 — 템플릿 리터럴보다 강력한 지점

f-string은 `{값:포맷}` 형태로 자릿수·정렬·천단위 구분을 선언적으로 지정합니다. JS라면 `toFixed`, `padStart`, `toLocaleString`을 조합해야 하던 일이 한 줄에 들어갑니다.

| JavaScript | Python |
|---|---|
| `x.toFixed(2)` | `f"{x:.2f}"` |
| `n.toLocaleString()` | `f"{n:,}"` |
| `s.padStart(5)` | `f"{s:>5}"` |

```python
pi = 3.14159
price = 1234567
print(f"{pi:.2f}")      # 소수점 2자리
print(f"{price:,}")     # 천단위 콤마
print(f"{price:,.1f}")  # 콤마 + 소수 1자리
# 출력: 3.14
```

`:.2f`는 반올림하여 소수 둘째 자리까지 고정 표기합니다. AICE에서 평가지표(R², RMSE 등)를 정해진 자릿수로 출력할 때 자주 씁니다.

> 🎯 **AICE**: 모델 성능을 `print(f"정확도: {acc:.2f}")`처럼 포맷해 제출하는 문항이 나옵니다. `:.2f`, `:.4f` 포맷 스펙을 손에 익혀두세요.

## 3.3 문자열 메서드 — split / join / strip / replace

이름과 시그니처만 다를 뿐 JS 메서드와 거의 대응합니다. 가장 큰 차이는 **`join`의 주어가 구분자 문자열**이라는 점입니다.

| JavaScript | Python |
|---|---|
| `"a,b".split(",")` | `"a,b".split(",")` |
| `arr.join("-")` | `"-".join(arr)` |
| `s.trim()` | `s.strip()` |
| `s.replaceAll("a","b")` | `s.replace("a","b")` |

```python
csv = "  ada, grace , alan  "
names = [n.strip() for n in csv.split(",")]   # 컴프리헨션은 6장
print(names)
joined = "-".join(names)
print(joined)
# 출력: ['ada', 'grace', 'alan']
```

> ⚠️ **JS 함정**: `arr.join("-")`가 아니라 `"-".join(arr)`입니다. 구분자가 메서드의 주인입니다. 어순을 뒤집으면 `AttributeError`가 납니다.

Python의 `replace`는 JS의 `replaceAll`처럼 **모든 일치**를 바꿉니다. 첫 번째만 바꾸려면 세 번째 인자로 횟수를 줍니다.

```python
s = "a-b-c-d"
print(s.replace("-", "/"))       # 전부 치환
print(s.replace("-", "/", 1))    # 1개만
# 출력: a/b/c/d
```

## 3.4 슬라이싱 맛보기

문자열은 문자의 시퀀스라, 인덱스와 슬라이스로 잘라낼 수 있습니다. JS의 `slice`와 비슷하지만 `[start:stop:step]` 대괄호 문법을 씁니다. 4장에서 리스트와 함께 깊이 다룹니다.

| JavaScript | Python |
|---|---|
| `s[0]` | `s[0]` |
| `s.slice(0, 3)` | `s[0:3]` |
| `s.slice(-2)` | `s[-2:]` |

```python
word = "python"
print(word[0])       # 첫 글자
print(word[0:3])     # 0,1,2번 문자
print(word[-1])      # 마지막 글자(음수 인덱스)
print(word[::-1])    # 뒤집기
# 출력: p
```

> ⚠️ **JS 함정**: 음수 인덱스 `word[-1]`이 마지막 글자입니다. JS는 `s[-1]`이 `undefined`였지만 Python은 뒤에서부터 셉니다. `s.at(-1)`에 대응한다고 보면 됩니다.

## 연습문제

**Q1.** 실수 `score`를 소수점 셋째 자리까지 출력하도록 포맷 스펙을 채우세요.

```python no-run
score = 0.87654
print(f"{score:____}")
```

<details><summary>정답</summary>

```python
score = 0.87654
print(f"{score:.3f}")
# 출력: 0.877
```

`.3f`는 반올림하여 소수 셋째 자리까지 고정 표기합니다.
</details>

**Q2.** 리스트 `parts`를 언더스코어로 이어 붙이세요.

```python no-run
parts = ["2024", "01", "15"]
result = "____".____(parts)   # "2024_01_15"
```

<details><summary>정답</summary>

```python
parts = ["2024", "01", "15"]
result = "_".join(parts)
print(result)
# 출력: 2024_01_15
```

구분자 문자열이 `join`의 주인입니다(`parts.join`이 아님).
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `` `${x}` `` | `f"{x}"` | 백틱 아닌 따옴표 + `f` 접두사 |
| `x.toFixed(2)` | `f"{x:.2f}"` | 포맷 스펙이 더 강력 |
| `n.toLocaleString()` | `f"{n:,}"` | 천단위 구분 |
| `arr.join("-")` | `"-".join(arr)` | 구분자가 주어 |
| `s.trim()` | `s.strip()` | 양끝 공백 제거 |
| `s.replaceAll(a,b)` | `s.replace(a,b)` | 기본이 전체 치환 |
| `s.at(-1)` | `s[-1]` | 음수 인덱스 지원 |
