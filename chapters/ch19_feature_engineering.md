# Chapter 19. 고급 전처리와 특성 공학

> **학습 목표**
> - 기존 컬럼에서 파생·상호작용 특성을 만들어 모델에 신호를 더할 수 있다.
> - 범주형 변수를 상황에 맞게(원-핫·빈도·순서) 인코딩할 수 있다.
> - 스케일링과 결측·이상치 처리를 데이터 누수 없이 `train`에만 fit하여 적용할 수 있다.
> - `SelectKBest`·모델 중요도로 특성을 선택하고, 불균형 데이터의 개념을 설명할 수 있다.

Part 2에서 `fillna`·`get_dummies`·`StandardScaler`로 "돌아가는" 전처리를 배웠습니다. Professional 트랙은 여기서 한 걸음 더 나아가 **모델 성능을 끌어올리는** 전처리를 요구합니다. 이 장의 코드는 numpy·pandas·scikit-learn만 사용하므로 전부 실행 가능합니다.

먼저 이 장 전체에서 쓸 합성 데이터를 만듭니다.

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "age": np.random.randint(20, 60, n),
    "income": np.random.randint(2000, 9000, n),
    "city": np.random.choice(["seoul", "busan", "daegu"], n),
    "signup_days": np.random.randint(1, 400, n),
})
print(df.shape)
# 출력: (200, 4)
```

## 19.1 특성 생성 — 파생과 상호작용

특성 공학의 출발점은 "도메인 지식으로 컬럼을 조합"하는 일입니다. JS에서 배열을 `.map()`으로 가공하듯, pandas에서는 **열 단위 벡터 연산**으로 새 컬럼을 만듭니다. 반복문은 필요 없습니다.

| JavaScript | Python |
|---|---|
| ```const r = rows.map(x => ({...x, ratio: x.income / x.age}));``` | ```df["ratio"] = df["income"] / df["age"]``` |

`income / age`처럼 두 특성을 곱하거나 나눈 값을 **상호작용 특성(interaction feature)**이라 합니다. 선형 모델은 특성 간 곱셈을 스스로 학습하지 못하므로, 사람이 미리 만들어주면 표현력이 올라갑니다.

```python
df["income_per_age"] = df["income"] / df["age"]      # 파생 비율
df["age_x_days"] = df["age"] * df["signup_days"]      # 상호작용
df["is_new"] = (df["signup_days"] < 30).astype(int)   # 불리언 → 0/1 플래그
print(df.shape[1])
# 출력: 7
```

> ⚠️ **JS 함정**: `(df["signup_days"] < 30)`은 원소별 불리언 Series입니다. JS의 `if (arr < 30)`처럼 배열 전체를 하나의 진릿값으로 착각하지 마세요. 여기에 `.astype(int)`를 붙여야 `True/False`가 `1/0` 정수 특성이 됩니다.

## 19.2 범주형 고급 인코딩

Part 2에서는 `get_dummies`(원-핫) 하나만 썼습니다. 실무·시험에서는 카디널리티(고윳값 개수)에 따라 인코딩을 골라야 합니다.

- **원-핫(One-Hot)**: 고윳값이 적을 때. 순서 없는 명목형에 안전합니다.
- **빈도(Frequency)**: 고윳값이 많을 때. 각 범주를 등장 비율로 치환해 컬럼 폭발을 막습니다.
- **순서(Ordinal)**: `저/중/고`처럼 순서가 있는 범주.

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
city_ohe = ohe.fit_transform(df[["city"]])   # 2차원 입력 df[["city"]]에 주의
print(city_ohe.shape)
# 출력: (200, 3)
```

빈도 인코딩은 pandas `value_counts` + `map`으로 한 줄입니다.

```python
freq = df["city"].value_counts(normalize=True)   # 각 city의 등장 비율
df["city_freq"] = df["city"].map(freq)
print(df["city_freq"].nunique())
# 출력: 3
```

> ⚠️ **함정**: `OneHotEncoder`는 입력으로 **2차원**을 요구합니다. `df["city"]`(1차원 Series)를 넣으면 에러가 납니다. 대괄호를 두 번 감싼 `df[["city"]]`(DataFrame)을 넘기세요 — JS의 `[x]` 배열 감싸기와 발상은 같지만 축(axis) 개념이 다릅니다.

## 19.3 스케일링 심화 — 누수 없이 fit하기

스케일러 종류는 데이터 분포로 고릅니다. `StandardScaler`(평균 0·표준편차 1)는 정규분포에 가까울 때, `RobustScaler`(중앙값·IQR 기준)는 이상치가 많을 때 유리합니다. 핵심은 종류가 아니라 **fit 시점**입니다.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

num_cols = ["age", "income", "signup_days"]
X_train, X_test = train_test_split(df[num_cols], test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # 통계는 train에서만 학습
X_test_s = scaler.transform(X_test)         # test는 transform만 (재학습 금지)
print(abs(X_train_s.mean()) < 1e-9)
# 출력: True
```

> ⚠️ **함정**: `fit_transform`을 전체 데이터에 한 번 돌린 뒤 나누면, test의 평균·분산 정보가 train 전처리에 새어 들어갑니다. 이것이 **데이터 누수(data leakage)**입니다. 반드시 `train`에 `fit_transform`, `test`에 `transform`만 하세요. 21장의 `Pipeline`이 이 순서를 강제해 줍니다.

> 🎯 **AICE**: Professional 실기는 "train에 `fit_transform`, test에 `transform`" 빈칸을 자주 냅니다. 두 메서드를 손으로 구분해 쓸 수 있어야 합니다.

## 19.4 결측·이상치 전략

Part 2의 `fillna`는 값을 직접 지정했습니다. `SimpleImputer`는 통계값(평균·중앙값·최빈값)을 **학습**해 채우므로, 스케일러처럼 누수 없이 train/test에 적용됩니다.

```python
from sklearn.impute import SimpleImputer

df2 = df.copy()
df2.loc[:9, "income"] = np.nan          # 앞 10행을 결측으로 만들기
imp = SimpleImputer(strategy="median")
df2["income"] = imp.fit_transform(df2[["income"]])
print(df2["income"].isnull().sum())
# 출력: 0
```

이상치는 **IQR 규칙**(Q1−1.5·IQR ~ Q3+1.5·IQR 밖)으로 탐지합니다. 박스플롯 수염과 동일한 기준입니다.

```python
q1, q3 = df["income"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
mask = df["income"].between(lower, upper)   # 정상 범위 = True
print("outliers:", int((~mask).sum()))
# 출력: outliers:
```

## 19.5 특성 선택

특성이 많다고 좋은 게 아닙니다. 노이즈 특성은 과적합을 부릅니다. `SelectKBest`는 타깃과의 통계적 관련성(예: `f_classif`) 상위 k개를 고릅니다.

```python
from sklearn.feature_selection import SelectKBest, f_classif

y = (df["income"] > df["income"].median()).astype(int)   # 이진 타깃
num_feats = df[["age", "income", "signup_days", "income_per_age"]]
selector = SelectKBest(score_func=f_classif, k=2)
selector.fit(num_feats, y)
chosen = num_feats.columns[selector.get_support()].tolist()
print(len(chosen))
# 출력: 2
```

모델 기반 선택도 흔합니다. 트리 모델의 `feature_importances_`(20장에서 상술)로 중요도를 매겨 하위 특성을 버립니다.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=30, random_state=42)
rf.fit(num_feats, y)
importances = pd.Series(rf.feature_importances_, index=num_feats.columns)
print(round(importances.sum(), 4))   # 중요도 합은 항상 1
# 출력: 1.0
```

> 🎯 **AICE**: `feature_importances_`는 Professional에서 "어떤 특성이 예측에 기여했는가"를 묻는 문항으로 등장합니다. `pd.Series(model.feature_importances_, index=X.columns).sort_values()` 관용구를 익혀두세요.

## 19.6 불균형 데이터 개요

분류에서 한 클래스가 90%를 차지하면(예: 정상 180 : 이상 20), 모델이 전부 "정상"이라 찍어도 정확도 90%가 나옵니다. 이것이 **불균형(imbalanced) 데이터** 문제입니다.

```python
y_imb = np.array([0] * 180 + [1] * 20)
print(round((y_imb == 1).mean(), 2))   # 소수 클래스 비율
# 출력: 0.1
```

대응은 크게 세 갈래입니다: (1) 소수 클래스 복제·합성(오버샘플링, SMOTE 등), (2) 다수 클래스 축소(언더샘플링), (3) 손실 함수에서 소수 클래스에 가중치를 주는 `class_weight="balanced"`. sklearn 내장 방식인 (3)이 가장 간단합니다.

```python
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(class_weight="balanced", max_iter=1000)
print(clf.get_params()["class_weight"])
# 출력: balanced
```

불균형 데이터에서는 정확도(accuracy) 대신 **f1·recall**로 평가해야 합니다(22장 참조).

> 🎯 **AICE (출제 이력 불확실)**: 불균형 데이터 처리(SMOTE·`class_weight`)는 AICE Professional 공개 범위에 명시되어 있지 않아 **회차별 출제 편차가 있을 수 있습니다**. `imblearn`의 SMOTE는 별도 설치가 필요하므로, 시험 환경에서 우선순위는 sklearn 내장 `class_weight`와 평가지표(f1) 쪽에 두는 편이 안전합니다.

## 연습문제

**Q1.** train에만 통계를 학습시키고 test에는 적용만 하도록 빈칸을 채우세요.

```python no-run
scaler = StandardScaler()
X_train_s = scaler.____(X_train)   # 학습 + 변환
X_test_s = scaler.____(X_test)     # 변환만
```

<details><summary>정답</summary>

```python no-run
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
```

`fit_transform`은 train에, `transform`은 test에. 반대로 하거나 test에 `fit`하면 데이터 누수가 발생합니다.
</details>

**Q2.** 타깃과의 관련성 상위 3개 특성을 선택하도록 빈칸을 채우세요.

```python no-run
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(score_func=f_classif, k=____)
selector.fit(X, y)
cols = X.columns[selector.____()]
```

<details><summary>정답</summary>

```python no-run
selector = SelectKBest(score_func=f_classif, k=3)
selector.fit(X, y)
cols = X.columns[selector.get_support()]
```

`k`는 선택할 특성 수, `get_support()`는 선택 여부 불리언 마스크를 반환합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `rows.map(x => x.a / x.b)` | `df["a"] / df["b"]` | 파생 특성은 열 벡터 연산 |
| `arr < 30` (전체 비교 불가) | `(df["c"] < 30).astype(int)` | 원소별 불리언 → 0/1 플래그 |
| `[x]`로 배열 감싸기 | `df[["col"]]` | 인코더는 2차원 입력 요구 |
| 수동 정규화 함수 | `StandardScaler().fit_transform` | train fit / test transform 분리 |
| — | `SimpleImputer`, `SelectKBest` | JS 대응 없음, sklearn 고유 |
