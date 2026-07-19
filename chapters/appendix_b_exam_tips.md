# Appendix B. AICE 실기 팁과 자주 하는 실수

> AICE 실기는 **빈 셀에 코드를 채워 오류 없이 실행**시키는 형태입니다. 자동완성에 의존하면 시험장에서 무너지므로, API 시그니처를 **손으로 쓸 수 있어야** 합니다. 이 부록은 각 챕터의 🎯 AICE 콜아웃과 시험 범위 참조를 트랙별로 취합했습니다.

## B.1 시험 트랙 개요

| 트랙 | 대상 | 범위 | 이 책의 커버 |
|------|------|------|------|
| **Associate** | 실무자·개발자 | EDA→전처리→분리→모델링→평가 파이프라인 | Part 1 + Part 2 (1~18장) |
| **Professional** | AI 개발자 | Associate + 특성공학·앙상블·튜닝·교차검증·CNN/RNN·텍스트 | 전체 (1~24장) |

두 트랙 모두 Jupyter + Python 실기입니다. Associate를 통과한 뒤 Part 3를 얹으면 Professional로 이어집니다.

## B.2 공통 실기 팁 (JS 개발자용)

**Restart & Run All로 재현성 확인.** Jupyter 셀은 실행한 순서대로 상태가 쌓입니다(1장). 위→아래 순서와 실제 실행 순서가 다르면 채점 시 오류가 납니다. 제출 전 반드시 커널을 재시작하고 처음부터 전부 실행하세요.

**첫 셀 import는 통째로 암기.** 실기 첫 셀은 거의 항상 아래로 시작합니다. 별칭을 틀리면 이후 모든 코드가 연쇄로 무너집니다(10장).

```python
import numpy as np
import pandas as pd
print(np.__name__, pd.__name__)
# 출력: numpy pandas
```

**shape를 습관적으로 확인.** 모델 입력 전 `X.shape`로 `(샘플 수, 특성 수)`를 눈으로 확인하는 것이 shape 불일치 에러를 막는 가장 빠른 길입니다(13장).

**포맷 스펙으로 답 제출.** 성능 출력은 `print(f"정확도: {acc:.2f}")`처럼 자릿수를 고정합니다(3장).

## B.3 JS 개발자 습관성 오타 체크리스트

시험장에서 무의식적으로 저지르는 JS 습관입니다. 제출 전 이 목록을 훑으세요.

| # | JS 습관 | Python 정답 | 근거 |
|---|--------|------|------|
| 1 | `arr.push(x)` | `lst.append(x)` | 4장 |
| 2 | `x == None` | `x is None` | 2장 |
| 3 | `if (arr)`로 존재 확인 | `if arr is not None:` | 2장 |
| 4 | `cond ? a : b` | `a if cond else b` | 5장 |
| 5 | `self` 누락 | `def method(self):` | 9장 |
| 6 | `df[A and B]` | `df[(A) & (B)]` | 14장 |
| 7 | `f1_score(pred, y)` | `f1_score(y_test, pred)` | 17장 |
| 8 | 탭·스페이스 혼용 | 스페이스 4칸 통일 | 5장 |

## B.4 Associate 트랙 팁

Associate는 **정형화된 파이프라인**을 그대로 따라갑니다. 순서와 대표 API를 통째로 외우면 절반은 풉니다.

**파이프라인 6단계 시그니처.**

```python no-run
# 1. EDA
df.head(); df.info(); df.describe()
# 2. 전처리
df.isnull().sum(); df["c"].fillna(값); pd.get_dummies(df, columns=[...])
# 3. 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 4. 모델링
model = LogisticRegression(); model.fit(X_train, y_train)
# 5. 예측·평가
pred = model.predict(X_test); accuracy_score(y_test, pred)
# 6. 딥러닝
model.compile(optimizer="adam", loss="...", metrics=["accuracy"])
```

- **EDA는 `head`/`info`/`describe` 3종 세트**로 시작하고, `info()`로 결측 열을 찾아 전처리로 넘어갑니다(14장).
- **불리언 인덱싱 `df[df["col"] 조건]`**은 매 회 등장합니다. "조건 행 추출 → 개수/평균 집계" 손동작을 몸에 익히세요(14장).
- **인코딩 관례**: 입력 X의 범주형은 `get_dummies`(원-핫), 목표 y의 라벨은 `LabelEncoder`(15장).
- **`train_test_split`의 `random_state`는 항상 명시**합니다. 안 하면 채점 기준과 결과가 달라집니다(17장).
- **활성화↔loss 짝**: `sigmoid`↔`binary_crossentropy`, `softmax`↔`categorical_crossentropy`. 정수 라벨이면 `sparse_`를 붙입니다(18장).
- **시각화 인자 이름**: `sns.countplot(data=df, x="col")`처럼 `data`/`x`가 빈칸으로 나옵니다. 학습곡선은 `plt.plot(...)` 뒤 `plt.legend()`를 짝으로(16장).

## B.5 Professional 트랙 팁

Professional은 Associate 파이프라인을 **심화·자동화**합니다. 코딩 비중이 높고, 데이터 누수 방지가 핵심 채점 포인트입니다.

- **`fit_transform` vs `transform` 구분**: train에는 `fit_transform`, test에는 `transform`만. 이 빈칸이 자주 나옵니다(19장). test에 `fit`하면 누수입니다.
- **특성 중요도**: `pd.Series(model.feature_importances_, index=X.columns).sort_values()` 관용구를 외우세요. `_` 접미사는 학습 후에만 생기는 속성입니다(19장, 20장).
- **앙상블 생성자**: `RandomForestClassifier(n_estimators=)`, `GradientBoostingClassifier(learning_rate=, n_estimators=)`. 분류는 `...Classifier`, 회귀는 `...Regressor`(20장).
- **GridSearchCV 구조**: `GridSearchCV(estimator, param_grid, cv=)`. `param_grid`는 **딕셔너리**, 값은 **리스트**입니다. 결과는 `best_params_`/`best_score_`(21장).
- **Pipeline 파라미터**: `단계이름__파라미터` 더블 언더스코어 표기. 전처리를 교차검증 안에서 수행해 누수를 막는 정석입니다(21장).
- **교차검증**: `cross_val_score(model, X, y, cv=5)`는 점수 배열을 반환하고 `.mean()`으로 대표값을 냅니다(22장).
- **임계값 조정**: `(proba >= 임계값).astype(int)`로 확률을 라벨로 변환. precision-recall은 트레이드오프 관계입니다(22장).
- **콜백**: `EarlyStopping(monitor="val_loss", patience=)` + `fit(..., callbacks=[...])`, `restore_best_weights=True`로 최적 가중치 복원(23장).
- **텍스트 벡터화**: `CountVectorizer`(빈도)와 `TfidfVectorizer`(중요도 가중)는 인터페이스가 같습니다. 차이만 기억하세요(24장).

## B.6 트랙별 시간 배분 가이드

| 단계 | Associate | Professional |
|------|-----------|-------------|
| EDA·전처리 | 40% | 30% |
| 모델링·학습 | 35% | 35% |
| 평가·튜닝·시각화 | 15% | 25% (튜닝·교차검증 비중↑) |
| 검토(Restart & Run All) | 10% | 10% |

전처리에서 막히면 뒤 단계 전체가 밀립니다. 결측·인코딩·스케일링 시그니처를 반사적으로 쓸 수 있을 때까지 손에 익히는 것이 최우선입니다.

> ℹ️ AICE 공식 출제 범위는 회차별 편차가 있습니다. 최신 정보는 aice.study 공식 사이트에서 확인하세요. 특히 Professional 상세 범위(불균형 데이터·다중분류 평가·임베딩)와 XGBoost/LightGBM 출제 이력은 갱신될 수 있습니다.
