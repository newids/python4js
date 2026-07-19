# Chapter 15. Pandas II: 전처리

> **학습 목표**
> - 결측치를 탐지하고 fillna/dropna로 처리할 수 있다
> - 타입 변환과 파생 변수 생성으로 데이터를 가공할 수 있다
> - groupby 집계와 merge 결합으로 데이터를 재구성할 수 있다
> - 범주형 인코딩(get_dummies/LabelEncoder)과 스케일링으로 모델 입력을 완성할 수 있다

전처리는 AICE Associate 실기에서 **가장 배점이 큰 영역**입니다. "결측치를 채우고, 범주형을 숫자로 바꾸고, 스케일을 맞춰 모델에 넣을 수 있는 형태로 만드는" 과정 전체가 이 챕터입니다. JS에는 대응 개념이 거의 없으니, 각 함수의 시그니처를 손으로 쓸 수 있을 때까지 익히는 것이 목표입니다.

## 15.1 결측치 처리 — isnull / fillna / dropna

실제 데이터에는 빈 값(`NaN`)이 흔합니다. JS의 `null`/`undefined`에 해당하지만, pandas는 이를 **열 단위로 한 번에** 탐지·처리합니다. 먼저 어디에 얼마나 있는지 셉니다.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Kim", "Lee", "Park", "Choi"],
    "age": [25, np.nan, 35, 28],
    "score": [88, 72, np.nan, 63],
})
print(df.isnull().sum().sum())   # 전체 결측 개수
# 출력: 2
print(df["age"].isnull().sum())  # age 열 결측 개수
# 출력: 1
```

`fillna`는 결측을 특정 값으로 채우고, `dropna`는 결측이 있는 행을 버립니다. **pandas 3.0에서는 `inplace=True` 대신 결과를 다시 대입**하는 방식이 권장됩니다.

```python
df["age"] = df["age"].fillna(df["age"].mean())   # 평균으로 대치
print(df["age"].isnull().sum())
# 출력: 0

dropped = df.dropna()               # 결측 있는 행 제거
print(dropped.shape)                # score의 결측 행 하나 제거
# 출력: (3, 3)
```

> ⚠️ **함정**: `NaN`은 자기 자신과도 같지 않습니다(JS와 동일). 따라서 `df["age"] == np.nan`으로는 절대 결측을 찾지 못하고 전부 False가 나옵니다. 결측 탐지는 반드시 `isnull()`(또는 `isna()`)을 쓰세요.

## 15.2 타입 변환과 파생 변수

숫자가 문자열로 들어오거나, 기존 열을 조합해 새 열을 만들어야 할 때가 많습니다. 타입은 `astype`, 파생 변수는 **벡터 연산으로 열을 통째 계산**해 새 열에 대입합니다(13장 벡터화의 실전).

```python
df = pd.DataFrame({
    "height": [170, 165, 180],
    "weight": [70, 55, 82],
    "grade": ["1", "2", "3"],       # 숫자인데 문자열
})
df["grade"] = df["grade"].astype("int64")   # 문자열 → 정수
print(df["grade"].dtype)
# 출력: int64

df["bmi"] = df["weight"] / (df["height"] / 100) ** 2   # 파생 변수
print(df["bmi"].round(1).tolist())
# 출력: [24.2, 20.2, 25.3]
```

조건에 따라 범주를 만드는 파생도 자주 씁니다. `np.where`가 JS의 삼항 연산을 벡터화한 것입니다.

```python
df["obese"] = np.where(df["bmi"] >= 25, "yes", "no")
print(df["obese"].tolist())
# 출력: ['no', 'no', 'yes']
```

## 15.3 groupby — 범주별 집계

SQL의 `GROUP BY`와 같습니다. "도시별 평균 점수"처럼 **범주별로 나눠 집계**합니다. JS라면 `reduce`로 직접 누적해야 할 로직을 한 줄로 표현합니다.

**JavaScript**

```javascript
const byCity = {};
for (const r of rows) (byCity[r.city] ??= []).push(r.score);
// 이후 각 배열의 평균을 다시 계산...
```

**Python (pandas)**

```python
df = pd.DataFrame({
    "city": ["Seoul", "Busan", "Seoul", "Busan", "Seoul"],
    "score": [80, 70, 90, 60, 100],
})
by_city = df.groupby("city")["score"].mean()
print(by_city["Seoul"])
# 출력: 90.0
print(by_city["Busan"])
# 출력: 65.0
```

여러 집계를 한 번에 하려면 `agg`를 씁니다.

```python
stats = df.groupby("city")["score"].agg(["mean", "count"])
print(stats.loc["Seoul", "count"])
# 출력: 3
```

## 15.4 merge — 두 표 결합하기

SQL `JOIN`에 해당합니다. 공통 키를 기준으로 두 DataFrame을 옆으로 붙입니다. `on`에 기준 열, `how`에 결합 방식(`inner`/`left`/`right`/`outer`)을 줍니다.

```python
users = pd.DataFrame({"id": [1, 2, 3], "name": ["Kim", "Lee", "Park"]})
orders = pd.DataFrame({"id": [1, 1, 2], "amount": [100, 200, 150]})

merged = pd.merge(users, orders, on="id", how="inner")
print(merged.shape)          # id=3은 주문 없어 제외
# 출력: (3, 3)
print(merged["amount"].sum())
# 출력: 450
```

> ⚠️ **함정**: `how`의 기본값은 `"inner"`라, 한쪽에만 있는 키는 **조용히 사라집니다**. 위 예에서 `id=3`인 Park은 주문이 없어 결과에서 빠집니다. 모든 행을 유지하려면 `how="left"`를 명시하세요. JS에서 수동 조인하던 감각으로 접근하면 누락을 놓치기 쉽습니다.

## 15.5 범주형 인코딩 — get_dummies / LabelEncoder

모델은 문자열을 못 먹습니다. 범주형을 숫자로 바꿔야 합니다. 두 방식이 있습니다. **`get_dummies`는 원-핫 인코딩**(범주마다 0/1 열 생성), **`LabelEncoder`는 각 범주에 정수를 부여**합니다.

```python
df = pd.DataFrame({"city": ["Seoul", "Busan", "Seoul", "Daegu"]})
dummies = pd.get_dummies(df["city"])     # 원-핫: 범주 수만큼 열
print(dummies.shape)
# 출력: (4, 3)
print(dummies.columns.tolist())
# 출력: ['Busan', 'Daegu', 'Seoul']
```

`LabelEncoder`는 sklearn에서 가져오며, 순서가 있는 범주나 목표 변수(y)에 주로 씁니다.

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
encoded = le.fit_transform(df["city"])   # 알파벳순 정수 부여
print(encoded.tolist())
# 출력: [2, 0, 2, 1]
print(le.classes_.tolist())
# 출력: ['Busan', 'Daegu', 'Seoul']
```

> 🎯 **AICE**: 입력 특성(X)의 범주형은 대개 `get_dummies`(원-핫), 목표 변수(y)의 범주 라벨은 `LabelEncoder`를 쓰는 것이 실기의 관례입니다. `pd.get_dummies(df, columns=["열이름"])`처럼 DataFrame 통째로 특정 열만 인코딩하는 형태가 빈칸으로 자주 나옵니다.

## 15.6 스케일링 — StandardScaler / MinMaxScaler

특성마다 단위와 범위가 다르면(나이 0~100, 소득 0~1억) 모델이 큰 값에 휘둘립니다. 스케일링으로 범위를 맞춥니다. 두 스케일러의 **인터페이스가 동일**(`fit_transform`)하므로 하나로 묶어 봅니다. `StandardScaler`는 평균 0·표준편차 1로, `MinMaxScaler`는 0~1 범위로 변환합니다.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

X = pd.DataFrame({
    "age": [20, 40, 60, 80],
    "income": [2000, 4000, 6000, 8000],
})

std_scaled = StandardScaler().fit_transform(X)
print(std_scaled.mean(axis=0).round(1).tolist())   # 각 열 평균 0
# 출력: [0.0, 0.0]

minmax_scaled = MinMaxScaler().fit_transform(X)
print(minmax_scaled.min(axis=0).tolist())          # 각 열 최솟값 0
# 출력: [0.0, 0.0]
print(minmax_scaled.max(axis=0).tolist())          # 각 열 최댓값 1
# 출력: [1.0, 1.0]
```

> ⚠️ **함정**: 스케일러는 학습 데이터에만 `fit`하고, 검증·테스트 데이터에는 `transform`만 해야 합니다. 전체 데이터에 `fit_transform`을 먼저 하면 테스트 정보가 새어 들어가는 **데이터 누수**가 생깁니다(21장에서 Pipeline으로 자동 방지). 실기에서는 분리(17장) 후 스케일링하는 순서를 지키세요.

## 연습문제

**Q1.** `age` 열의 결측치를 중앙값(median)으로 채우려 합니다. 빈칸을 채우세요.

```python no-run
import pandas as pd, numpy as np
df = pd.DataFrame({"age": [20, np.nan, 40, np.nan, 30]})
df["age"] = df["age"].____(df["age"].median())
print(df["age"].isnull().sum())   # 0
```

<details><summary>정답</summary>

```python
import pandas as pd, numpy as np
df = pd.DataFrame({"age": [20, np.nan, 40, np.nan, 30]})
df["age"] = df["age"].fillna(df["age"].median())
print(df["age"].isnull().sum())
# 출력: 0
```

`fillna`에 채울 값을 넘깁니다. 결과를 열에 다시 대입해야 반영됩니다.
</details>

**Q2.** `city` 열을 원-핫 인코딩하려 합니다. 빈칸을 채우세요.

```python no-run
df = pd.DataFrame({"city": ["A", "B", "A", "C"]})
onehot = pd.____(df["city"])
print(onehot.shape)   # (4, 3)
```

<details><summary>정답</summary>

```python
df = pd.DataFrame({"city": ["A", "B", "A", "C"]})
onehot = pd.get_dummies(df["city"])
print(onehot.shape)
# 출력: (4, 3)
```

`pd.get_dummies`가 범주마다 0/1 열을 만듭니다. 범주가 3종이라 열이 3개입니다.
</details>

**Q3.** 특성 `X`를 평균 0·표준편차 1로 표준화하려 합니다. 빈칸을 채우세요.

```python no-run
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.____(X)
```

<details><summary>정답</summary>

```python
from sklearn.preprocessing import StandardScaler
import pandas as pd
X = pd.DataFrame({"v": [1.0, 2.0, 3.0]})
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(round(float(X_scaled.mean()), 1))
# 출력: 0.0
```

`fit_transform`이 통계량 학습과 변환을 한 번에 수행합니다(학습 데이터에만 사용).
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python (pandas/sklearn) | 비고 |
|----|--------|------|
| `x == null` 체크 | `df.isnull()` | `== np.nan`은 항상 False |
| `x ?? 기본값` | `df["c"].fillna(값)` | 결측 대치 |
| `arr.filter(x => x != null)` | `df.dropna()` | 결측 행 제거 |
| `Number(x)` | `df["c"].astype("int64")` | 타입 변환 |
| `cond ? a : b` (열 전체) | `np.where(cond, a, b)` | 벡터화 삼항 |
| `reduce`로 그룹 집계 | `df.groupby("k")["v"].mean()` | SQL GROUP BY |
| 수동 조인 | `pd.merge(a, b, on="k")` | SQL JOIN |
| (대응 없음) | `get_dummies` / `LabelEncoder` | 범주형 인코딩 |
| (대응 없음) | `StandardScaler` / `MinMaxScaler` | 스케일링 |
