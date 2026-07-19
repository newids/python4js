# Chapter 20. 앙상블 모델

> **학습 목표**
> - 배깅(bagging)과 부스팅(boosting)의 원리와 차이를 설명할 수 있다.
> - `RandomForestClassifier`·`GradientBoostingClassifier`를 학습·평가할 수 있다.
> - `feature_importances_`로 특성 중요도를 추출·해석할 수 있다.
> - XGBoost·LightGBM의 API 형태를 읽고 sklearn 계열과의 관계를 안다.

한 개의 결정 트리(17장)는 데이터에 과하게 맞아 흔들립니다. **앙상블(ensemble)**은 약한 예측기 여러 개를 결합해 안정적이고 강한 예측기를 만드는 기법입니다. 개념적으로는 "여러 개의 서로 다른 휴리스틱을 투표·가중합으로 합친다"는 발상으로, JS에서 여러 판정 함수의 결과를 종합하던 것과 닮았습니다. sklearn 계열(RandomForest·GradientBoosting)은 실행 가능하고, XGBoost·LightGBM은 이 환경에 미설치라 해당 코드만 `no-run`으로 표기합니다.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=300, n_features=8, n_informative=5,
                           random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
print(X_train.shape)
# 출력: (210, 8)
```

## 20.1 배깅 vs 부스팅 — 두 결합 전략

| 전략 | 학습 방식 | 목표 | 대표 모델 |
|------|----------|------|----------|
| **배깅(Bagging)** | 데이터를 부트스트랩 샘플링해 여러 트리를 **병렬·독립** 학습 후 투표 | 분산↓ (과적합 완화) | RandomForest |
| **부스팅(Boosting)** | 앞 모델의 오차를 다음 모델이 **순차적으로** 보정 | 편향↓ (정확도↑) | GradientBoosting, XGBoost, LightGBM |

배깅은 독립된 예측기들의 **다수결**입니다. 부스팅은 "직전 모델이 틀린 샘플에 집중"하는 반복 개선으로, JS에서 오차를 조금씩 줄여가며 파라미터를 갱신하던 반복 루프와 사고방식이 같습니다. 병렬이 아니라 순차라서 느리지만 대체로 더 정확합니다.

## 20.2 RandomForest — 대표 배깅 모델

`RandomForestClassifier`는 17장의 결정 트리와 **완전히 같은** `fit`/`predict` 인터페이스를 씁니다. 트리를 숲으로 바꾸기만 하면 됩니다.

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=50, random_state=42)
rf.fit(X_train, y_train)
acc = rf.score(X_test, y_test)   # score = 분류 정확도
print(round(acc, 2) > 0.5)
# 출력: True
```

단일 트리보다 숲이 왜 나은지 비교해 봅니다. 같은 데이터에서 결정 트리 한 그루는 test 성능이 출렁이지만, 숲은 이를 평균 내어 안정됩니다.

```python
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(random_state=42).fit(X_train, y_train)
print(tree.score(X_test, y_test) <= 1.0)
# 출력: True
```

> ⚠️ **함정**: `n_estimators`(트리 개수)는 크게 잡을수록 안정적이지만 그만큼 느려집니다. JS에서 루프 반복 횟수를 무작정 늘리지 않듯, 100~300 선에서 타협합니다. `random_state`를 고정하지 않으면 부트스트랩 샘플링이 매번 달라져 결과가 재현되지 않습니다.

## 20.3 GradientBoosting — 대표 부스팅 모델

`GradientBoostingClassifier`도 인터페이스는 동일합니다. 다른 점은 트리를 **순차적으로** 쌓아 오차를 줄인다는 것입니다.

```python
from sklearn.ensemble import GradientBoostingClassifier

gb = GradientBoostingClassifier(n_estimators=50, learning_rate=0.1,
                                random_state=42)
gb.fit(X_train, y_train)
print(gb.n_estimators)
# 출력: 50
```

`learning_rate`(학습률)는 각 트리가 오차를 얼마나 반영할지 정하는 부스팅 고유 파라미터입니다. 작을수록 신중하게(과적합↓) 학습하지만 더 많은 트리가 필요합니다.

> 🎯 **AICE**: Professional 실기에서 `RandomForestClassifier(n_estimators=...)`와 `GradientBoostingClassifier(learning_rate=..., n_estimators=...)`의 생성자 인자를 빈칸으로 냅니다. 분류는 `...Classifier`, 회귀는 `...Regressor`로 이름만 바뀐다는 점을 함께 외우세요.

## 20.4 특성 중요도

앙상블 모델의 큰 장점은 **어떤 특성이 예측에 기여했는지** 알려준다는 점입니다. `feature_importances_`는 합이 1인 배열로, `pd.Series`에 담아 정렬하면 읽기 좋습니다.

```python
import pandas as pd

importances = pd.Series(rf.feature_importances_).sort_values(ascending=False)
print(round(importances.sum(), 2))   # 중요도 총합은 1
# 출력: 1.0
```

```python
top_feature = importances.index[0]   # 가장 중요한 특성의 인덱스
print(top_feature >= 0)
# 출력: True
```

> ⚠️ **JS 함정**: `feature_importances_`는 끝에 언더스코어가 붙습니다. sklearn 관례상 **학습 후 생성된 속성**에는 `_`가 붙습니다(`coef_`, `classes_`도 동일). `fit` 전에 접근하면 에러가 나므로, JS에서 초기화 전 프로퍼티를 읽는 실수와 같은 함정입니다.

## 20.5 XGBoost·LightGBM

XGBoost와 LightGBM은 부스팅을 고도로 최적화한 별도 라이브러리로, 캐글·실무에서 표준처럼 쓰입니다. 이 실행 환경에는 미설치이므로 아래는 `no-run`입니다. 설치는 `pip install xgboost lightgbm`.

API는 sklearn과 호환되게 설계되어 `fit`/`predict`/`feature_importances_`를 그대로 씁니다. 즉 17장의 estimator 인터페이스만 알면 라이브러리를 갈아끼우기만 하면 됩니다.

```python no-run
from xgboost import XGBClassifier

xgb = XGBClassifier(n_estimators=100, learning_rate=0.1,
                    max_depth=3, random_state=42)
xgb.fit(X_train, y_train)
pred = xgb.predict(X_test)
print(xgb.feature_importances_)   # sklearn과 동일한 인터페이스
```

```python no-run
from lightgbm import LGBMClassifier

lgbm = LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
lgbm.fit(X_train, y_train)
pred = lgbm.predict(X_test)
```

> 🎯 **AICE (출제 이력 불확실)**: XGBoost·LightGBM의 AICE 실기 등장 여부는 **회차별 편차가 있어 공식 범위상 확실하지 않습니다**. 등장하더라도 위처럼 sklearn과 같은 `fit`/`predict` 형태이므로, sklearn 앙상블(RandomForest·GradientBoosting)을 확실히 익히면 전이가 쉽습니다. 시험 대비 우선순위는 sklearn 계열에 두세요.

## 연습문제

**Q1.** 트리 100개짜리 RandomForest 분류기를 학습하도록 빈칸을 채우세요.

```python no-run
from sklearn.ensemble import ____
model = RandomForestClassifier(____=100, random_state=42)
model.____(X_train, y_train)
```

<details><summary>정답</summary>

```python no-run
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

`n_estimators`가 트리 개수, `fit`으로 학습합니다.
</details>

**Q2.** 학습된 모델의 특성 중요도를 내림차순 Series로 만드세요.

```python no-run
import pandas as pd
imp = pd.Series(model.____, index=X.columns)
imp = imp.sort_values(ascending=____)
```

<details><summary>정답</summary>

```python no-run
imp = pd.Series(model.feature_importances_, index=X.columns)
imp = imp.sort_values(ascending=False)
```

`feature_importances_`(언더스코어 필수), `ascending=False`로 큰 값이 위로 옵니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| 여러 판정 함수 다수결 | 배깅 / `RandomForestClassifier` | 병렬·독립 트리의 투표 |
| 오차 줄이는 반복 개선 루프 | 부스팅 / `GradientBoostingClassifier` | 순차적 오차 보정 |
| 초기화 전 프로퍼티 접근 오류 | `fit` 전 `feature_importances_` 접근 오류 | `_` 접미사 = 학습 후 속성 |
| 라이브러리 교체 | XGBoost/LightGBM (동일 `fit`/`predict`) | estimator 인터페이스 공통 |
