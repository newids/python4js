# Python for JavaScript Developers — AICE 대비 e-book

JavaScript에 능숙한 개발자가 **AICE 자격증(Associate·Professional)** 실기를 준비하는 데 필요한 Python을 "JS와의 차이" 중심으로 배우는 e-book입니다.

**📖 웹에서 읽기: https://newids.github.io/python4js/** (단일 페이지 e-book — 검색·오프라인 저장에 유리)

아래 목차에서 챕터를 클릭하면 GitHub에서 마크다운으로 바로 읽을 수 있습니다.

## 이 책의 특징

- 모든 개념을 **JS ↔ Python 나란히 비교**로 설명 — 아는 것은 건너뛰고 차이만 익힙니다
- 본문 예제 코드 **223개 전부 실제 실행 검증** (Python 3.13 · pandas 3.0 · scikit-learn 1.9 · TensorFlow 2.21 기준)
- `⚠️ JS 함정`(JS 습관이 만드는 오류) / `⚠️ 함정`(Python·라이브러리 자체 함정) 콜아웃 구분
- `🎯 AICE` 콜아웃과 **빈칸 채우기형 연습문제**(실기 형식) + 접기 정답

## 목차

### Part 1 — Python 문법: JS 개발자의 눈으로

| | |
|---|---|
| [Chapter 00. 이 책을 읽기 전에](chapters/ch00_about.md) | 개요·학습 대상·학습 방법 |
| [Chapter 01. 개발 환경과 실행 모델](chapters/ch01_environment.md) | node/npm ↔ python/pip/venv |
| [Chapter 02. 변수·타입·연산자](chapters/ch02_variables_types.md) | truthiness 반전, `is None` |
| [Chapter 03. 문자열과 포매팅](chapters/ch03_strings.md) | 템플릿 리터럴 ↔ f-string |
| [Chapter 04. 컬렉션: list·dict·set·tuple](chapters/ch04_collections.md) | Array/Object/Map/Set 대응, 슬라이싱 |
| [Chapter 05. 제어 흐름](chapters/ch05_control_flow.md) | 들여쓰기 블록, enumerate/zip |
| [Chapter 06. 컴프리헨션](chapters/ch06_comprehensions.md) | map/filter의 Python 관용구 |
| [Chapter 07. 함수](chapters/ch07_functions.md) | \*args/\*\*kwargs ↔ rest/spread, 가변 기본값 함정 |
| [Chapter 08. 스코프와 클로저](chapters/ch08_scope_closures.md) | LEGB, 늦은 바인딩 |
| [Chapter 09. 클래스와 객체](chapters/ch09_classes.md) | prototype ↔ class, self, dunder |
| [Chapter 10. 모듈과 패키지](chapters/ch10_modules.md) | ESM ↔ import |
| [Chapter 11. 에러 처리](chapters/ch11_error_handling.md) | try/catch ↔ try/except/else/finally |
| [Chapter 12. 이터레이터와 제너레이터](chapters/ch12_iterators_generators.md) | function\* ↔ yield |

### Part 2 — AICE Associate 실전

| | |
|---|---|
| [Chapter 13. NumPy 기초](chapters/ch13_numpy.md) | 배열 연산·브로드캐스팅 |
| [Chapter 14. Pandas I: Series와 DataFrame](chapters/ch14_pandas_basics.md) | 불리언 인덱싱, loc/iloc |
| [Chapter 15. Pandas II: 전처리](chapters/ch15_pandas_preprocessing.md) | 결측치·groupby·merge (최다 출제) |
| [Chapter 16. 시각화](chapters/ch16_visualization.md) | matplotlib/seaborn 빈출 패턴 |
| [Chapter 17. Scikit-learn 모델링 프로세스](chapters/ch17_sklearn_modeling.md) | split → fit → predict → 평가 |
| [Chapter 18. Keras 딥러닝 기초](chapters/ch18_keras_basics.md) | Sequential·compile·fit |

### Part 3 — AICE Professional 심화

| | |
|---|---|
| [Chapter 19. 고급 전처리와 특성 공학](chapters/ch19_feature_engineering.md) | 인코딩·스케일링·데이터 누수 |
| [Chapter 20. 앙상블 모델](chapters/ch20_ensemble_models.md) | RF·GB·XGBoost·LightGBM |
| [Chapter 21. 하이퍼파라미터 튜닝과 Pipeline](chapters/ch21_tuning_pipeline.md) | GridSearchCV·ColumnTransformer |
| [Chapter 22. 모델 평가 심화와 교차검증](chapters/ch22_model_evaluation.md) | ROC-AUC·cross_val_score |
| [Chapter 23. 딥러닝 심화: CNN·RNN·시계열](chapters/ch23_deep_learning_advanced.md) | Conv2D·LSTM·콜백 |
| [Chapter 24. 텍스트 데이터 처리 기초](chapters/ch24_text_processing.md) | Vectorizer·텍스트 파이프라인 |

### 부록

| | |
|---|---|
| [Appendix A. JS → Python 치트시트](chapters/appendix_a_cheatsheet.md) | 시험 직전 훑기용 대응표 |
| [Appendix B. AICE 실기 팁과 자주 하는 실수](chapters/appendix_b_exam_tips.md) | 트랙별 팁, JS 개발자 습관성 오타 체크리스트 |
| [Appendix C. Associate vs Professional 로드맵](chapters/appendix_c_roadmap.md) | 트랙별 학습 경로와 챕터 의존 그래프 |

## 학습 경로

- **AICE Associate**: 1~18장 (+ 부록)
- **AICE Professional**: 1~24장 전체
- 자세한 트랙별 경로는 [Appendix C](chapters/appendix_c_roadmap.md) 참조

## 실습 환경

Python 3.13 기준. 필수 `numpy` `pandas` `scikit-learn`, 시각화·딥러닝 챕터용 `matplotlib` `seaborn` `tensorflow`, 선택(20장) `xgboost` `lightgbm` — macOS에서 부스팅 라이브러리는 `brew install libomp`가 먼저 필요합니다. 자세한 안내는 [Chapter 00](chapters/ch00_about.md).

## 저장소 구조

이 책은 Claude Code 멀티 에이전트 하네스(목차 설계 → 집필 → 실행 검증 → QA → 조판)로 제작·유지보수됩니다.

```
chapters/    챕터 마크다운 (GitHub 열람용 — _workspace에서 동기화되는 파생 복사본)
docs/        GitHub Pages 배포본 (index.html)
dist/        빌드 산출물 (단일 HTML)
_workspace/  파이프라인 원본: 목차·챕터 원본·검증/QA 보고서
.claude/     에이전트·스킬 정의 (하네스)
```
