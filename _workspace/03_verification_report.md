# 코드 검증 보고서 — ch01~ch24 독립 전수 검증

- 검증자: code-verifier (독립 검증, 집필자 자가검증 결과 불신뢰 전수 재실행)
- 검증 일시: 2026-07-19
- 검증 방식: `code-verification` 스킬의 `scripts/verify_code_blocks.py`로 디렉토리 전체 실행 (블록별 순차 실행 + `# 출력:` 대조)
- 스크립트 종료 코드: **0 (전체 PASS, FAIL 없음)**

## 검증 환경

| 항목 | 버전 |
|------|------|
| Python | 3.13.5 |
| numpy | 2.5.0 |
| pandas | 3.0.3 |
| scikit-learn | 1.9.0 |
| matplotlib | **미설치 (ModuleNotFoundError)** |
| tensorflow / keras | 미설치 |
| xgboost / lightgbm | 미설치 |

> matplotlib·tensorflow·xgboost·lightgbm 미설치는 환경 문제이며, 해당 라이브러리를 쓰는 블록은 모두 `no-run`으로 처리되어 있어 `DEPENDENCY_MISSING` 실패가 발생하지 않았다. 시각화(ch16)·딥러닝(ch18, ch23) 챕터가 전량 no-run인 것은 이 때문이며 정상이다.

## 챕터별 집계

| 챕터 | PASS | FAIL | SKIP | 비고 |
|------|------|------|------|------|
| ch01_environment.md | 6 | 0 | 3 | 블록2 셸명령(venv), 6·8 연습 빈칸 |
| ch02_variables_types.md | 9 | 0 | 3 | 7·9·11 연습 빈칸 |
| ch03_strings.md | 7 | 0 | 2 | 6·8 연습 빈칸 |
| ch04_collections.md | 12 | 0 | 3 | 10·12·14 연습 빈칸 |
| ch05_control_flow.md | 11 | 0 | 3 | 9·11·13 연습 빈칸 |
| ch06_comprehensions.md | 9 | 0 | 3 | 7·9·11 연습 빈칸 |
| ch07_functions.md | 11 | 0 | 3 | 9·11·13 연습 빈칸 |
| ch08_scope_closures.md | 10 | 0 | 2 | 9·11 연습 빈칸 |
| ch09_classes.md | 8 | 0 | 2 | 7·9 연습 빈칸 |
| ch10_modules.md | 7 | 0 | 4 | 6·8·9·10 모듈파일/연습 |
| ch11_error_handling.md | 8 | 0 | 2 | 7·9 연습 빈칸 |
| ch12_iterators_generators.md | 8 | 0 | 3 | 6·8·10 연습 빈칸 |
| ch13_numpy.md | 16 | 0 | 3 | 14·16·18 연습 빈칸 |
| ch14_pandas_basics.md | 14 | 0 | 3 | 12·14·16 연습 빈칸 |
| ch15_pandas_preprocessing.md | 13 | 0 | 3 | 11·13·15 연습 빈칸 |
| ch16_visualization.md | 0 | 0 | 13 | **no-run 챕터 (matplotlib 미설치)** |
| ch17_sklearn_modeling.md | 12 | 0 | 3 | 10·12·14 연습 빈칸 |
| ch18_keras_basics.md | 0 | 0 | 12 | **no-run 챕터 (keras 미설치)** |
| ch19_feature_engineering.md | 11 | 0 | 4 | 12·14 빈칸 + 13·15 해답 |
| ch20_ensemble_models.md | 6 | 0 | 6 | 7·8 xgboost/lightgbm 미설치, 9·11 빈칸 + 10·12 해답 |
| ch21_tuning_pipeline.md | 7 | 0 | 4 | 8·10 빈칸 + 9·11 해답 |
| ch22_model_evaluation.md | 9 | 0 | 5 | 7 matplotlib 미설치, 11·13 빈칸 + 12·14 해답 |
| ch23_deep_learning_advanced.md | 0 | 0 | 10 | **no-run 챕터 (keras 미설치)** |
| ch24_text_processing.md | 6 | 0 | 5 | 7 keras 미설치, 8·10 빈칸 + 9·11 해답 |

## 총계

| 지표 | 값 |
|------|-----|
| 총 블록 | 304 |
| **PASS** | **200** |
| **FAIL** | **0** |
| **SKIP (no-run)** | **104** |
| OUTPUT_MISMATCH | 0 |
| DEPENDENCY_MISSING | 0 |

## 추가 검사 — no-run 남용 여부

SKIP(no-run) 블록 104개를 표본이 아닌 전 챕터 대상으로 유형 분류하여 "실행 가능해야 할 코드가 no-run으로 도피"한 사례를 조사했다. 결과: **남용 사례 없음.** 모든 no-run은 아래 3개 정당 유형에 속한다.

1. **연습문제 빈칸** (`____` 포함) — 문법상 실행 불가. 예: ch02 blk7 `if user ____ None:`, ch20 blk9 `RandomForestClassifier(____=100)`.
2. **연습 해답 블록** — 빈칸 문제 바로 뒤의 완성 코드로, 연습 섹션 로컬 변수(X_train, model, corpus 등)에 의존하는 참고용 정답. 예: ch19 blk13/15, ch20 blk10/12, ch21 blk9/11, ch22 blk12/14, ch24 blk9/11.
3. **미설치 선택 의존성 데모** — 이 환경에 없는 라이브러리 사용 블록. xgboost(ch20 blk7), lightgbm(ch20 blk8), tensorflow/keras(ch24 blk7, ch16·18·23 전량), matplotlib(ch16 전량, ch22 blk7). no-run 처리가 오히려 올바른 선택(설치 시 실행 가능).

추가로 ch01 blk2는 Python이 아닌 셸 명령(venv 생성)이라 no-run이 정확하다.

핵심 라이브러리(numpy/pandas/sklearn) 기반 코드 중 부당하게 no-run으로 회피된 블록은 발견되지 않았다. no-run 비율이 높은 챕터(ch20 6/12, ch22 5/14, ch24 5/11)도 위 3개 유형으로 전부 설명된다.

## 결론

- **FAIL 0건, OUTPUT_MISMATCH 0건.** 실행된 200개 블록 전부 통과, 본문 `# 출력:` 주석과 실제 출력도 일치.
- no-run 남용 없음 — SKIP 104건 모두 연습 빈칸·해답·미설치 의존성으로 정당.
- 조치 필요 사항: 없음. (matplotlib/tensorflow/xgboost/lightgbm 미설치는 의도된 no-run 처리로 흡수됨 — 리더가 이 라이브러리 사용 챕터를 실제 실행 검증까지 원하면 설치 후 재검증 요청 가능.)
