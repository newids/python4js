# Chapter 22. 모델 평가 심화와 교차검증

> **학습 목표**
> - K-Fold 교차검증으로 단일 분할보다 신뢰도 높은 성능을 추정할 수 있다.
> - `cross_val_score`로 여러 폴드 점수를 한 번에 계산할 수 있다.
> - ROC 곡선·AUC로 임계값 전반의 분류 성능을 평가할 수 있다.
> - precision-recall 트레이드오프를 이해하고 임계값을 조정할 수 있다.

17장의 `train_test_split`은 데이터를 한 번만 나눕니다. 운 나쁜 분할이면 성능이 왜곡됩니다. **교차검증(cross-validation)**은 분할을 여러 번 바꿔 평균 내어 이 불안정을 줄입니다. AUC·임계값 조정은 정확도 하나로는 안 보이는 분류기의 실체를 드러냅니다. 계산은 sklearn으로 실행 가능하며, **시각화(ROC 플롯) 부분만** matplotlib 미설치로 `no-run`입니다.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=300, n_features=6, n_informative=4,
                           weights=[0.7, 0.3], random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42)
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print(X_test.shape)
# 출력: (90, 6)
```

## 22.1 K-Fold 교차검증

K-Fold는 데이터를 k등분해, 매번 한 조각을 검증용으로 두고 나머지로 학습하기를 k번 반복합니다. 개념적으로는 `train_test_split`을 위치를 바꿔 k번 돌려 평균 내는 것입니다.

```python
from sklearn.model_selection import cross_val_score, KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf, scoring="accuracy")
print(len(scores))   # 폴드마다 하나씩, 총 5개 점수
# 출력: 5
```

점수 배열의 평균과 표준편차를 함께 봅니다. 표준편차가 크면 데이터 분할에 민감하다는 신호입니다.

```python
print(0.0 <= scores.mean() <= 1.0)
# 출력: True
```

> ⚠️ **함정**: `cross_val_score`는 넘긴 모델을 **내부에서 복제해** 폴드마다 새로 학습합니다. 원본 `model` 객체는 바뀌지 않으므로, JS에서 함수에 객체를 넘겨 변형됐는지 걱정하던 것과 달리 부작용이 없습니다. 반환값은 "점수 배열"일 뿐, 학습된 모델이 아닙니다.

분류에서는 클래스 비율을 폴드마다 유지하는 **StratifiedKFold**가 기본입니다. 불균형 데이터에서 특히 중요합니다.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5)
strat_scores = cross_val_score(model, X, y, cv=skf)
print(strat_scores.shape)
# 출력: (5,)
```

> 🎯 **AICE**: `cross_val_score(model, X, y, cv=5)`의 인자 순서와 반환이 "점수 배열"이라는 점, 그리고 `.mean()`으로 대표값을 내는 흐름이 Professional에 자주 나옵니다.

## 22.2 ROC 곡선과 AUC

정확도는 임계값 0.5를 고정한 한 점의 성능일 뿐입니다. **ROC 곡선**은 임계값을 0~1로 훑으며 (거짓양성률, 참양성률)을 그린 곡선이고, **AUC**는 그 아래 면적(1에 가까울수록 좋음, 0.5는 무작위)입니다. 임계값 전반의 분류력을 하나의 수로 요약합니다.

AUC 계산에는 클래스가 아니라 **확률**이 필요합니다. `predict`가 아니라 `predict_proba`를 씁니다.

```python
from sklearn.metrics import roc_auc_score

proba = model.predict_proba(X_test)[:, 1]   # 양성(1) 클래스 확률
auc = roc_auc_score(y_test, proba)
print(0.0 <= auc <= 1.0)
# 출력: True
```

`roc_curve`는 곡선을 그릴 좌표(fpr, tpr)와 각 임계값을 반환합니다.

```python
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, proba)
print(fpr.min() == 0.0)
# 출력: True
```

> ⚠️ **함정**: `predict_proba`는 (표본 수 × 클래스 수) 2차원 배열을 반환합니다. 양성 클래스 확률만 쓰려면 `[:, 1]`로 두 번째 열을 골라야 합니다. `predict`(0/1 라벨)를 `roc_auc_score`에 넣으면 곡선이 계단이 되어 AUC가 왜곡됩니다.

시각화는 matplotlib이 필요해 아래는 `no-run`입니다. 설치 시 `pip install matplotlib`.

```python no-run
import matplotlib.pyplot as plt

plt.plot(fpr, tpr, label=f"AUC = {auc:.2f}")
plt.plot([0, 1], [0, 1], "--")   # 무작위 분류기 기준선
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.show()
```

## 22.3 precision-recall 트레이드오프와 임계값 조정

기본 임계값은 0.5지만, 문제에 따라 조정합니다. 임계값을 **낮추면** 양성 판정이 늘어 재현율(recall)↑·정밀도(precision)↓, **높이면** 반대입니다. 암 진단처럼 놓치면 안 되는 문제는 임계값을 낮춰 recall을 확보합니다.

```python
from sklearn.metrics import precision_score, recall_score

pred_default = (proba >= 0.5).astype(int)   # 기본 임계값
pred_low = (proba >= 0.3).astype(int)        # 임계값 낮춤

r_default = recall_score(y_test, pred_default, zero_division=0)
r_low = recall_score(y_test, pred_low, zero_division=0)
print(r_low >= r_default)   # 임계값을 낮추면 recall은 줄지 않음
# 출력: True
```

정밀도와 재현율은 이렇게 서로 밀고 당깁니다. 둘의 조화평균이 **f1 점수**이고, 임계값을 직접 옮겨 원하는 지점을 고르는 것이 임계값 조정입니다.

```python
p = precision_score(y_test, pred_default, zero_division=0)
r = recall_score(y_test, pred_default, zero_division=0)
print(0.0 <= p <= 1.0 and 0.0 <= r <= 1.0)
# 출력: True
```

> 🎯 **AICE**: `(proba >= 임계값).astype(int)`로 확률을 라벨로 바꾸는 관용구, 그리고 recall과 precision이 트레이드오프 관계라는 개념이 Professional 서술·빈칸형으로 나옵니다.

## 22.4 다중분류 평가

클래스가 3개 이상이면 precision·recall·f1을 클래스별로 구한 뒤 평균합니다. `average` 인자로 평균 방식을 정합니다: `"macro"`(클래스 단순 평균), `"weighted"`(표본 수 가중).

```python
from sklearn.metrics import f1_score

X3, y3 = make_classification(n_samples=200, n_features=6, n_informative=4,
                             n_classes=3, random_state=42)
m3 = LogisticRegression(max_iter=1000).fit(X3, y3)
pred3 = m3.predict(X3)
macro_f1 = f1_score(y3, pred3, average="macro")   # 다중분류엔 average 필수
print(0.0 <= macro_f1 <= 1.0)
# 출력: True
```

> 🎯 **AICE (출제 이력 불확실)**: 다중분류 세부 평가(`average` 옵션 선택 등)는 AICE 공개 범위에 명시가 적어 **회차별 출제 편차가 있을 수 있습니다**. 이진분류의 accuracy/precision/recall/f1/AUC를 먼저 확실히 하고, 다중분류는 "`average="macro"`를 지정한다"는 개념 수준으로 대비하는 편이 안전합니다.

## 연습문제

**Q1.** 5-폴드 교차검증 정확도의 평균을 구하도록 빈칸을 채우세요.

```python no-run
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=____, scoring="accuracy")
print(scores.____())
```

<details><summary>정답</summary>

```python no-run
scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(scores.mean())
```

`cv`는 폴드 수, 결과 배열에 `.mean()`으로 대표값을 냅니다.
</details>

**Q2.** 양성 클래스 확률로 AUC를 계산하도록 빈칸을 채우세요.

```python no-run
from sklearn.metrics import roc_auc_score
proba = model.____(X_test)[:, 1]
auc = roc_auc_score(y_test, ____)
```

<details><summary>정답</summary>

```python no-run
proba = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, proba)
```

`predict_proba`로 확률을 얻고 `[:, 1]`로 양성 클래스 열을 골라 AUC에 넣습니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| split을 여러 번 반복해 평균 | `cross_val_score(model, X, y, cv=)` | 반환은 점수 배열 |
| 객체 넘겨도 원본 불변 | `cross_val_score`는 모델 복제 학습 | 부작용 없음 |
| 임계값별 성능 곡선 | `roc_curve` / `roc_auc_score` | 확률(`predict_proba`) 필요 |
| 배열 열 선택 `arr.map(r=>r[1])` | `predict_proba(X)[:, 1]` | 양성 클래스 확률 |
| 판정 경계 조정 | `(proba >= t).astype(int)` | 임계값 튜닝 |
