# Chapter 14. Pandas I: Series와 DataFrame

> **학습 목표**
> - Series와 DataFrame의 관계를 JS의 배열/객체 모델에 대응시켜 이해할 수 있다
> - read_csv로 데이터를 로드하고 head/info/describe로 구조를 파악할 수 있다(EDA 1단계)
> - loc/iloc로 라벨·정수 위치 기반 행·열 선택을 구분해 수행할 수 있다
> - 불리언 인덱싱으로 조건에 맞는 행을 필터링할 수 있다

pandas는 AICE Associate 실기의 무대입니다. 시험은 "데이터를 읽고(EDA) → 다듬고(전처리) → 나누고 → 모델에 넣는" 흐름이며, 이 챕터는 그 첫 단계인 **로드와 구조 확인**을 다룹니다. JS 개발자에게 DataFrame은 "각 열이 같은 길이인 객체들의 배열"이라고 생각하면 가장 가깝습니다.

## 14.1 Series와 DataFrame — 열과 표

**Series**는 인덱스가 붙은 1차원 배열(13장 ndarray + 라벨), **DataFrame**은 Series를 열로 묶은 2차원 표입니다. JS로 치면 Series는 "이름표 달린 배열", DataFrame은 "행 객체들의 배열"입니다.

| JavaScript | Python (pandas) |
|---|---|
| `const ages = [25, 30, 35];` | `ages = pd.Series([25, 30, 35])` |
| `[{name:'Kim', age:25}, ...]` | `pd.DataFrame({"name": [...], "age": [...]})` |

DataFrame은 보통 **열 단위 딕셔너리**로 만듭니다. JS의 "행 객체 배열"과 축이 반대라는 점에 주의하세요.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Kim", "Lee", "Park", "Choi"],
    "age": [25, 30, 35, 28],
    "city": ["Seoul", "Busan", "Seoul", "Daegu"],
})
print(df.shape)      # (행, 열)
# 출력: (4, 3)
print(df["age"].mean())
# 출력: 29.5
```

하나의 열을 꺼내면 Series입니다. Series는 13장의 벡터 연산을 그대로 지원합니다.

```python
print(type(df["age"]))
# 출력: <class 'pandas.Series'>
older = df["age"] + 1        # 열 전체에 벡터 연산
print(older.tolist())
# 출력: [26, 31, 36, 29]
```

> ⚠️ **JS 함정**: DataFrame은 "행 객체의 배열"이 아니라 "열의 딕셔너리"입니다. `df[0]`은 첫 번째 행이 아니라 이름이 `0`인 열을 찾으려다 에러가 납니다. 행을 위치로 꺼내려면 `df.iloc[0]`을 써야 합니다(14.3).

## 14.2 read_csv와 EDA 3종 세트 — head/info/describe

실기에서 데이터는 CSV로 주어집니다. `pd.read_csv("파일경로")`가 표준이지만, 여기서는 실행 가능하도록 문자열을 `io.StringIO`로 감싸 읽습니다. **실기에서는 파일 경로 문자열만 넣으면 됩니다.**

```python
import io

csv_text = """name,age,city,score
Kim,25,Seoul,88
Lee,30,Busan,72
Park,35,Seoul,95
Choi,28,Daegu,63
Yoon,42,Busan,80"""

df = pd.read_csv(io.StringIO(csv_text))
print(df.shape)
# 출력: (5, 4)
```

로드 직후 데이터의 첫인상을 보는 세 함수입니다. 순서대로 외워 두면 실기에서 그대로 씁니다.

```python
head3 = df.head(3)          # 앞 3행 (기본 5행)
print(head3.shape)
# 출력: (3, 4)
```

`info()`는 행 수·열별 결측 여부·dtype을 한눈에 보여줍니다(결측치 파악의 출발점). 출력의 첫 줄은 항상 클래스 이름입니다.

```python
df.info()
# 출력: <class 'pandas.DataFrame'>
```

`describe()`는 수치형 열의 요약 통계(개수·평균·표준편차·사분위수)를 냅니다.

```python
desc = df.describe()
print(desc.loc["mean", "age"])   # age 열 평균
# 출력: 32.0
print(desc.loc["max", "score"])  # score 최댓값
# 출력: 95.0
```

> 🎯 **AICE**: 실기 EDA 문항은 대개 `df.head()`, `df.info()`, `df.describe()`를 순서대로 요구합니다. 특히 `info()`로 결측치가 있는 열을 찾아 다음 전처리 단계로 넘어가는 흐름이 정형화되어 있으니, 이 세 함수는 손에 익혀 두세요.

## 14.3 loc와 iloc — 라벨이냐 위치냐

행·열을 선택하는 두 가지 방식입니다. **`loc`는 라벨(이름) 기반, `iloc`는 정수 위치 기반**입니다. JS 배열은 정수 인덱스만 있지만, pandas는 인덱스에 이름을 붙일 수 있어 둘을 구분합니다.

| JavaScript | Python (pandas) |
|---|---|
| `rows[0]` | `df.iloc[0]` (위치) |
| (대응 없음) | `df.loc[0, "age"]` (라벨) |

```python
df = pd.DataFrame({
    "name": ["Kim", "Lee", "Park"],
    "age": [25, 30, 35],
}, index=["a", "b", "c"])     # 문자열 인덱스

print(df.loc["b", "age"])     # 라벨로 접근
# 출력: 30
print(df.iloc[1, 1])          # 정수 위치로 접근
# 출력: 30
```

슬라이싱도 됩니다. 여러 열은 리스트로 넘깁니다. **`loc`의 범위 슬라이싱은 끝값을 포함**하는 점이 4장의 리스트 슬라이싱과 다릅니다.

```python
print(df.loc["a":"b", "name"].tolist())   # 끝 라벨 포함
# 출력: ['Kim', 'Lee']
print(df.iloc[0:2]["name"].tolist())       # 끝 위치 제외(리스트와 동일)
# 출력: ['Kim', 'Lee']
sub = df[["name", "age"]]                    # 여러 열 선택
print(sub.shape)
# 출력: (3, 2)
```

> ⚠️ **JS 함정**: `loc`의 슬라이싱 `df.loc["a":"c"]`는 **끝 라벨 `"c"`를 포함**합니다. JS의 `slice`나 Python 리스트 슬라이싱이 끝을 제외하는 것과 반대이므로, 정수 인덱스에 `loc`을 쓸 때 특히 조심하세요. 위치 기반 `iloc`은 끝을 제외합니다.

## 14.4 불리언 인덱싱 — pandas의 핵심 전환점

이 챕터에서 가장 중요한 문법입니다. 13장의 NumPy 불리언 마스크가 그대로 DataFrame으로 올라옵니다. 조건식이 True/False Series를 만들고, `df[마스크]`가 True인 행만 남깁니다. 실기에서 "조건을 만족하는 데이터 추출"은 거의 매번 나옵니다.

**JavaScript**

```javascript
const adults = people.filter(p => p.age >= 30);
```

**Python (pandas)**

```python
df = pd.DataFrame({
    "name": ["Kim", "Lee", "Park", "Choi", "Yoon"],
    "age": [25, 30, 35, 28, 42],
    "city": ["Seoul", "Busan", "Seoul", "Daegu", "Busan"],
})

adults = df[df["age"] >= 30]        # 30세 이상 행만
print(adults["name"].tolist())
# 출력: ['Lee', 'Park', 'Yoon']
```

조건을 결합할 때는 NumPy와 똑같이 `&`/`|`를 쓰고 각 조건을 괄호로 감쌉니다.

```python
seoul_young = df[(df["city"] == "Seoul") & (df["age"] < 30)]
print(seoul_young["name"].tolist())
# 출력: ['Kim']

busan = df[df["city"].isin(["Busan"])]   # 여러 값 매칭은 isin
print(len(busan))
# 출력: 2
```

특정 열의 값 분포는 `value_counts()`로 셉니다(EDA에서 범주형 파악의 필수 도구).

```python
counts = df["city"].value_counts()
print(counts["Seoul"])
# 출력: 2
```

> ⚠️ **함정**: 여기서도 `and`/`or`가 아니라 `&`/`|`입니다. 그리고 각 조건은 **반드시 괄호**로 감싸세요. `df[df["city"] == "Seoul" & df["age"] < 30]`은 연산자 우선순위 때문에 에러가 납니다. `df[(...) & (...)]` 형태를 습관화하세요.

> 🎯 **AICE**: `df[df['컬럼'] 조건]` 패턴은 실기 빈칸 채우기의 단골입니다. "특정 조건의 행을 추출해 개수를 세라"거나 "조건에 맞는 행의 평균을 구하라"는 문항이 반복되므로, 마스크 → 대괄호 필터 → 집계로 이어지는 손동작을 몸에 익히세요.

## 연습문제

**Q1.** DataFrame `df`에서 `age` 열의 평균을 구하려 합니다. 빈칸을 채우세요.

```python no-run
import pandas as pd
df = pd.DataFrame({"age": [20, 30, 40], "score": [70, 80, 90]})
avg = df[____].mean()
print(avg)   # 30.0
```

<details><summary>정답</summary>

```python
import pandas as pd
df = pd.DataFrame({"age": [20, 30, 40], "score": [70, 80, 90]})
avg = df["age"].mean()
print(avg)
# 출력: 30.0
```

열 하나를 문자열 키로 꺼내면 Series가 되고, `.mean()`으로 평균을 구합니다.
</details>

**Q2.** `score`가 75 이상인 행만 골라내려 합니다. 빈칸을 채우세요.

```python no-run
df = pd.DataFrame({"name": ["A", "B", "C"], "score": [60, 80, 90]})
high = df[df[____] >= 75]
print(high["name"].tolist())   # ['B', 'C']
```

<details><summary>정답</summary>

```python
df = pd.DataFrame({"name": ["A", "B", "C"], "score": [60, 80, 90]})
high = df[df["score"] >= 75]
print(high["name"].tolist())
# 출력: ['B', 'C']
```

`df["score"] >= 75`가 불리언 Series를 만들고, `df[...]`가 True인 행만 남깁니다.
</details>

**Q3.** 2번째 행(정수 위치)을 통째로 꺼내려 합니다. 라벨이 아니라 위치 기반이어야 합니다. 빈칸을 채우세요.

```python no-run
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
row = df.____[1]
print(row["a"])   # 2
```

<details><summary>정답</summary>

```python
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
row = df.iloc[1]
print(row["a"])
# 출력: 2
```

정수 위치 기반 접근은 `iloc`입니다. 라벨 기반이라면 `loc`을 씁니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python (pandas) | 비고 |
|----|--------|------|
| `[{...}, {...}]` (행 객체 배열) | `pd.DataFrame({열: [...]})` | 열 딕셔너리로 생성 |
| `arr[i]` | `df.iloc[i]` | 정수 위치 접근 |
| (대응 없음) | `df.loc[라벨, 열]` | 라벨 기반 접근 |
| `arr.filter(p => p.x > 0)` | `df[df["x"] > 0]` | 불리언 인덱싱 |
| `arr.filter(p => A && B)` | `df[(A) & (B)]` | 괄호 필수, `&` 사용 |
| `arr.slice(0, 3)` | `df.head(3)` | 앞부분 미리보기 |
| `new Set(arr).size` 계열 | `df["col"].value_counts()` | 값 빈도 |
