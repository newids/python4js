# Chapter 18. Keras 딥러닝 기초

> **학습 목표**
> - Sequential과 Dense로 신경망 구조를 쌓을 수 있다
> - compile로 optimizer/loss/metrics를 설정할 수 있다
> - fit의 epochs/batch_size/validation로 학습을 제어할 수 있다
> - EarlyStopping/ModelCheckpoint 콜백과 evaluate로 학습을 관리·평가할 수 있다

딥러닝은 AICE Associate 실기의 마지막 관문입니다. 다행히 Keras는 17장의 scikit-learn과 **정신 모델이 같습니다**: 모델을 만들고(구성) → 설정하고(compile) → 학습하고(fit) → 평가한다(evaluate). 층(layer)을 순서대로 쌓는 것은 함수를 합성하거나 미들웨어를 체이닝하던 감각과 비슷합니다. 새로 외울 것은 "층의 종류와 compile 인자"뿐입니다.

> 📦 **설치 안내**: 이 챕터의 코드는 실행 환경에 TensorFlow/Keras가 없어 검증에서 제외됩니다. 로컬에서 실습하려면 다음을 설치하세요.
> ```bash
> pip install tensorflow
> ```
> `from tensorflow import keras`로 불러오며, 최신 Keras 3 기준으로 설명합니다.

## 18.1 Sequential과 Dense — 층을 쌓기

가장 기본 구조는 층을 **일렬로 쌓는** `Sequential`입니다. 각 `Dense`(완전연결층)는 뉴런 수와 활성화 함수를 받습니다. JS로 비유하면 입력을 순서대로 통과시키는 변환 파이프라인을 선언하는 것과 같습니다.

```python no-run
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    keras.Input(shape=(10,)),                 # 입력 특성 10개
    layers.Dense(64, activation="relu"),      # 은닉층 64뉴런
    layers.Dense(32, activation="relu"),      # 은닉층 32뉴런
    layers.Dense(1, activation="sigmoid"),    # 출력층: 이진분류
])
model.summary()   # 층 구조와 파라미터 수 출력
```

**활성화 함수**는 층에 비선형성을 부여합니다. 은닉층에는 보통 `relu`, 출력층은 문제에 따라 다릅니다: 이진분류는 `sigmoid`(0~1 확률), 다중분류는 `softmax`(합이 1인 분포), 회귀는 활성화 없음(선형).

| 문제 유형 | 출력층 뉴런 수 | 출력층 활성화 |
|---|---|---|
| 회귀 | 1 | 없음(linear) |
| 이진분류 | 1 | sigmoid |
| 다중분류(N클래스) | N | softmax |

> ⚠️ **함정**: 첫 층에서 `keras.Input(shape=(특성수,))`로 입력 형태를 알려 줘야 합니다. `shape`는 **샘플 하나의 형태**라 배치 크기는 넣지 않습니다. 특성이 10개면 `(10,)`이지 `(샘플수, 10)`이 아닙니다. 튜플 안 쉼표(`(10,)`)를 빠뜨리면 정수로 해석돼 에러가 납니다(4장 튜플).

## 18.2 compile — 학습 방법 설정

모델의 뼈대를 만들었으면 **어떻게 학습할지**를 정합니다. 세 가지를 지정합니다: `optimizer`(가중치 갱신 방법, 보통 `"adam"`), `loss`(오차 정의), `metrics`(모니터링할 지표).

```python no-run
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",     # 이진분류용 손실
    metrics=["accuracy"],
)
```

`loss`는 문제 유형과 반드시 짝이 맞아야 합니다. 이것이 딥러닝 실기에서 가장 자주 틀리는 지점입니다.

| 문제 유형 | loss |
|---|---|
| 회귀 | `"mse"` (또는 `"mae"`) |
| 이진분류 | `"binary_crossentropy"` |
| 다중분류(정수 라벨) | `"sparse_categorical_crossentropy"` |
| 다중분류(원-핫 라벨) | `"categorical_crossentropy"` |

> 🎯 **AICE**: `model.compile(optimizer='adam', loss='...', metrics=['accuracy'])`는 실기 고정 패턴이며 `loss` 자리가 빈칸으로 자주 나옵니다. 출력층 활성화와 loss의 짝(`sigmoid`↔`binary_crossentropy`, `softmax`↔`categorical_crossentropy`)을 세트로 외우세요. 목표변수가 정수 라벨이면 `sparse_`를 붙입니다.

## 18.3 fit — 학습 실행

`fit`으로 학습합니다. 17장 scikit-learn의 `fit`과 이름이 같지만, 딥러닝은 데이터를 **여러 번 반복** 학습하므로 인자가 더 많습니다.

- `epochs`: 전체 데이터를 몇 번 반복할지
- `batch_size`: 한 번에 처리할 샘플 수(메모리·속도 조절)
- `validation_split` 또는 `validation_data`: 학습 중 검증 성능 확인

```python no-run
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,     # 학습 데이터의 20%를 검증에 사용
)
```

`fit`은 `history` 객체를 반환하며, `history.history`에 epoch별 손실·지표가 딕셔너리로 담깁니다. 16장의 학습곡선이 이 값을 그리는 것입니다.

```python no-run
print(history.history.keys())
# dict_keys(['loss', 'accuracy', 'val_loss', 'val_accuracy'])
```

> ⚠️ **함정**: `validation_split`은 학습 데이터의 **뒷부분을 순서대로** 떼어 검증에 씁니다. 데이터가 클래스별로 정렬돼 있으면 검증셋이 한 클래스로 쏠려 성능이 왜곡됩니다. 미리 섞여 있지 않다면 17장의 `train_test_split`으로 별도 검증셋을 만들어 `validation_data=(X_val, y_val)`로 넘기는 편이 안전합니다.

## 18.4 콜백 — EarlyStopping과 ModelCheckpoint

**콜백**은 학습 도중 자동으로 개입하는 훅입니다(JS의 이벤트 콜백과 같은 발상). 두 가지가 필수입니다. `EarlyStopping`은 검증 성능이 나아지지 않으면 학습을 조기 종료하고, `ModelCheckpoint`는 가장 좋았던 시점의 모델을 파일로 저장합니다.

```python no-run
early = keras.callbacks.EarlyStopping(
    monitor="val_loss",         # 검증 손실을 감시
    patience=5,                 # 5 epoch 개선 없으면 중단
    restore_best_weights=True,  # 최적 가중치로 복원
)
checkpoint = keras.callbacks.ModelCheckpoint(
    "best_model.keras",         # Keras 3: 확장자 .keras
    monitor="val_loss",
    save_best_only=True,
)

history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early, checkpoint],   # 리스트로 전달
)
```

> ⚠️ **함정**: `patience`는 "몇 epoch까지 참을지"입니다. 너무 작으면 잠깐의 정체에도 조기 종료되고, 너무 크면 과적합이 진행됩니다. 또 `restore_best_weights=True`를 빠뜨리면 조기 종료 시점의(최적이 아닌) 가중치가 남으니 함께 지정하세요. Keras 3에서 `ModelCheckpoint` 경로는 `.keras` 확장자로 끝나야 합니다.

## 18.5 evaluate와 predict — 평가와 예측

학습이 끝나면 평가용 데이터로 최종 성능을 확인합니다. `evaluate`는 compile에서 지정한 loss와 metrics를 반환하고, `predict`는 예측값을 냅니다 — 여기서도 scikit-learn과 인터페이스가 같습니다.

```python no-run
loss, acc = model.evaluate(X_test, y_test)   # [손실, 정확도]
print(f"test accuracy: {acc:.3f}")

probs = model.predict(X_test)                # 확률(sigmoid 출력)
preds = (probs > 0.5).astype("int32")        # 0.5 기준 이진 변환
```

> 🎯 **AICE**: 딥러닝 문항의 마무리는 `model.evaluate(X_test, y_test)`로 성능을 출력하고, `history`로 학습곡선을 그리는 흐름입니다. `evaluate`는 compile의 `metrics`에 따라 반환값 개수가 달라지므로(손실 + 각 지표), 정확도까지 원하면 compile에 `metrics=['accuracy']`를 반드시 넣어야 합니다.

## 연습문제

**Q1.** 특성 8개를 입력받아 이진분류하는 3층 신경망을 만들려 합니다. 빈칸을 채우세요.

```python no-run
from tensorflow import keras
from tensorflow.keras import layers
model = keras.Sequential([
    keras.Input(shape=(____,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="____"),   # 이진분류 출력
])
```

<details><summary>정답</summary>

```python no-run
model = keras.Sequential([
    keras.Input(shape=(8,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])
```

입력 특성이 8개이므로 `(8,)`, 이진분류 출력층은 `sigmoid`입니다.
</details>

**Q2.** 이진분류 모델을 컴파일하려 합니다. 빈칸을 채우세요.

```python no-run
model.compile(
    optimizer="adam",
    loss="____",              # 이진분류 손실
    metrics=["accuracy"],
)
```

<details><summary>정답</summary>

```python no-run
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
```

이진분류의 손실은 `binary_crossentropy`이고, 출력층 `sigmoid`와 짝을 이룹니다.
</details>

**Q3.** 검증 손실이 5 epoch 동안 개선되지 않으면 학습을 멈추는 콜백을 만들려 합니다. 빈칸을 채우세요.

```python no-run
early = keras.callbacks.EarlyStopping(
    monitor="____",
    patience=____,
    restore_best_weights=True,
)
```

<details><summary>정답</summary>

```python no-run
early = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
)
```

검증 손실 `val_loss`를 감시하고, `patience=5`만큼 참은 뒤 최적 가중치로 복원합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| 개념 | Python (Keras) | 비고 |
|----|--------|------|
| 층 쌓기 | `keras.Sequential([...])` | 순차 파이프라인 |
| 완전연결층 | `layers.Dense(뉴런, activation=)` | 은닉층 relu |
| 입력 형태 | `keras.Input(shape=(특성수,))` | 배치 크기 제외 |
| 학습 설정 | `model.compile(optimizer, loss, metrics)` | loss↔출력활성화 짝 |
| 학습 (17장 fit 확장) | `model.fit(X, y, epochs=, batch_size=)` | history 반환 |
| 이벤트 콜백 | `EarlyStopping` / `ModelCheckpoint` | `callbacks=[...]` |
| 평가 (17장과 동일) | `model.evaluate(X_test, y_test)` | [loss, metrics] |
