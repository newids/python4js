# Chapter 21. 하이퍼파라미터 튜닝과 Pipeline

> **학습 목표**
> - 하이퍼파라미터와 학습된 파라미터의 차이를 구분할 수 있다.
> - `GridSearchCV`·`RandomizedSearchCV`로 최적 조합을 탐색할 수 있다.
> - `Pipeline`으로 전처리와 모델을 하나의 객체로 묶을 수 있다.
> - `ColumnTransformer`로 열 종류별 전처리를 구성하고 데이터 누수를 원천 차단할 수 있다.

모델에는 두 종류의 값이 있습니다. `fit`이 **데이터로 학습하는** 파라미터(트리 분기 기준, 회귀 계수)와, 사람이 **학습 전에 정해주는** 하이퍼파라미터(`n_estimators`, `max_depth`, `learning_rate`)입니다. 이 장은 후자를 자동으로 탐색하고, 전처리와 모델을 누수 없이 묶는 법을 다룹니다. 모두 sklearn만 쓰므로 실행 가능합니다.

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

np.random.seed(42)
n = 200
df = pd.DataFrame({
    "age": np.random.randint(20, 60, n),
    "income": np.random.randint(2000, 9000, n),
    "city": np.random.choice(["seoul", "busan", "daegu"], n),
})
y = (df["income"] + df["age"] * 50 > 5000).astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.3, random_state=42)
print(X_train.shape)
# 출력: (140, 3)
```

## 21.1 GridSearchCV — 격자 전수 탐색

하이퍼파라미터 후보들을 딕셔너리로 주면, `GridSearchCV`가 **모든 조합 × 교차검증**을 돌려 최고 성능 조합을 찾습니다. JS로 치면 중첩 `for` 루프로 파라미터를 스윕하되, 각 조합을 교차검증으로 공정하게 채점하는 것입니다.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

param_grid = {"n_estimators": [10, 30], "max_depth": [2, 4]}   # 2×2 = 4조합
grid = GridSearchCV(RandomForestClassifier(random_state=42),
                    param_grid, cv=3)
grid.fit(X_train[["age", "income"]], y_train)
print(sorted(grid.best_params_.keys()))
# 출력: ['max_depth', 'n_estimators']
```

탐색이 끝나면 `best_params_`(최적 조합)·`best_score_`(교차검증 평균 점수)·`best_estimator_`(그 조합으로 재학습된 모델)를 꺼낼 수 있습니다.

```python
print(0.0 <= grid.best_score_ <= 1.0)
# 출력: True
```

> ⚠️ **함정**: 격자 크기는 곱셈으로 폭발합니다. 파라미터 3개에 각 5후보면 5³=125조합, `cv=5`면 총 625회 학습입니다. JS에서 중첩 루프 복잡도를 계산하듯, 후보를 넣기 전에 조합 수를 곱해보세요.

## 21.2 RandomizedSearchCV — 무작위 표본 탐색

격자가 너무 크면 전수 탐색 대신 `RandomizedSearchCV`로 `n_iter`개만 무작위 추출해 시험합니다. 넓은 공간을 적은 비용으로 훑을 때 효율적입니다.

```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {"n_estimators": [10, 20, 30, 50], "max_depth": [2, 3, 4, 5]}
rand = RandomizedSearchCV(RandomForestClassifier(random_state=42),
                          param_dist, n_iter=4, cv=3, random_state=42)
rand.fit(X_train[["age", "income"]], y_train)
print(rand.n_iter)
# 출력: 4
```

> 🎯 **AICE**: Professional 실기에서 `GridSearchCV(estimator, param_grid, cv=...)`의 인자 순서와 `best_params_`·`best_score_` 속성명을 빈칸으로 냅니다. `param_grid`는 **딕셔너리**, 값은 **리스트**라는 구조를 손으로 쓸 수 있어야 합니다.

## 21.3 Pipeline — 전처리와 모델을 한 객체로

`Pipeline`은 여러 변환 단계와 마지막 모델을 하나로 묶습니다. JS의 함수 합성(`compose`)이나 Express 미들웨어 체인처럼, `fit`을 호출하면 각 단계를 순서대로 통과시킵니다.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),                 # 1단계: 스케일링
    ("clf", LogisticRegression(max_iter=1000)),   # 2단계: 모델
])
pipe.fit(X_train[["age", "income"]], y_train)
print(round(pipe.score(X_test[["age", "income"]], y_test), 2) >= 0.0)
# 출력: True
```

Pipeline의 진짜 가치는 **누수 방지**입니다. 교차검증 시 각 폴드의 train에만 스케일러가 `fit`되고 검증 폴드에는 `transform`만 적용됩니다 — 19장에서 손으로 지키던 순서를 자동으로 강제합니다.

## 21.4 ColumnTransformer — 열 종류별 전처리

실제 데이터는 숫자·범주형이 섞여 있어 열마다 다른 전처리가 필요합니다. `ColumnTransformer`는 "이 열들엔 스케일러, 저 열들엔 인코더"를 한 번에 지정합니다. JS로 치면 필드별로 다른 변환기를 매핑하는 것입니다.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

pre = ColumnTransformer([
    ("num", StandardScaler(), ["age", "income"]),          # 숫자 열
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),  # 범주 열
])
full = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
full.fit(X_train, y_train)   # 원본 DataFrame을 그대로 투입
print(round(full.score(X_test, y_test), 2) >= 0.0)
# 출력: True
```

> ⚠️ **함정**: `ColumnTransformer`의 열 지정은 **리스트**(`["age", "income"]`)여야 합니다. 문자열 하나(`"age"`)를 넣으면 축 오류가 납니다. 또한 지정하지 않은 열은 기본적으로 **버려집니다**(`remainder="drop"`) — 유지하려면 `remainder="passthrough"`를 명시하세요.

## 21.5 튜닝 + Pipeline 결합 — 누수 없는 튜닝

`GridSearchCV`에 Pipeline을 통째로 넘기면, 전처리까지 포함해 교차검증이 돌아 누수가 원천 차단됩니다. Pipeline 단계 이름과 파라미터는 **`단계이름__파라미터`**(언더스코어 2개)로 지정합니다.

```python
grid2 = GridSearchCV(full, {"clf__C": [0.1, 1.0]}, cv=3)
grid2.fit(X_train, y_train)
print("clf__C" in grid2.best_params_)
# 출력: True
```

> 🎯 **AICE**: `clf__C`의 **더블 언더스코어**(`__`) 표기는 Professional에서 자주 헷갈리는 지점입니다. `단계이름 + __ + 파라미터명` 규칙을 기억하세요. 이 방식이 "전처리를 교차검증 안에서" 수행해 누수를 막는 정석입니다.

## 연습문제

**Q1.** `max_depth`를 3, 5, 7 중에서 3-폴드 교차검증으로 탐색하도록 빈칸을 채우세요.

```python no-run
from sklearn.model_selection import GridSearchCV
param_grid = {"max_depth": ____}
grid = GridSearchCV(model, param_grid, cv=____)
grid.fit(X_train, y_train)
best = grid.____
```

<details><summary>정답</summary>

```python no-run
param_grid = {"max_depth": [3, 5, 7]}
grid = GridSearchCV(model, param_grid, cv=3)
grid.fit(X_train, y_train)
best = grid.best_params_
```

값은 리스트, `cv`는 폴드 수, 결과는 `best_params_`에서 꺼냅니다.
</details>

**Q2.** 스케일러와 로지스틱 회귀를 순서대로 묶는 Pipeline을 만드세요.

```python no-run
from sklearn.pipeline import Pipeline
pipe = ____([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.____(X_train, y_train)
```

<details><summary>정답</summary>

```python no-run
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.fit(X_train, y_train)
```

`(이름, 변환기)` 튜플의 리스트를 넘기고, 전체를 하나의 estimator처럼 `fit`합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| 중첩 for 루프 파라미터 스윕 | `GridSearchCV(model, param_grid, cv=)` | 조합 × 교차검증 |
| 무작위 샘플링 탐색 | `RandomizedSearchCV(..., n_iter=)` | 넓은 공간 저비용 탐색 |
| 함수 합성 / 미들웨어 체인 | `Pipeline([(name, step), ...])` | 전처리+모델 단일 객체 |
| 필드별 변환 매핑 | `ColumnTransformer([(name, tf, cols)])` | 열 종류별 전처리 |
| `obj.step.param` | `"step__param"` (더블 언더스코어) | Pipeline 파라미터 지정 |
