# QA 정합성 검수 보고서 — ch01~ch24

- 검수자: qa-reviewer (경계면 교차 비교 검수)
- 검수 일시: 2026-07-19
- 검수 전제: code-verifier 실행 검증 전량 PASS(03_verification_report.md). 실행 오류는 QA 범위 외.
- 검수 범위: ch01~ch24. 부록(Appendix A/B/C)은 집필 중이라 범위 제외.
- 검수 항목: (1) 목차↔본문 커버리지 교차 비교 (2) JS 코드 정확성 (3) 용어 일관성 (4) 챕터 템플릿 준수 (5) AICE 정렬 (6) 4인 병렬 집필 이음새.

## 총평

- **CRITICAL 0건 / HIGH 0건.** 출판 블로킹 결함 없음.
- 커버리지: 24개 챕터 전수에서 목차 `개념 목록`의 모든 키워드가 본문에 존재. 누락·임의 추가 없음.
- JS 코드: `javascript` 펜스 3개(ch13/14/15) 및 비교표 내 인라인 JS 전수 확인 — 전부 현대 문법(const/arrow/`??=`). `var`·`function()`·콜백 지옥 오표기 없음. `var` 언급은 ch08의 늦은 바인딩 함정 설명용으로 의도적·정확.
- 용어: `사전`(dict 오용)·`배열`(list 오용) 위반 없음. `배열`은 전부 JS Array 또는 NumPy ndarray 지칭, `사전`은 ch24 "어휘 사전"(lexicon)으로 정당. dict=딕셔너리/list=리스트/tuple=튜플 일관.
- 템플릿: 24개 전부 학습 목표·연습문제(빈칸형+`<details>` 정답)·"한눈에 보기" 요약표 보유.
- MEDIUM은 대부분 Part 경계(집필자 4인)의 이음새 표기 불일치. 조판 전 정리 권장이나 블로킹 아님.

## 심각도별 지적

### CRITICAL
없음.

### HIGH
없음.

### MEDIUM

| 심각도 | 파일 | 위치 | 지적 | 수정 방향 |
|--------|------|------|------|-----------|
| MEDIUM | 전 챕터(이음새) | ch02/03/04/06(`ch05`,`ch13` 등) vs ch13~24(`13장`,`17장` 등) | 챕터 상호참조 표기가 Part 1(집필자 A)은 `chNN`, Part 2·3(집필자 B/C/D)은 `N장`으로 갈림. 4인 병렬 집필의 이음새 불일치. | 하나로 통일. 본문 가독성상 `N장` 권장(제목이 "Chapter NN"이므로 `NN장`이 자연스러움). ch02 L?(`ch04`,`ch15`), ch03(`ch06`), ch04(`ch13`,`ch14`), ch06(`ch05`)를 `N장`으로 치환. |
| MEDIUM | ch13_numpy.md | L176 | `print(centered)` 출력 주석이 `# 출력: [[-1.5 -1.5 -1.5]`로 **1행만 표기·닫는 괄호 누락**. 실제 출력은 2행(`[[-1.5 -1.5 -1.5]` / `[ 1.5  1.5  1.5]]`). 학습자에게 잘못된 출력 노출(검증 스크립트는 통과했으나 표시값이 불완전). | 출력 주석을 실제 2행 전체로 보정: `# 출력: [[-1.5 -1.5 -1.5]\n#        [ 1.5  1.5  1.5]]`. |
| MEDIUM | Part 2·3 다수 (ch13 L124·L188, ch17 L31·L90·L145, ch15 등) | `⚠️ **JS 함정**` 콜아웃 | JS 대응이 없는(목차 "대응 없음") 챕터에서 순수 Python/NumPy/sklearn 함정(`&` vs `and`, 브로드캐스팅 shape, `train_test_split` 반환 순서, RMSE 함수 교체, Classifier/Regressor 구분)을 **`JS 함정`으로 라벨링** — 내용상 JS와 무관해 오도. ch18은 올바르게 `⚠️ **함정**`만 사용(라벨 자체 불일치이기도 함). | JS 무관 함정은 `⚠️ **함정**`(또는 `⚠️ **실전 함정**`)으로 라벨 통일. JS 습관 유래 함정(ch02 truthiness 등)만 `JS 함정` 유지. |
| MEDIUM | ch08_scope_closures.md | 전체(🎯=0) | 유일하게 `🎯 AICE` 콜아웃이 없는 챕터. A중/P중이라 배점은 낮으나 나머지 23개 챕터가 모두 보유 → 템플릿 일관성 이탈. LEGB·`nonlocal`의 실기 등장 맥락(중첩 함수 상태) 한 줄이 비어 있음. | ch08에 `🎯 AICE` 콜아웃 1개 추가(예: 클로저/`nonlocal`이 콜백·카운터 패턴에서 어떻게 쓰이는지, 실기 직접 출제보다 코드 독해용임을 명시). |

### LOW

| 심각도 | 파일 | 위치 | 지적 | 수정 방향 |
|--------|------|------|------|-----------|
| LOW | ch02_variables_types.md | L33-36 비교표 | `a === b` → `a == b`(값 비교)로만 매핑. JS `===`는 **객체/배열에서는 정체성 비교**(`[1,2,3]===[1,2,3]`은 false)라 원시값에만 정확한 대응. 본문·예제(L38-46)가 `is`로 보완하므로 오해 소지는 낮음. | 표 하단 각주로 "객체·배열의 `===`는 정체성 비교라 Python `is`에 해당" 한 줄 보강(선택). |
| LOW | ch18_keras_basics.md | L42 등 | 콜아웃 라벨 `⚠️ **함정**`(JS 무관 Keras 함정). 내용상은 정확하나 MEDIUM의 라벨 통일 결정에 함께 반영 필요. | MEDIUM 라벨 통일안 적용 시 함께 정리. |
| LOW | ch16/ch18 | 말미 섹션 | 종료 섹션명이 다른 챕터의 "한눈에 보기"와 별개로 "마무리" 표현 병용. | 조판 일관성 위해 종료 섹션 명칭 확인(내용 문제 아님, 선택). |
| LOW | ch19~ch24 (Part 3, P상) | 연습문제 수 | P상 핵심 챕터가 연습문제 2개(Part 2 A상은 3개). 빈칸+해답 쌍 구조는 갖춤. 출판 필수는 아니나 Professional 배점 대비 다소 경량. | 여력 시 각 챕터 빈칸형 1문항 추가로 Part 2와 분량 균형(선택, 비블로킹). |

## 챕터별 상태 요약

| 챕터 | 커버리지 | 템플릿 | JS코드 | 상태 |
|------|----------|--------|--------|------|
| ch01 | 완전 | OK | (JS펜스 없음/인라인 OK) | PASS |
| ch02 | 완전 | OK | OK | PASS (LOW: === 각주) |
| ch03 | 완전 | OK | OK | PASS |
| ch04 | 완전 | OK | OK | PASS (MEDIUM: 상호참조 표기) |
| ch05 | 완전 | OK | OK | PASS |
| ch06 | 완전 | OK | OK | PASS (MEDIUM: 상호참조 표기) |
| ch07 | 완전 | OK | OK | PASS |
| ch08 | 완전 | 🎯 누락 | OK | 수정 권장 (MEDIUM: 🎯 추가) |
| ch09 | 완전 | OK | OK | PASS |
| ch10 | 완전 | OK(⚠️ 없음-정당) | OK | PASS |
| ch11 | 완전 | OK | OK | PASS |
| ch12 | 완전 | OK | OK | PASS |
| ch13 | 완전 | OK | OK | 수정 권장 (MEDIUM: L176 출력, 라벨) |
| ch14 | 완전 | OK | OK | PASS |
| ch15 | 완전 | OK | OK | PASS (MEDIUM: 라벨) |
| ch16 | 완전 | OK | (no-run) | PASS |
| ch17 | 완전 | OK | OK(최신 API 정확) | PASS (MEDIUM: 라벨) |
| ch18 | 완전 | OK | (no-run) | PASS (LOW: 라벨) |
| ch19 | 완전 | OK | OK | PASS |
| ch20 | 완전 | OK | (부분 no-run) | PASS |
| ch21 | 완전 | OK | OK | PASS |
| ch22 | 완전 | OK | (부분 no-run) | PASS |
| ch23 | 완전 | OK | (no-run) | PASS |
| ch24 | 완전 | OK | (부분 no-run) | PASS |

> 참조 정확성 표본: ch17→9장(클래스), ch18→17장, ch23→18장/24장, ch24→23장 등 상호참조 대상 챕터 번호 전수 정확. ch23 "100장"은 이미지 100장(개수)으로 챕터 참조 아님(오탐 아님).

## 결론

- 24개 챕터 전부 CRITICAL/HIGH 없이 조판 진입 가능(ebook-builder 착수 조건 충족).
- MEDIUM 4건은 이음새·일관성 정리 항목으로, chapter-writer가 일괄 반영 권장:
  1) 상호참조 표기 `N장`으로 통일(Part 1 4곳),
  2) ch13 L176 출력 주석 2행 보정,
  3) Part 2·3 JS 무관 함정 라벨 `⚠️ 함정`으로 통일,
  4) ch08 `🎯 AICE` 콜아웃 1개 추가.
- LOW는 문체·선택 개선으로 비블로킹.

---

# 부록 QA (appendix A/B/C) — 추가 검수

- 검수 일시: 2026-07-19 (부록 3편 완성분 추가 배정)
- 대상: appendix_a_cheatsheet.md, appendix_b_exam_tips.md, appendix_c_roadmap.md
- 기준: 챕터와 동일 + 부록 특성(치트시트 정합성/시험팁 syllabus 대조/로드맵 의존관계 대조).
- 참조: `.claude/skills/aice-python-curriculum/references/aice-syllabus.md`, `01_curriculum_outline.md`.

## 부록 총평

- **CRITICAL 0 / HIGH 0 / MEDIUM 1 / LOW 2.** 블로킹 결함 없음.
- **치트시트(A)**: 전 항목이 실제 챕터에 존재 — **임의 창작 항목 0건**. 기계 대조로 `SimpleImputer`(ch19), `toLocaleString`/`replaceAll`/`toFixed`(ch03), `feature_importances_`(ch17/19/20), `RandomForest`/`GradientBoosting`(ch20), `cross_val_score`(ch22), `ColumnTransformer`/`best_params_`(ch21), `root_mean_squared_error`(ch17), `Float64Array`(ch13) 전부 근거 챕터 확인. 표 안 스니펫 전부 3줄 이하, 문법 정확(`keras.Input(shape=(특성수,))`, `Pipeline([("prep",...),("clf",...)])`, `GridSearchCV(model, param_grid, cv=5)` 등 최신·정확).
- **시험팁(B)**: syllabus와 트랙 구분 일치 — Associate=ch01~18(딥러닝 Keras 포함), Professional=ch01~24. syllabus의 "Associate 딥러닝=Keras Sequential/Dense/compile/fit/EarlyStopping"과 B.4의 활성화↔loss·콜백 서술 정합. `sparse_categorical` 정수라벨 팁(ch18 근거 존재)도 정확.
- **로드맵(C)**: 의존 화살표가 목차 설계노트와 일치 — `13→14→15→{16,17}`, `17→{18,19,20,22}`, `18→23`, `20→21→24` 전부 정확 재현. C.1 트랙 비교표도 outline AICE 연관도와 정합(앙상블 A중/P필수 등).
- 용어(사전·배열 오용 0), 경어체(3편 모두 plain체 0, 전부 -습니다/-세요), 콜아웃(⚠️/🎯/ℹ️) 일관.

## 부록 심각도별 지적

### CRITICAL / HIGH
없음.

### MEDIUM

| 심각도 | 파일 | 위치 | 지적 | 수정 방향 |
|--------|------|------|------|-----------|
| MEDIUM | appendix_c_roadmap.md | C.2 의존 그래프 L37 | ASCII 의존 그래프가 `18(Keras)`를 **`[Part 3 — Professional]` 행에 배치**. 그러나 ch18은 **Part 2(Associate)** 챕터(outline "Part 2: ch13~18", C.1 "Keras 기본=Associate 필수", 같은 부록 L21 "Part 3(ch19~24)", B.1 "Associate=ch01~18"과 모두 상충). 의존 화살표(17→18→23)는 맞으나 Part 소속 라벨이 틀려 "Keras가 Professional 범위"로 오독될 소지. | ch18을 Part 2 블록으로 옮기거나, 그래프에서 18을 별도 표기하고 "18은 Part 2지만 17에 의존해 같은 깊이에 그림"이라는 주석 추가. 의존 화살표는 유지. |

### LOW

| 심각도 | 파일 | 위치 | 지적 | 수정 방향 |
|--------|------|------|------|-----------|
| LOW | appendix_b_exam_tips.md | B.4/B.5 | syllabus는 RandomForest를 **Associate 모델링 범위**(항목4)로 명시하나, 부록 B는 앙상블을 B.5(Professional)에만 배치. C.1이 앙상블을 "Associate 중"으로 올바르게 표기해 상충은 아니나, B에선 RandomForest의 Associate 등장 가능성이 누락. | B.4(Associate)에 "RandomForest는 Associate에도 등장 이력(확인 필요)" 한 줄 보강(선택). |
| LOW | appendix A/B (전반) | 상호참조 표기 | 부록도 챕터 상호참조를 `chNN`(헤더·표: `(ch01)`,`(ch14~15)`)과 `N장`(A.15/A.16 비고: `23장`,`24장`) 혼용 — 챕터 본문과 동일 이슈. | 챕터 MEDIUM(상호참조 표기 통일)의 최종 표준에 맞춰 부록도 동일하게 정렬. |

## 부록별 상태 요약

| 부록 | 정합성 | 용어/경어체/콜아웃 | 상태 |
|------|--------|-------------------|------|
| A. 치트시트 | 창작 항목 0, 스니펫 3줄↓, 문법 정확 | OK | PASS (LOW: 상호참조 표기) |
| B. 시험 팁 | syllabus·트랙 구분 일치 | OK | PASS (LOW: RandomForest 트랙 표기) |
| C. 로드맵 | 의존 화살표 정확 | OK | 수정 권장 (MEDIUM: C.2 ch18 Part 라벨) |

## 부록 결론

- CRITICAL/HIGH 없음 — 부록 3편 조판 진입 가능.
- MEDIUM 1건(appendix_c C.2 그래프의 ch18 Part-3 오배치)만 chapter-writer(또는 curriculum-architect) 반영 권장. 나머지 LOW 2건은 선택.

---

# ch00 QA (프런트매터) — 경량 검수

- 검수 일시: 2026-07-19 (신규 ch00_about.md 추가 배정)
- 대상: ch00_about.md 1개 + 관련 정합성. 목차 ch00 포함 갱신(총 25챕터) 반영.
- 검수 관점: 프런트매터는 책 전체를 서술 → **사실 오류 시 치명적**이므로 팩트체크 집중. 비교표·연습문제·요약표 부재는 면제 항목이라 지적 대상 아님.

## ch00 총평

- **CRITICAL 0 / HIGH 0 / MEDIUM 0 / LOW 0 — PASS.** 빌드 진입 가능.
- 팩트 전량 실측 대조 통과. 목차 개념 목록 6항목 전부 본문 커버. 부록 C와 역할 분리 준수(경로 그래프 없음). 용어·경어체·상호참조(`N장`) 표준 준수.

## ch00 팩트 검증 결과 (전량 실측 대조)

| 항목 | ch00 본문 | 실측 | 판정 |
|------|-----------|------|------|
| 트랙 범위 | Associate 1~18장 / Professional 1~24장 (0.2, 0.7) | 목차 Part2=13~18, Part3=19~24, 부록 B.1/C 일치 | ✅ 일치 |
| 검증 블록 수 | 본문 실행 가능 Python 블록 **221개** 실행·출력 대조 (0.5) | ch01~24 러너블 `python` 펜스 실측 = **221**(부록 제외). 환경에 numpy/pandas/sklearn/**matplotlib/seaborn/tensorflow 설치 확인** → 시각화·DL 예제 실제 실행 가능 | ✅ 일치 |
| 패키지 3분류 | 필수 numpy/pandas/sklearn · 시각화·DL matplotlib/seaborn/tensorflow(16·18·23장) · 선택 xgboost/lightgbm(20장) (0.6) | 현재 환경: 앞 6개 설치됨, xgboost/lightgbm만 미설치 → 분류·장 매핑 정확 | ✅ 일치 |
| 콜아웃 2종 구분 | JS 함정=JS 습관 오류(주로 Part 1) / 함정=라이브러리 자체(주로 Part 2·3) (0.5) | 실측 Part1 `JS함정 34/함정 0`, Part2 `2/15`, Part3 `2/11` (ch01~24 계 JS함정 38·함정 26) → 설명과 분포 부합 | ✅ 일치 |
| Part 구성 | Part1 1~12 / Part2 13~18 / Part3 19~24, 본문 24장+부록 3 (0.4) | 목차와 완전 일치. ch00은 프런트매터로 "24장" 외 별도 | ✅ 일치 |

## ch00 커버리지 · 역할 분리

- **목차 개념목록 6항목 전부 커버**: 책의 목적(0.1)·AICE 트랙 구분(0.2)·대상 독자(0.3)·책 구성(0.4)·학습 방법/권장 경로(0.7, 상세는 부록 C 위임)·실습 환경(0.6). 누락 0. 추가된 0.5(읽는 방법)는 프런트매터 성격에 부합하는 정당한 확장.
- **부록 C와 역할 분리 준수**: ch00에 경로/의존 그래프 **없음**. 0.7이 "챕터 의존 그래프는 부록 C에 정리"로 명시 위임. 개요·방법론(ch00) ↔ 경로 그래프(C) 분리 정확.
- **용어/경어체/상호참조**: `리스트`(사전·배열 오용 0), 전면 경어체, 상호참조 `1장`/`16·18·23장`/`20장` = `N장` 표준. 모두 준수.

> 참고(정보성, ch00 결함 아님): `03_verification_report.md`는 matplotlib·tensorflow **미설치** 시점 기준(PASS 200)이라 현재 환경(6개 설치·러너블 221)과 어긋난다. ebook-builder/리더가 03 보고서를 참조할 때 최신 수치는 **221**임에 유의(재검증은 code-verifier 소관).

## ch00 결론

- ch00_about.md는 CRITICAL/HIGH/MEDIUM/LOW **0건 — PASS**. 사실 서술 전량 실측 부합, 커버리지 완전, 부록 C 역할 분리·표준 준수. 빌드 진행 가능.
