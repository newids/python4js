# 코드 검증 보고서 — ch01~ch24 독립 전수 검증 (재검증 2회차)

- 검증자: code-verifier (독립 검증, 집필자 자가검증 결과 불신뢰 전수 재실행)
- 최종 검증 일시: 2026-07-19 (재검증 2회차)
- 검증 방식: `code-verification` 스킬의 `scripts/verify_code_blocks.py`로 디렉토리 전체 실행
- **2회차 변경점**: 스크립트가 파일별 격리 서브프로세스(파일당 타임아웃 300초)로 패치됨(matplotlib/sklearn ↔ TensorFlow OpenMP 런타임 충돌 회피). matplotlib·seaborn·tensorflow 설치 후 ch16·ch18·ch22·ch23·ch24의 미설치 기인 no-run 블록이 실행 가능 코드로 전환됨.
- 스크립트 종료 코드: **0 (전체 PASS, FAIL·타임아웃 없음)**

## 검증 환경

| 항목 | 버전 | 비고 |
|------|------|------|
| Python | 3.13.5 | |
| numpy | 2.5.0 | |
| pandas | 3.0.3 | |
| scikit-learn | 1.9.0 | |
| matplotlib | **3.11.1** | 2회차 신규 설치 |
| seaborn | **0.13.2** | 2회차 신규 설치 |
| tensorflow | **2.21.0** | 2회차 신규 설치 |
| xgboost / lightgbm | **미설치** | 여전히 미설치 — 해당 블록은 no-run 유지 |

## 챕터별 집계 (재검증 2회차)

| 챕터 | PASS | FAIL | SKIP | 1회차 대비 |
|------|------|------|------|-----------|
| ch01_environment.md | 6 | 0 | 3 | 동일 |
| ch02_variables_types.md | 9 | 0 | 3 | 동일 |
| ch03_strings.md | 7 | 0 | 2 | 동일 |
| ch04_collections.md | 12 | 0 | 3 | 동일 |
| ch05_control_flow.md | 11 | 0 | 3 | 동일 |
| ch06_comprehensions.md | 9 | 0 | 3 | 동일 |
| ch07_functions.md | 11 | 0 | 3 | 동일 |
| ch08_scope_closures.md | 10 | 0 | 2 | 동일 (행번호만 이동) |
| ch09_classes.md | 8 | 0 | 2 | 동일 |
| ch10_modules.md | 7 | 0 | 4 | 동일 |
| ch11_error_handling.md | 8 | 0 | 2 | 동일 |
| ch12_iterators_generators.md | 8 | 0 | 3 | 동일 |
| ch13_numpy.md | 16 | 0 | 3 | 동일 |
| ch14_pandas_basics.md | 14 | 0 | 3 | 동일 |
| ch15_pandas_preprocessing.md | 13 | 0 | 3 | 동일 |
| **ch16_visualization.md** | **7** | 0 | **6** | **+7 PASS / −7 SKIP** (matplotlib·seaborn 전환) |
| ch17_sklearn_modeling.md | 12 | 0 | 3 | 동일 |
| **ch18_keras_basics.md** | **6** | 0 | **6** | **+6 PASS / −6 SKIP** (tensorflow 전환) |
| ch19_feature_engineering.md | 11 | 0 | 4 | 동일 |
| ch20_ensemble_models.md | 6 | 0 | 6 | 동일 (xgboost/lightgbm 미설치 유지) |
| ch21_tuning_pipeline.md | 7 | 0 | 4 | 동일 |
| **ch22_model_evaluation.md** | **10** | 0 | **4** | **+1 PASS / −1 SKIP** (matplotlib ROC 전환) |
| **ch23_deep_learning_advanced.md** | **6** | 0 | **4** | **+6 PASS / −6 SKIP** (tensorflow CNN 전환) |
| **ch24_text_processing.md** | **7** | 0 | **4** | **+1 PASS / −1 SKIP** (keras Embedding 전환) |
| appendix_b_exam_tips.md | 1 | 0 | 1 | (2회차 신규 스캔) |
| appendix_a_cheatsheet.md | — | — | — | python 블록 없음 |
| appendix_c_roadmap.md | — | — | — | python 블록 없음 |

## 총계 (재검증 2회차)

| 지표 | 2회차 | 1회차 | 증감 |
|------|-------|-------|------|
| 총 블록(ch01~24) | 304 | 304 | — |
| **PASS** (ch01~24) | **221** | 200 | **+21** |
| **SKIP** (ch01~24) | **83** | 104 | **−21** |
| **FAIL** | **0** | 0 | — |
| OUTPUT_MISMATCH | 0 | 0 | — |
| 타임아웃 | 0 | — | — |

> +21 PASS는 전량 전환 챕터의 SKIP→PASS 전환분(ch16 +7, ch18 +6, ch22 +1, ch23 +6, ch24 +1 = 21)이며, 기존 실행 챕터는 회귀 없음(전 챕터 카운트 동일). 부록 포함 전체 스캔 총계는 222 PASS / 0 FAIL / 84 SKIP (306 블록).

## no-run 잔존 블록 분류 (재검증 2회차)

SKIP 잔존 블록을 전 챕터 대상으로 재분류했다. 코디네이터가 제시한 정당 사유 (a) 연습 빈칸/정답, (b) XGBoost/LightGBM(미설치) **외의 no-run 도피는 발견되지 않았다.**

1. **연습 빈칸/정답** (사유 a) — 대다수. 빈칸(`____`) 문제와 그 참고 정답 블록 쌍. 예: ch16 blk8~13(seaborn countplot/heatmap/plot), ch18 blk9~12(compile·EarlyStopping), ch22 blk11~14(cross_val_score·roc_auc), ch23 blk7~10(CNN·EarlyStopping), ch24 blk8~11(TfidfVectorizer·Pipeline). 정답 블록은 연습 섹션 로컬 변수(model, df, corpus 등)에 의존하는 참고용이라 no-run 유지가 타당.
2. **XGBoost/LightGBM 미설치** (사유 b) — ch20 blk7(XGBClassifier), blk8(LGBMClassifier) 2건. 이 환경에 미설치이므로 no-run 유지가 올바름. 설치 시 실행 검증 가능.
3. **참고성 outline** (사유 a/b 외, 부록 한정) — appendix_b blk2: `df.head(); df.info()...` 형태의 AICE 실전 워크플로 개요. 미정의 `df` 참조 의사코드로 실행 불가한 서술용 블록. 핵심 라이브러리 runnable 코드의 회피가 아니라 개념 요약이며, 부록은 코디네이터 지정 범위(ch01~24) 밖. 참고로만 기록.

핵심 라이브러리(numpy/pandas/sklearn/matplotlib/seaborn/tensorflow) 기반 코드 중 부당하게 no-run으로 회피된 블록은 **없음.**

## 임시 파일 확인

검증 후 프로젝트에 생성된 임시 산출물 없음:
- `.keras/.png/.jpg/.h5/.hdf5/.joblib/.pkl/.pb/.model` 전 트리 스캔 결과 **(none)**.
- git status 변경분은 패치된 검증 스크립트, CLAUDE.md, 집필자가 전환한 5개 챕터(ch16·18·22·23·24)뿐 — 검증 실행이 남긴 새 파일 없음.
- matplotlib은 Agg 백엔드+`plt.show()` no-op으로 PNG 미생성, keras 모델 저장(.keras) 블록은 no-run이라 파일 미생성.

## 결론

- **FAIL 0건, OUTPUT_MISMATCH 0건, 타임아웃 0건.** 실행된 221개(부록 포함 222개) 블록 전부 통과.
- 전환 챕터(ch16·18·22·23·24) 예상 결과와 정확히 일치, 나머지 챕터 회귀 없음.
- no-run 잔존은 (a) 연습 빈칸/정답, (b) XGBoost/LightGBM 미설치로 전부 설명됨 — 부당 도피 없음.
- 임시 파일 오염 없음.
- 조치 필요 사항: 없음. (XGBoost/LightGBM까지 실행 검증하려면 설치 후 재검증 요청 가능.)
