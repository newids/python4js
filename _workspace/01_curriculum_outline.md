# Python for JS Developers — AICE Associate & Professional 대비

> **대상 독자**: JavaScript 숙련(시니어) 개발자. JS 개념 자체는 이미 안다는 전제하에, "Python은 어떻게 다른가"에만 지면을 쓴다.
> **목표**: AICE **Associate + Professional** 두 트랙 실기를 최단 경로로 통과할 수 있는 Python 문법·데이터 핸들링·ML/DL 역량 습득.
> **총 챕터 수**: 24개 (Part 1: 12 / Part 2: 6 / Part 3: 6) + Appendix 3개
> **예상 학습 시간**: 약 16~20시간 (챕터당 30~60분 기준)
> **산출물**: `dist/python4js-ebook.html` (단일 자기완결형 HTML)

## 범례
- **AICE 연관도**: 트랙별로 표기. `A`=Associate, `P`=Professional. 각 트랙에 대해 상/중/하.
  - 예: `A상 / P상` = 두 트랙 모두 배점 핵심. `A하 / P상` = Associate엔 거의 안 나오나 Professional 핵심.
- **비고 `[no-run 챕터]`**: 코드 실행 검증 환경(numpy·pandas·scikit-learn만 설치, Python 3.13)에 미설치된 패키지(matplotlib·seaborn·tensorflow/keras·xgboost·lightgbm)를 다루는 챕터. 집필자는 해당 코드 펜스를 no-run으로 작성한다.
- **`(확인 필요)`**: AICE 공식 공개 범위가 제한적이라 회차별 편차가 있을 수 있는 항목. 특히 Professional 상세 출제 범위는 공개 정보가 적어 references/aice-syllabus.md 기준 + 일반적 AI 개발 실기 관례로 추정 설계했다.

---

## Part 1: Python 문법 — JS 개발자의 눈으로

> JS 대응이 명확한 개념은 빠르게 통과하고, Python 고유 관용구(컴프리헨션·슬라이싱·언패킹)와 JS 습관이 역효과를 내는 함정(truthiness·가변 기본값·늦은 바인딩)에 분량을 집중한다. Part 2·3의 pandas/sklearn 코드를 읽고 쓰기 위한 최소 문법 토대.

| 번호 | 제목 | 학습 목표 | 개념 목록 | JS 대응 | AICE 연관도 | 선수 챕터 | 비고 (슬러그) |
|------|------|----------|----------|---------|------------|----------|------|
| 01 | 개발 환경과 실행 모델 | Python 실행/패키지 생태계를 node 경험에 매핑하고 Jupyter 셀 실행 모델을 이해한다 | python/pip/venv, REPL, Jupyter 노트북 셀 실행, import 경로, 스크립트 vs 모듈 | node/npm/nvm, REPL, package.json | A상 / P상 | - | AICE는 Jupyter 환경 실기. (ch01_environment) |
| 02 | 변수·타입·연산자 | 동적 타이핑 공통점을 확인하고 `==`/`is`·나눗셈·truthiness 차이를 체득한다 | 동적 타이핑, 할당(상수 관례), `==` vs `is`, `is None`, `/` vs `//`, truthiness 차이 | let/const, `===`, `==null`, `/` | A상 / P상 | 01 | ⚠️ truthiness·`is None` JS 함정 집중. (ch02_variables_types) |
| 03 | 문자열과 포매팅 | f-string과 주요 문자열 메서드를 JS 대응으로 습득한다 | f-string(포맷 스펙 `:.2f`), 문자열 메서드(split/join/strip/replace), 슬라이싱 맛보기 | 템플릿 리터럴, String 메서드 | A중 / P중 | 02 | (ch03_strings) |
| 04 | 컬렉션: list·dict·set·tuple | 4대 컬렉션과 슬라이싱을 익혀 pandas 인덱싱의 토대를 만든다 | list, dict, set, tuple(신개념), 슬라이싱 `[start:stop:step]`·`[::-1]`, `in` 멤버십 | Array, Object/Map, Set, 구조분해 | A상 / P상 | 02 | 슬라이싱=pandas 선수 지식, 분량 증대. (ch04_collections) |
| 05 | 제어 흐름 | 들여쓰기 블록과 Python식 순회(enumerate/zip)를 익힌다 | 들여쓰기 블록, `for in`, range, enumerate, zip, 삼항 표현식 어순, `while` | for...of, 삼항 `?:` | A상 / P상 | 04 | ⚠️ 삼항 어순·블록 스코프 없음. (ch05_control_flow) |
| 06 | 컴프리헨션 | map/filter를 대체하는 Python 고유 관용구를 자유자재로 쓴다 | 리스트 컴프리헨션, 조건부 컴프리헨션, dict/set 컴프리헨션, 제너레이터 표현식, 중첩 | `arr.filter().map()` | A상 / P상 | 05 | Python 고유, 분량 증대. pandas 벡터화 사고 복선. (ch06_comprehensions) |
| 07 | 함수 | 인자 체계(기본값·키워드·가변)와 lambda 제약을 이해한다 | def, 기본 인자, 키워드 인자, `*args`/`**kwargs`, lambda 제약, 가변 기본값 함정 | 화살표 함수, spread/rest, 기본 매개변수 | A상 / P상 | 05 | ⚠️ 가변 기본값 `def f(x=[])` 공유 함정. (ch07_functions) |
| 08 | 스코프와 클로저 | LEGB 규칙과 늦은 바인딩 함정을 이해한다 | 함수 스코프, LEGB, `global`/`nonlocal`, 클로저, 루프 늦은 바인딩 | 렉시컬/블록 스코프, 클로저 | A중 / P중 | 07 | ⚠️ 루프 클로저 `lambda x=x:` 트릭. (ch08_scope_closures) |
| 09 | 클래스와 객체 | `self`·dunder·상속을 익혀 sklearn/keras 객체 코드를 읽는다 | class, `__init__`, `self`, 인스턴스/클래스 속성, dunder(`__repr__`/`__len__`), 상속 | prototype/class, this, 연산자 | A중 / P중 | 07 | ⚠️ `self` 명시 누락 최다 에러. estimator 객체 이해 토대. (ch09_classes) |
| 10 | 모듈과 패키지 | import 어순과 `__main__` 관용구, as 별칭을 익힌다 | from-import 어순, `import ... as`, 표준 라이브러리, `if __name__ == "__main__"` | ESM import/export | A중 / P중 | 01 | `import pandas as pd` 관례 토대. (ch10_modules) |
| 11 | 에러 처리 | try/except/else/finally와 예외 계층을 익힌다 | try/except, 예외 타입 명시, else/finally, raise, 예외 계층 | try/catch/finally, throw | A하 / P중 | 05 | (ch11_error_handling) |
| 12 | 이터레이터·제너레이터 | iter/next와 yield로 지연 평가를 이해한다 | iterable vs iterator, iter/next, `yield`, 제너레이터 함수, 지연 평가 | Symbol.iterator, `function*` | A하 / P중 | 06 | Professional 대용량 데이터 처리 복선. (ch12_iterators_generators) |

---

## Part 2: AICE Associate 실전 — 데이터 핸들링과 모델링

> AICE Associate 실기는 "EDA → 전처리 → 분리 → 모델링 → 평가" 파이프라인을 빈칸 채우기형으로 출제한다. API 시그니처를 손으로 쓸 수 있어야 하므로, 이 파트의 모든 챕터는 연관도 A상이며 빈칸 채우기형 연습문제를 포함한다. JS 대응이 없는 벡터화 사고방식이 최대 전환점.

| 번호 | 제목 | 학습 목표 | 개념 목록 | JS 대응 | AICE 연관도 | 선수 챕터 | 비고 (슬러그) |
|------|------|----------|----------|---------|------------|----------|------|
| 13 | NumPy 기초 | ndarray·벡터화·브로드캐스팅으로 벡터화 사고를 획득한다 | ndarray 생성, dtype·shape, 인덱싱/슬라이싱, 벡터화 연산, 브로드캐스팅, 축(axis) 집계 | (대응 없음) TypedArray 유사 | A상 / P상 | 04, 06 | pandas·sklearn의 토대. (ch13_numpy) |
| 14 | Pandas I: Series와 DataFrame | 데이터 로드와 구조 확인(EDA 1단계)을 수행한다 | Series/DataFrame, read_csv, head/info/describe, 열·행 선택(loc/iloc), 불리언 인덱싱 | JSON 배열/객체 다루기 | A상 / P상 | 13 | ⚠️ 불리언 인덱싱 `df[df.col>0]` 핵심 전환점. (ch14_pandas_basics) |
| 15 | Pandas II: 전처리 | 결측치·인코딩·스케일링으로 모델 입력 데이터를 만든다 | 결측치(isnull/fillna/dropna), 타입 변환, 파생 변수, groupby, merge, 인코딩(get_dummies/LabelEncoder), 스케일링(StandardScaler/MinMaxScaler) | (대응 없음) | A상 / P상 | 14 | AICE 최다 출제 영역. 개념 7개 상한 근접—집필 시 스케일링을 예제로 압축. (ch15_pandas_preprocessing) |
| 16 | 시각화 | EDA용 핵심 플롯을 그려 분포·상관을 읽는다 | matplotlib 기본, seaborn countplot/histplot, boxplot, 상관 heatmap, 학습곡선 플롯 | (대응 없음) Chart.js 유사 | A중 / P하 | 14 | **[no-run 챕터]** matplotlib·seaborn 미설치. (ch16_visualization) |
| 17 | Scikit-learn 모델링 프로세스 | fit/predict 일관 인터페이스로 회귀·분류 모델을 학습·평가한다 | train_test_split, estimator API(fit/predict), LinearRegression/LogisticRegression, DecisionTree, 평가지표(accuracy/f1/confusion_matrix, MAE/RMSE/R²) | (대응 없음) | A상 / P상 | 15 | 회귀+분류 평가지표 함께. estimator 객체=ch09 연결. (ch17_sklearn_modeling) |
| 18 | Keras 딥러닝 기초 | Sequential 모델을 구성·컴파일·학습·평가한다 | Sequential, Dense, 활성화 함수, compile(optimizer/loss/metrics), fit(epochs/batch_size/validation), EarlyStopping/ModelCheckpoint, evaluate | (대응 없음) | A상 / P상 | 17 | **[no-run 챕터]** tensorflow/keras 미설치. (ch18_keras_basics) |

---

## Part 3: AICE Professional 심화 — 고급 ML·딥러닝

> **Professional은 AI 개발자 대상 실기로 코딩 비중이 매우 높다.** 공개 상세 범위가 제한적이므로(references/aice-syllabus.md 기준 + AI 개발 실기 관례로 추정), 아래 주제군을 기본으로 하되 회차 편차 가능 항목은 `(확인 필요)`로 표시했다. Part 2의 파이프라인을 심화·자동화하는 관점으로 구성. 각 챕터 개념 7개 이하 준수.

| 번호 | 제목 | 학습 목표 | 개념 목록 | JS 대응 | AICE 연관도 | 선수 챕터 | 비고 (슬러그) |
|------|------|----------|----------|---------|------------|----------|------|
| 19 | 고급 전처리와 특성 공학 | 특성 생성·선택·변환으로 모델 성능을 끌어올린다 | 특성 생성(파생·상호작용), 범주형 고급 인코딩, 스케일링 심화, 결측·이상치 전략, 특성 선택, 불균형 데이터 개요(확인 필요) | (대응 없음) | A중 / P상 | 15 | numpy·pandas·sklearn만 사용—실행 가능. (ch19_feature_engineering) |
| 20 | 앙상블 모델 | 배깅·부스팅 원리와 대표 앙상블 API를 익힌다 | 앙상블 개념(배깅/부스팅), RandomForest, GradientBoosting, XGBoost, LightGBM, 특성 중요도 | (대응 없음) | A중 / P상 | 17 | **[no-run 챕터]** RandomForest/GradientBoosting은 sklearn(실행 가능)이나 XGBoost·LightGBM 미설치—해당 펜스는 no-run 처리. (ch20_ensemble_models) |
| 21 | 하이퍼파라미터 튜닝과 Pipeline | GridSearchCV·Pipeline으로 튜닝을 자동화·누수 없이 구성한다 | 하이퍼파라미터 개념, GridSearchCV, RandomizedSearchCV, sklearn Pipeline, ColumnTransformer, 데이터 누수 방지 | (대응 없음) | A하 / P상 | 20 | sklearn만 사용—실행 가능. (ch21_tuning_pipeline) |
| 22 | 모델 평가 심화와 교차검증 | 교차검증·ROC-AUC로 일반화 성능을 정밀 평가한다 | K-Fold 교차검증, cross_val_score, ROC 곡선·AUC, precision-recall 트레이드오프, 임계값 조정, 다중분류 평가(확인 필요) | (대응 없음) | A중 / P상 | 17 | sklearn 계산은 실행 가능. ROC 곡선 **플롯**은 matplotlib 미설치로 해당 펜스만 no-run. (ch22_model_evaluation) |
| 23 | 딥러닝 심화: CNN·RNN·시계열 | 이미지·시퀀스·시계열용 신경망 구조를 이해·구성한다 | CNN(Conv2D/Pooling), 이미지 데이터 개요, RNN/LSTM, 시퀀스 처리, 시계열 데이터 준비(window), 콜백 활용 | (대응 없음) | A하 / P상 | 18 | **[no-run 챕터]** tensorflow/keras 미설치. 상세 출제 비중 (확인 필요). (ch23_deep_learning_advanced) |
| 24 | 텍스트 데이터 처리 기초 | 텍스트를 수치 특성으로 변환해 모델에 투입한다 | 토큰화·정규화, 불용어, CountVectorizer, TfidfVectorizer, 텍스트 분류 파이프라인, 임베딩 개요(확인 필요) | (대응 없음) | A하 / P중 | 21 | CountVectorizer/TfidfVectorizer는 sklearn(실행 가능). 임베딩(keras) 언급 부분만 no-run. (ch24_text_processing) |

---

## Appendix

| 부록 | 제목 | 내용 | 슬러그 |
|------|------|------|--------|
| A | JS → Python 치트시트 | 직접 대응·함정·Python 고유 관용구 한눈에 보는 대조표 (references/js-python-mapping.md 기반) | appendix_a_cheatsheet |
| B | AICE 실기 팁과 자주 하는 실수 | 빈칸 채우기 대비 API 시그니처 암기 전략, Jupyter 실기 팁, JS 습관성 오타 목록, 트랙별 시간 배분 | appendix_b_exam_tips |
| C | Associate vs Professional 로드맵 | 두 트랙 범위 비교표, 챕터 의존 그래프, 추천 학습 순서(트랙별 최단 경로) | appendix_c_roadmap |

---

## 설계 노트 (집필자·QA 참조)

- **집필 순서(의존 그래프)**: Part 1(01→12)은 대체로 선형. Part 2·3는 `13(NumPy) → 14 → 15 → {16, 17}`, `17 → {18, 19, 20, 22}`, `20 → 21 → 24`, `18 → 23` 순. NumPy(13)와 Pandas(14, 15)를 먼저 확정해야 하위 챕터 예제가 안정된다.
- **개념 7개 상한**: ch15(전처리)와 ch22가 상한에 근접. ch15는 스케일링 2종을 하나의 예제로 묶어 실질 6개로 운용, ch22는 다중분류 평가를 개요 수준으로 축약 권장.
- **no-run 챕터 총 4개**: ch16, ch18, ch23(전체) + ch20·ch22·ch24(부분). code-verifier는 이 챕터들의 no-run 표기를 신뢰하고 실행 검증 대상에서 제외한다.
- **`(확인 필요)` 항목**: Professional 상세 범위(ch19 불균형 데이터, ch22 다중분류, ch23 출제 비중, ch24 임베딩), Associate의 XGBoost/LightGBM 출제 이력(ch20). AICE 공식 사이트 최신 확인 시 갱신.
- **트랙별 최단 경로**: Associate만 목표면 Part 1 + Part 2(ch13~18)로 충분. Professional은 Part 3 전체 추가 이수. 상세 로드맵은 Appendix C.
