# Chapter 24. 텍스트 데이터 처리 기초

> **학습 목표**
> - 토큰화·정규화·불용어 제거의 역할을 이해한다.
> - `CountVectorizer`로 텍스트를 단어 빈도 행렬(BoW)로 변환할 수 있다.
> - `TfidfVectorizer`로 단어 중요도를 반영한 특성을 만들 수 있다.
> - 벡터라이저와 분류기를 Pipeline으로 묶어 텍스트 분류를 수행할 수 있다.

머신러닝 모델은 숫자만 먹습니다. 텍스트를 넣으려면 **수치 특성**으로 바꿔야 합니다. 이 장은 그 표준 도구인 `CountVectorizer`·`TfidfVectorizer`를 다루며, 둘 다 sklearn이라 실행 가능합니다. 딥러닝 임베딩만 keras라 `no-run`입니다.

```python
corpus = [
    "Python is great for data science",
    "JavaScript is great for web",
    "Data science uses python and pandas",
    "Web development uses javascript",
]
labels = [1, 0, 1, 0]   # 1 = 데이터과학 글, 0 = 웹 글

tokens = corpus[0].lower().split()   # 가장 단순한 토큰화
print(tokens[:3])
# 출력: ['python', 'is', 'great']
```

## 24.1 토큰화·정규화·불용어

텍스트를 숫자로 바꾸기 전 세 가지를 합니다. **토큰화**(문장을 단어로 쪼개기), **정규화**(대소문자 통일·구두점 제거), **불용어 제거**(`is`, `for`, `the`처럼 의미가 옅은 단어 버리기). 위 `lower().split()`은 토큰화+정규화를 최소한으로 흉내 낸 것이지만, 실무에서는 벡터라이저가 이를 내장 처리합니다.

| JavaScript | Python |
|---|---|
| ```"Hello World".toLowerCase().split(" ")``` | ```"Hello World".lower().split()``` |

## 24.2 CountVectorizer — 단어 빈도 행렬(BoW)

`CountVectorizer`는 말뭉치의 모든 단어로 어휘 사전을 만들고, 각 문서를 "단어별 등장 횟수" 벡터로 바꿉니다. 이 표현을 **BoW(Bag of Words)**라 합니다. JS로 치면 각 문서를 `{단어: 횟수}` 딕셔너리로 만든 뒤 공통 열에 정렬한 것입니다.

```python
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
X_count = cv.fit_transform(corpus)   # (문서 수 × 어휘 수) 희소 행렬
print(X_count.shape[0])
# 출력: 4
```

학습된 어휘는 `vocabulary_`(단어→열 인덱스 딕셔너리)에 담깁니다. `CountVectorizer`는 기본으로 소문자화하므로 `"Python"`도 `"python"`으로 저장됩니다.

```python
print("python" in cv.vocabulary_)
# 출력: True
```

> ⚠️ **함정**: `fit_transform`의 결과는 일반 배열이 아니라 **희소 행렬(sparse matrix)**입니다. 어휘가 수만 개여도 대부분 0이라 메모리를 아끼는 구조입니다. 내용을 눈으로 보려면 `.toarray()`로 밀집 배열로 바꿔야 합니다 — JS 배열처럼 바로 인덱싱되지 않습니다.

`stop_words="english"`를 주면 영어 불용어가 자동 제거됩니다.

```python
cv_sw = CountVectorizer(stop_words="english")
cv_sw.fit(corpus)
print("is" in cv_sw.get_feature_names_out())   # 불용어 'is'는 제거됨
# 출력: False
```

## 24.3 TfidfVectorizer — 단어 중요도 반영

단순 빈도는 흔한 단어를 과대평가합니다. **TF-IDF**는 "한 문서에서 자주 나오되(TF) 전체 문서에서는 드문(IDF)" 단어에 높은 가중치를 줍니다. 즉 그 문서를 **특징짓는** 단어를 부각합니다. 사용법은 `CountVectorizer`와 동일합니다.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(corpus)
print(X_tfidf.shape[0])
# 출력: 4
```

> 🎯 **AICE**: `CountVectorizer`와 `TfidfVectorizer`는 이름만 다르고 `fit_transform`/`get_feature_names_out` 인터페이스가 같습니다. "빈도만 vs 중요도 가중"의 차이와, 둘 다 sklearn 벡터라이저라는 점을 함께 기억하세요.

## 24.4 텍스트 분류 파이프라인

벡터라이저도 estimator이므로 21장의 `Pipeline`에 그대로 들어갑니다. "텍스트 → 벡터화 → 분류기"를 한 객체로 묶으면, 원문 리스트를 바로 `fit`·`predict`할 수 있습니다. 텍스트 분류에는 `MultinomialNB`(나이브 베이즈)가 가볍고 강력합니다.

```python
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

pipe = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", MultinomialNB()),
])
pipe.fit(corpus, labels)
pred = pipe.predict(["python pandas data analysis"])   # 원문을 바로 투입
print(pred[0] in (0, 1))
# 출력: True
```

> ⚠️ **함정**: Pipeline에 벡터라이저를 넣으면, `predict`에 넘기는 것도 **벡터가 아니라 원문 문자열 리스트**입니다. 직접 `fit_transform`으로 벡터를 만든 뒤 그 벡터를 다시 넘기려다 이중 변환하는 실수를 피하세요. Pipeline이 변환을 내부에서 처리합니다.

## 24.5 임베딩 개요

BoW·TF-IDF는 단어를 독립된 열로만 봐서 "python"과 "javascript"의 의미적 유사성을 모릅니다. **임베딩(embedding)**은 단어를 의미가 담긴 밀집 벡터로 학습해 이 한계를 넘습니다. 딥러닝(keras) 영역이라 아래는 `no-run`입니다(23장 참조).

```python no-run
from tensorflow.keras.layers import Embedding

# 희소한 BoW 대신, 단어 인덱스를 64차원 밀집 벡터로 학습
emb = Embedding(input_dim=10000, output_dim=64)   # 어휘 1만, 벡터 64차원
```

> 🎯 **AICE (출제 이력 불확실)**: 임베딩·딥러닝 기반 텍스트 처리는 AICE 공개 범위에 명시가 적어 **출제 여부가 확실하지 않습니다**. 시험 대비 우선순위는 실행 가능한 `CountVectorizer`·`TfidfVectorizer`와 텍스트 분류 파이프라인에 두고, 임베딩은 개념 수준으로 이해해 두면 충분합니다.

## 연습문제

**Q1.** 영어 불용어를 제거하는 TF-IDF 벡터라이저로 말뭉치를 변환하세요.

```python no-run
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer(____="english")
X = vec.____(corpus)
```

<details><summary>정답</summary>

```python no-run
vec = TfidfVectorizer(stop_words="english")
X = vec.fit_transform(corpus)
```

`stop_words="english"`로 불용어를 제거하고 `fit_transform`으로 벡터화합니다.
</details>

**Q2.** TF-IDF 벡터화와 나이브 베이즈 분류기를 Pipeline으로 묶으세요.

```python no-run
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
pipe = Pipeline([
    ("tfidf", ____()),
    ("clf", ____()),
])
pipe.fit(corpus, labels)
```

<details><summary>정답</summary>

```python no-run
pipe = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB()),
])
pipe.fit(corpus, labels)
```

벡터라이저와 분류기를 순서대로 묶으면 원문을 바로 학습할 수 있습니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `str.toLowerCase().split(" ")` | `str.lower().split()` | 토큰화+정규화 |
| `{단어: 횟수}` 딕셔너리 | `CountVectorizer` (BoW) | 단어 빈도 행렬 |
| 가중치 부여 맵 | `TfidfVectorizer` | 흔한 단어 억제, 특징 단어 부각 |
| 조밀 배열 | 희소 행렬 (`.toarray()`로 변환) | 메모리 효율 |
| 변환+분류 합성 | `Pipeline([vectorizer, clf])` | 원문을 바로 fit/predict |
