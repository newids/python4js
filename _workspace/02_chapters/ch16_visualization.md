# Chapter 16. 시각화

> **학습 목표**
> - matplotlib의 기본 플롯 구조(figure–plot–show)를 이해하고 그릴 수 있다
> - seaborn의 countplot/histplot/boxplot으로 분포를 시각화할 수 있다
> - 상관관계 heatmap으로 특성 간 관계를 읽을 수 있다
> - 학습곡선을 그려 모델의 과적합 여부를 판단할 수 있다

시각화는 EDA에서 "숫자로는 안 보이는 것을 눈으로 확인하는" 단계입니다. JS 개발자라면 Chart.js나 D3로 그려 봤을 것입니다. Python 생태계에서는 **matplotlib**(저수준 엔진)과 그 위에 얹힌 **seaborn**(통계 플롯 특화)이 사실상 표준입니다. AICE 실기에서는 분포·상관·학습곡선을 그리는 문항이 반복됩니다.

> 📦 **설치 안내**: 이 챕터의 플롯을 로컬에서 실습하려면 다음 패키지가 필요합니다(기본 파이썬 환경에는 없을 수 있습니다).
> ```bash
> pip install matplotlib seaborn
> ```
> Jupyter에서는 `%matplotlib inline`을 한 번 실행하면 셀 아래에 그림이 바로 표시됩니다.

## 16.1 matplotlib 기본 — figure, plot, show

matplotlib의 정신 모델은 "빈 도화지(figure)에 요소를 쌓고 마지막에 보여준다(show)"입니다. Chart.js가 설정 객체를 넘기는 선언형이라면, matplotlib는 명령을 순서대로 쌓는 명령형에 가깝습니다.

| JavaScript (Chart.js) | Python (matplotlib) |
|---|---|
| `new Chart(ctx, {type:'line', ...})` | `plt.plot(x, y)` |
| `chart.options.title` | `plt.title("...")` |

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

plt.figure(figsize=(6, 4))     # 도화지 크기(가로, 세로 인치)
plt.plot(x, y, marker="o")     # 선 + 점
plt.title("y = x^2")
plt.xlabel("x")
plt.ylabel("y")
plt.show()                     # 화면에 표시
```

여러 그래프를 나란히 놓을 때는 `subplots`를 씁니다. 반환된 축(`ax`) 객체에 그립니다.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1행 2열
axes[0].plot(x, y)
axes[0].set_title("Line")
axes[1].scatter(x, y)          # 산점도
axes[1].set_title("Scatter")
plt.tight_layout()             # 겹침 방지
plt.show()
```

> ⚠️ **함정**: matplotlib는 "현재 활성 figure"라는 전역 상태를 씁니다. `plt.plot`을 연달아 호출하면 같은 그림에 겹쳐 그려집니다. 새 그림을 원하면 `plt.figure()`로 새 도화지를 열거나, 위처럼 `subplots`로 축을 명시적으로 다루세요. JS의 캔버스별 독립 컨텍스트와 달리 상태가 공유됩니다.

## 16.2 seaborn — 분포를 한 줄로

seaborn은 DataFrame을 직접 받아 통계 플롯을 그립니다. `data=`에 DataFrame, `x=`/`y=`에 열 이름 문자열을 넘기는 패턴이 일관됩니다. 실기 빈출 3종을 봅니다.

**countplot**은 범주형 열의 빈도를 셉니다(막대그래프). `df["col"].value_counts()`를 그림으로 보는 것입니다.

```python
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    "city": ["Seoul", "Busan", "Seoul", "Daegu", "Seoul", "Busan"],
    "age": [25, 30, 35, 28, 42, 33],
})
sns.countplot(data=df, x="city")   # 도시별 개수
plt.title("City Counts")
plt.show()
```

**histplot**은 수치형 열의 분포를 구간(bin)으로 나눠 봅니다. `kde=True`를 주면 밀도 곡선을 겹칩니다.

```python
sns.histplot(data=df, x="age", bins=10, kde=True)
plt.title("Age Distribution")
plt.show()
```

**boxplot**은 사분위수·이상치를 한눈에 보여줍니다. 범주별 분포 비교에 유용합니다(`x`에 범주, `y`에 수치).

```python
sns.boxplot(data=df, x="city", y="age")   # 도시별 나이 분포
plt.title("Age by City")
plt.show()
```

> 🎯 **AICE**: `countplot`(범주 빈도), `histplot`(수치 분포), `boxplot`(이상치 확인)은 실기 EDA 문항에서 "분포를 시각화하라"는 지시에 그대로 대응합니다. `sns.countplot(data=df, x='컬럼')`처럼 `data`와 `x` 인자를 빈칸으로 두는 형태가 자주 출제되니 인자 이름을 정확히 외우세요.

## 16.3 상관관계 heatmap

수치형 특성들이 서로 얼마나 함께 움직이는지를 봅니다. `df.corr()`가 상관계수 행렬(−1~1)을 만들고, `sns.heatmap`이 색으로 표현합니다. 상관이 높은 특성 쌍을 찾아 다중공선성을 점검하는 EDA 단골입니다.

```python
num_df = pd.DataFrame({
    "age": [25, 30, 35, 40, 45],
    "income": [2000, 2500, 4000, 5000, 7000],
    "score": [80, 70, 75, 60, 55],
})
corr = num_df.corr()               # 상관계수 행렬
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation Heatmap")
plt.show()
```

`annot=True`는 셀에 숫자를 표시하고, `cmap`은 색 팔레트, `vmin`/`vmax`로 색 범위를 −1~1에 고정합니다.

> ⚠️ **함정**: `df.corr()`는 **수치형 열만** 대상으로 계산합니다. 문자열 열이 섞여 있으면 자동으로 제외되거나 버전에 따라 에러가 날 수 있으니, `df.select_dtypes(include="number").corr()`처럼 수치형만 골라 넘기는 습관이 안전합니다.

## 16.4 학습곡선 — 과적합을 눈으로

모델을 학습시키면(18장 Keras) epoch별 손실(loss)과 정확도가 기록됩니다. 이를 **학습(train) vs 검증(validation)** 두 선으로 그리면 과적합을 판단할 수 있습니다. 검증 손실이 다시 올라가기 시작하는 지점이 과적합의 신호입니다.

```python
# history는 model.fit(...)이 반환하는 객체 (18장 참조)
epochs = range(1, 11)
train_loss = [0.9, 0.7, 0.55, 0.45, 0.38, 0.33, 0.30, 0.28, 0.27, 0.26]
val_loss   = [0.95, 0.75, 0.60, 0.52, 0.50, 0.51, 0.55, 0.60, 0.66, 0.72]

plt.figure(figsize=(6, 4))
plt.plot(epochs, train_loss, label="train")
plt.plot(epochs, val_loss, label="validation")
plt.xlabel("epoch")
plt.ylabel("loss")
plt.legend()                   # 범례 표시
plt.title("Learning Curve")
plt.show()
# 검증 손실이 5 epoch 부근부터 상승 → 과적합 시작
```

> 🎯 **AICE**: 딥러닝 문항에서 `history.history['loss']`와 `history.history['val_loss']`를 꺼내 두 선을 그리는 학습곡선 시각화가 마무리 단계로 나옵니다. `plt.plot(..., label=...)` 뒤에 `plt.legend()`를 빠뜨려 범례가 안 나오는 실수가 잦으니 짝으로 외우세요.

## 연습문제

**Q1.** 범주형 열 `grade`의 빈도를 막대그래프로 그리려 합니다. 빈칸을 채우세요.

```python no-run
import seaborn as sns
sns.____(data=df, x="grade")
plt.show()
```

<details><summary>정답</summary>

```python no-run
import seaborn as sns
sns.countplot(data=df, x="grade")
plt.show()
```

범주별 개수를 세는 것은 `countplot`입니다. 수치 분포라면 `histplot`을 씁니다.
</details>

**Q2.** 수치형 특성들의 상관계수 행렬을 heatmap으로 그리려 합니다. 빈칸을 채우세요.

```python no-run
corr = df.____()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()
```

<details><summary>정답</summary>

```python no-run
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.show()
```

`df.corr()`가 상관계수 행렬을 만들고, `annot=True`로 각 셀에 값을 표시합니다.
</details>

**Q3.** 학습곡선에서 검증 손실 선에 범례가 나오도록 하려 합니다. 빈칸을 채우세요.

```python no-run
plt.plot(epochs, val_loss, ____="validation")
plt.legend()
plt.show()
```

<details><summary>정답</summary>

```python no-run
plt.plot(epochs, val_loss, label="validation")
plt.legend()
plt.show()
```

`plot`의 `label` 인자로 선 이름을 지정하고, `plt.legend()`가 그 라벨들을 범례로 표시합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS (Chart.js 계열) | Python (matplotlib/seaborn) | 비고 |
|----|--------|------|
| `new Chart(ctx, {type:'line'})` | `plt.plot(x, y)` | 선 그래프 |
| `type: 'bar'` + 집계 | `sns.countplot(data, x=...)` | 범주 빈도 |
| 히스토그램 플러그인 | `sns.histplot(data, x=..., bins=...)` | 수치 분포 |
| (대응 없음) | `sns.boxplot(data, x=, y=)` | 사분위·이상치 |
| 히트맵 플러그인 | `sns.heatmap(df.corr(), annot=True)` | 상관관계 |
| 여러 캔버스 | `plt.subplots(행, 열)` | 격자 배치 |
| 데이터셋 `label` | `plt.plot(..., label=...)`+`plt.legend()` | 범례 |
