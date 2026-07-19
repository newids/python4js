# Chapter 17. Scikit-learn 모델링 프로세스

> **학습 목표**
> - train_test_split으로 데이터를 학습·평가용으로 분리할 수 있다
> - 모든 모델이 공유하는 fit/predict 인터페이스를 이해하고 사용할 수 있다
> - LinearRegression/LogisticRegression/DecisionTree로 회귀·분류 모델을 학습할 수 있다
> - 회귀(MAE/RMSE/R²)와 분류(accuracy/f1/confusion_matrix) 평가지표를 계산할 수 있다

이제 전처리한 데이터로 모델을 만듭니다. scikit-learn의 가장 큰 미덕은 **모든 모델이 똑같은 인터페이스**를 쓴다는 점입니다. 회귀든 분류든 트리든, `모델 = 클래스()` → `모델.fit(X, y)` → `모델.predict(X)`의 3단계가 동일합니다. 9장에서 배운 클래스·객체·메서드가 여기서 그대로 실전이 됩니다. 이 챕터는 AICE Associate 실기의 종착점입니다.

## 17.1 데이터 분리 — train_test_split

모델을 학습에 쓴 데이터로 평가하면 "외운 답"을 채점하는 셈이라 성능이 부풀려집니다. 그래서 데이터를 학습용과 평가용으로 나눕니다. `train_test_split`이 이를 무작위로 갈라 4개(X_train, X_test, y_train, y_test)를 **한 줄로 반환**합니다(7장의 다중 반환·언패킹).

```python
import numpy as np
from sklearn.model_selection import train_test_split

X = np.arange(20).reshape(10, 2)   # 10샘플 × 2특성
y = np.arange(10)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
print(X_train.shape, X_test.shape)   # 7:3 분리
# 출력: (7, 2) (3, 2)
```

`test_size`는 평가용 비율, `random_state`는 재현성을 위한 난수 시드입니다. 분류에서는 `stratify=y`로 클래스 비율을 유지하기도 합니다.

> ⚠️ **함정**: 반환 순서는 **X_train, X_test, y_train, y_test**로 고정입니다. `X_train, y_train, X_test, y_test`로 받으면 문법 오류 없이 실행되지만 데이터가 뒤섞여 조용히 망가집니다. 순서를 손가락에 익히세요 — 실기 최다 실수 중 하나입니다.

> 🎯 **AICE**: `train_test_split(X, y, test_size=0.2, random_state=42)`는 실기의 고정 관용구입니다. `test_size`와 `random_state`를 빈칸으로 두는 형태가 자주 나오며, `random_state`를 지정하지 않으면 채점 기준과 결과가 달라질 수 있으니 항상 명시하세요.

## 17.2 estimator API — fit과 predict

scikit-learn의 모든 모델은 **estimator**라는 공통 객체 규약을 따릅니다. 9장의 관점으로 보면, 각 모델은 클래스이고 `fit`·`predict`는 그 인스턴스의 메서드입니다. `fit`이 데이터에서 내부 파라미터를 학습해 객체 상태를 갱신하고, `predict`가 그 상태로 예측합니다.

| 단계 | 코드 | 9장 대응 |
|---|---|---|
| 생성 | `model = LinearRegression()` | 인스턴스 생성 `__init__` |
| 학습 | `model.fit(X, y)` | 상태 갱신 메서드 |
| 예측 | `model.predict(X)` | 상태 사용 메서드 |

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()          # 1. 객체 생성
model.fit(X_train, y_train)         # 2. 학습(상태 갱신)
preds = model.predict(X_test)       # 3. 예측
print(preds.shape)
# 출력: (3,)
```

학습으로 채워진 상태는 **밑줄로 끝나는 속성**(`coef_`, `intercept_`)에 저장됩니다. 밑줄 접미사는 "fit 이후에 생기는 값"이라는 scikit-learn의 관례입니다.

```python
print(hasattr(model, "coef_"))      # fit 후 생김
# 출력: True
```

## 17.3 회귀 — LinearRegression과 평가지표

목표값이 연속 숫자(집값·점수)면 회귀입니다. 완벽히 선형인 데이터로 지표를 확인해 봅니다. `y = 3x + 5` 관계를 심으면 모델이 이를 되찾습니다.

```python
X_reg = np.arange(0, 50).reshape(-1, 1).astype(float)
y_reg = (3 * X_reg.flatten() + 5)          # 정확히 선형

Xtr, Xte, ytr, yte = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)
reg = LinearRegression().fit(Xtr, ytr)
print(round(reg.coef_[0], 1), round(reg.intercept_, 1))   # 기울기, 절편 복원
# 출력: 3.0 5.0
```

회귀 평가지표 3종입니다. **MAE**(평균절대오차)는 오차의 절댓값 평균, **RMSE**(평균제곱근오차)는 큰 오차에 민감, **R²**(결정계수)는 1에 가까울수록 좋습니다.

```python
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

pred_reg = reg.predict(Xte)
print(round(mean_absolute_error(yte, pred_reg), 2))     # 오차 거의 0
# 출력: 0.0
print(round(root_mean_squared_error(yte, pred_reg), 2))
# 출력: 0.0
print(round(r2_score(yte, pred_reg), 3))                # 완벽 예측=1.0
# 출력: 1.0
```

> ⚠️ **함정**: 예전 자료의 `mean_squared_error(y, pred, squared=False)`로 RMSE를 구하는 방식은 최신 scikit-learn에서 제거되었습니다. RMSE는 전용 함수 `root_mean_squared_error`를 쓰거나 `np.sqrt(mean_squared_error(...))`로 계산하세요.

## 17.4 분류 — LogisticRegression과 평가지표

목표값이 범주(합격/불합격, 개/고양이)면 분류입니다. 이름과 달리 `LogisticRegression`은 분류 모델입니다. 명확히 나뉘는 데이터로 지표를 확인합니다.

```python
from sklearn.linear_model import LogisticRegression

# 두 그룹이 뚜렷이 분리된 데이터
X_clf = np.array([[i] for i in [1, 2, 3, 4, 20, 21, 22, 23]], dtype=float)
y_clf = np.array([0, 0, 0, 0, 1, 1, 1, 1])

Xtr, Xte, ytr, yte = train_test_split(X_clf, y_clf, test_size=0.5, random_state=42)
clf = LogisticRegression().fit(Xtr, ytr)
pred_clf = clf.predict(Xte)
print(pred_clf.tolist())
# 출력: [0, 1, 0, 1]
```

분류 평가지표입니다. **accuracy**(정확도)는 맞힌 비율, **f1**은 정밀도·재현율의 조화평균(불균형 데이터에서 중요), **confusion_matrix**는 실제 vs 예측 교차표입니다.

```python
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

print(accuracy_score(yte, pred_clf))     # 완벽 분리=1.0
# 출력: 1.0
print(f1_score(yte, pred_clf))
# 출력: 1.0
print(confusion_matrix(yte, pred_clf).shape)   # 2×2 (클래스 2개)
# 출력: (2, 2)
```

> 🎯 **AICE**: 회귀 문항은 `r2_score`·RMSE를, 분류 문항은 `accuracy_score`·`f1_score`·`confusion_matrix`를 계산하라고 요구합니다. 모든 지표 함수의 인자 순서가 **`(정답 y_test, 예측 pred)`**임을 기억하세요 — 순서를 바꿔도 값이 나오는 지표가 있어 조용히 틀리기 쉽습니다.

## 17.5 DecisionTree — 같은 인터페이스, 다른 모델

의사결정나무는 회귀·분류 모두 가능하며, 인터페이스는 앞과 완전히 동일합니다. 모델 클래스만 바꾸면 됩니다 — 이것이 estimator API의 힘입니다.

```python
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=3, random_state=42)
tree.fit(Xtr, ytr)
print(accuracy_score(yte, tree.predict(Xte)))
# 출력: 1.0
```

`max_depth`(트리 깊이) 같은 값은 학습으로 정해지지 않고 사람이 지정하는 **하이퍼파라미터**입니다(21장에서 자동 탐색). 트리 계열은 어떤 특성이 중요했는지도 알려 줍니다.

```python
print(tree.feature_importances_.shape)   # 특성 수만큼
# 출력: (1,)
```

> ⚠️ **함정**: `DecisionTreeClassifier`(분류)와 `DecisionTreeRegressor`(회귀)는 다른 클래스입니다. 목표값이 범주면 Classifier, 연속값이면 Regressor입니다. 회귀 문제에 Classifier를 쓰면 연속값을 범주로 오인해 엉뚱한 결과가 나오니 목표변수 종류를 먼저 확인하세요.

## 연습문제

**Q1.** 데이터를 8:2로 분리하되 재현 가능하도록 시드를 42로 고정하려 합니다. 빈칸을 채우세요.

```python no-run
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=____, random_state=____
)
```

<details><summary>정답</summary>

```python
import numpy as np
from sklearn.model_selection import train_test_split
X = np.arange(20).reshape(10, 2); y = np.arange(10)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(X_test.shape[0])
# 출력: 2
```

`test_size=0.2`가 20%를 평가용으로, `random_state=42`가 분리를 고정합니다.
</details>

**Q2.** 선형회귀 모델을 학습시키고 예측하려 합니다. 빈칸을 채우세요.

```python no-run
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.____(X_train, y_train)     # 학습
preds = model.____(X_test)       # 예측
```

<details><summary>정답</summary>

```python
import numpy as np
from sklearn.linear_model import LinearRegression
X_train = np.arange(10).reshape(-1, 1).astype(float)
y_train = 2 * X_train.flatten()
model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_train)
print(round(model.coef_[0], 1))
# 출력: 2.0
```

`fit`으로 학습하고 `predict`로 예측합니다. 모든 estimator가 공유하는 인터페이스입니다.
</details>

**Q3.** 분류 결과의 정확도를 계산하려 합니다. 인자 순서에 주의해 빈칸을 채우세요.

```python no-run
from sklearn.metrics import accuracy_score
acc = accuracy_score(____, ____)   # (정답, 예측)
```

<details><summary>정답</summary>

```python
from sklearn.metrics import accuracy_score
y_test = [0, 1, 1, 0]
pred = [0, 1, 1, 0]
acc = accuracy_score(y_test, pred)
print(acc)
# 출력: 1.0
```

평가지표 함수는 `(정답 y_test, 예측 pred)` 순서로 넘깁니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| 개념 | Python (scikit-learn) | 비고 |
|----|--------|------|
| 데이터 분리 | `train_test_split(X, y, test_size=, random_state=)` | 반환 순서 고정 |
| 객체 생성 (9장 `__init__`) | `model = LinearRegression()` | 모델 = 클래스 인스턴스 |
| 학습 메서드 | `model.fit(X_train, y_train)` | 상태(`coef_`) 갱신 |
| 예측 메서드 | `model.predict(X_test)` | 학습된 상태 사용 |
| 회귀 지표 | `mean_absolute_error` / `root_mean_squared_error` / `r2_score` | `(정답, 예측)` 순 |
| 분류 지표 | `accuracy_score` / `f1_score` / `confusion_matrix` | `(정답, 예측)` 순 |
| 하이퍼파라미터 | `DecisionTreeClassifier(max_depth=3)` | 사람이 지정 |
