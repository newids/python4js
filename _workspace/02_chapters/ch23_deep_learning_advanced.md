# Chapter 23. 딥러닝 심화: CNN·RNN·시계열

> **학습 목표**
> - CNN(합성곱 신경망)의 `Conv2D`·`Pooling` 구조와 이미지 데이터 형태를 이해한다.
> - RNN/LSTM으로 시퀀스 데이터를 처리하는 모델을 구성할 수 있다.
> - 시계열 데이터를 윈도우(window)로 잘라 지도학습 형태로 변환할 수 있다.
> - `EarlyStopping`·`ModelCheckpoint` 콜백을 학습에 활용할 수 있다.

18장의 `Sequential`+`Dense`는 정형 데이터(표)를 다뤘습니다. 이미지·텍스트·시계열은 **공간·순서 구조**를 가지므로 전용 층이 필요합니다. 이미지엔 CNN, 순서 데이터엔 RNN/LSTM입니다.

> **⚠️ 실행 환경 안내**: 이 장의 코드는 TensorFlow/Keras가 필요합니다. 미설치 시 다음으로 설치하세요.
> ```bash
> pip install tensorflow
> ```
> 딥러닝 학습은 무거우므로 이 장 예제는 입력 크기·에폭을 **개념 확인용으로 최소화**했습니다(실무에선 더 큰 데이터·에폭). 층을 쌓는 발상은 18장과 동일하니, 새 층의 **역할과 인자**에 집중하세요.

> 🎯 **AICE (출제 이력 불확실)**: CNN·RNN의 AICE Professional 실기 출제 **비중은 공개 정보가 적어 확실하지 않습니다**. 다만 딥러닝 심화는 Professional의 성격상 다뤄질 가능성이 높아, 구조를 손으로 구성할 수 있는 수준까지 익혀두는 것을 권합니다.

## 23.1 CNN — 이미지용 합성곱 신경망

정형 데이터는 `Dense`로 충분하지만, 이미지는 인접 픽셀의 **공간 패턴**(모서리·질감)이 중요합니다. `Conv2D`는 작은 필터를 이미지 위로 훑어 이런 국소 패턴을 뽑고, `MaxPooling2D`는 크기를 줄여 계산량과 위치 민감도를 낮춥니다.

```python
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

tf.random.set_seed(42)
cnn = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D((2, 2)),
    Flatten(),                              # 2D 특성맵 → 1D 벡터
    Dense(64, activation="relu"),
    Dense(10, activation="softmax"),        # 10개 클래스 분류
])
cnn.compile(optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"])
print(cnn.output_shape)   # 마지막 층 출력 형태
# 출력: (None, 10)
```

핵심은 마지막 두 층입니다. `Flatten`으로 합성곱이 만든 2D 특성맵을 펼쳐야 `Dense`에 연결됩니다.

## 23.2 이미지 데이터의 형태

이미지 데이터는 4차원 텐서 **(표본 수, 높이, 너비, 채널)**입니다. 흑백은 채널 1, 컬러(RGB)는 3입니다. 픽셀값(0~255)은 학습 안정을 위해 255로 나눠 0~1로 **정규화**합니다.

```python
import numpy as np

np.random.seed(42)
# 예: 흑백 28×28 이미지 100장
images = np.random.randint(0, 256, size=(100, 28, 28, 1))
images = images.astype("float32") / 255.0   # 0~1 정규화
print(images.shape)
# 출력: (100, 28, 28, 1)
```

> ⚠️ **함정**: `Conv2D`의 `input_shape`에는 **표본 수를 넣지 않습니다**. `(28, 28, 1)`처럼 한 장의 형태만 지정하고, 표본 축은 Keras가 배치 처리 시 자동으로 붙입니다. JS에서 배열 전체 길이를 함께 넘기던 습관과 다릅니다.

## 23.3 RNN/LSTM — 순서가 있는 데이터

문장·주가처럼 **순서**가 의미를 갖는 데이터는 RNN 계열로 처리합니다. 기본 RNN은 긴 시퀀스에서 앞부분을 잊는 문제가 있어, 이를 개선한 **LSTM**을 주로 씁니다. 입력 형태는 **(표본 수, 타임스텝, 특성 수)** 3차원입니다.

```python
from tensorflow.keras.layers import LSTM

timesteps, features = 10, 1
model = Sequential([
    LSTM(64, input_shape=(timesteps, features)),   # 순서 정보 처리
    Dense(1),                                       # 회귀 출력(다음 값 예측)
])
model.compile(optimizer="adam", loss="mse")
print(model.output_shape)
# 출력: (None, 1)
```

텍스트 분류라면 `LSTM` 앞에 `Embedding` 층을 두어 단어 인덱스를 밀집 벡터로 바꿉니다(24장 참조).

```python
from tensorflow.keras.layers import Embedding

text_model = Sequential([
    Embedding(input_dim=10000, output_dim=32),   # 어휘 1만 → 32차원 벡터
    LSTM(64),
    Dense(1, activation="sigmoid"),               # 이진 분류
])
print(len(text_model.layers))
# 출력: 3
```

## 23.4 시계열 데이터 준비 — 윈도우 슬라이싱

시계열은 원본이 1차원 수열이라, 지도학습에 넣으려면 **윈도우**로 잘라야 합니다. "직전 n개 값 → 다음 값"을 (X, y) 쌍으로 만드는 것입니다. 이 변환은 순수 numpy로, 발상은 JS 배열 슬라이딩 윈도우와 같습니다.

```python
def make_windows(series, window):
    X, y = [], []
    for i in range(len(series) - window):
        X.append(series[i:i + window])   # 직전 window개
        y.append(series[i + window])     # 바로 다음 값
    return np.array(X), np.array(y)

series = np.sin(np.linspace(0, 20, 200))
X, y = make_windows(series, window=10)
X = X.reshape(X.shape[0], X.shape[1], 1)   # (표본, 타임스텝, 특성)로 reshape
print(X.shape)
# 출력: (190, 10, 1)
```

> ⚠️ **함정**: LSTM 입력은 반드시 **3차원**이어야 합니다. `make_windows`가 만든 2차원 `(표본, 타임스텝)`을 `reshape(..., ..., 1)`로 특성 축을 추가해야 합니다. 이 축을 빠뜨리면 `expected 3 dimensions` 에러가 납니다.

## 23.5 콜백 — 학습 제어

18장에서 본 `EarlyStopping`·`ModelCheckpoint`는 심화 학습에서 더 중요합니다. 긴 학습에서 과적합 직전에 멈추고(EarlyStopping), 최고 성능 시점을 저장(ModelCheckpoint)합니다.

```python
import os, tempfile
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

ckpt_path = os.path.join(tempfile.gettempdir(), "best_model.keras")
callbacks = [
    EarlyStopping(monitor="val_loss", patience=3,
                  restore_best_weights=True),          # 개선 없으면 조기 중단
    ModelCheckpoint(ckpt_path, monitor="val_loss",
                    save_best_only=True),               # 최고 성능만 저장
]

history = model.fit(
    X, y,
    epochs=3, batch_size=32,   # 시연용 3에폭 (실무에선 크게, EarlyStopping이 중단 담당)
    validation_split=0.2,      # train의 20%를 검증에
    callbacks=callbacks,
    verbose=0,
)
print(len(history.history["loss"]) <= 3)
# 출력: True
```

> 🎯 **AICE**: `EarlyStopping(monitor="val_loss", patience=...)`와 `fit(..., callbacks=[...])`의 결합은 Professional 딥러닝 문항의 단골입니다. `monitor`는 감시할 지표, `patience`는 참을 에폭 수, `restore_best_weights=True`로 최적 가중치를 복원한다는 흐름을 외우세요.

## 연습문제

**Q1.** 첫 합성곱 층에 필터 32개, 3×3 커널, 흑백 28×28 입력을 지정하세요.

```python no-run
model = Sequential([
    Conv2D(____, (____, ____), activation="relu", input_shape=(28, 28, ____)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(10, activation="softmax"),
])
```

<details><summary>정답</summary>

```python no-run
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(10, activation="softmax"),
])
```

필터 수 32, 커널 (3,3), 흑백 채널 1. `input_shape`에 표본 수는 넣지 않습니다.
</details>

**Q2.** 검증 손실이 3에폭 개선되지 않으면 학습을 멈추는 콜백을 만드세요.

```python no-run
from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor="____", patience=____, restore_best_weights=True)
model.fit(X, y, epochs=50, callbacks=[____])
```

<details><summary>정답</summary>

```python no-run
es = EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True)
model.fit(X, y, epochs=50, callbacks=[es])
```

`monitor="val_loss"`, `patience=3`, 콜백은 `callbacks` 리스트에 담습니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python(Keras) | 비고 |
|----|--------|------|
| 층 함수 합성 | `Sequential([Conv2D(...), ...])` | 18장 Dense 스택의 확장 |
| 배열 전체 길이 전달 | `input_shape=(28,28,1)` (표본 축 제외) | 배치 축은 자동 |
| 슬라이딩 윈도우 | `series[i:i+window]` + `reshape` | 시계열 → (표본,타임스텝,특성) |
| 조기 종료 조건문 | `EarlyStopping(patience=...)` | 콜백으로 학습 제어 |
| 단어 → 벡터 매핑 | `Embedding(input_dim, output_dim)` | 24장 텍스트와 연결 |
