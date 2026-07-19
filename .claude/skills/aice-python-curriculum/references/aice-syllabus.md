# AICE 시험 범위 참조

> AICE(AI Certification for Everyone)는 KT가 주관하고 한국경제와 공동 운영하는 국내 AI 자격증이다.
> 아래는 공개된 시험 안내 기준의 범위 요약이다. 세부 출제 경향은 회차마다 달라질 수 있으므로,
> 최신 정보가 필요하면 aice.study 공식 사이트를 WebSearch로 확인하고 이 파일을 갱신하라. (확인 필요 항목은 표시)

## 트랙 개요

| 트랙 | 대상 | 도구 | Python 필요도 |
|------|------|------|--------------|
| AICE Future/Junior | 초중고 | 블록코딩 등 | 없음 |
| AICE Basic | 비전공 일반 | AIDU(노코드) | 없음~낮음 |
| **AICE Associate** | 실무자·개발자 (기본 타깃) | Python + Jupyter | **높음** |
| AICE Professional | AI 개발자 | Python | 매우 높음 |

## AICE Associate 실기 범위 (e-book Part 2의 기준)

시험은 실기 코딩형이며, 문항 흐름이 "데이터 분석 파이프라인" 순서를 따른다:

1. **탐색적 데이터 분석 (EDA)** — pandas로 데이터 로드(read_csv), 구조 확인(info, describe, head), 분포 확인
2. **데이터 전처리** — 결측치 처리(isnull, fillna, dropna), 이상치, 타입 변환, 파생 변수, 인코딩(get_dummies, LabelEncoder), 스케일링(StandardScaler, MinMaxScaler)
3. **데이터 분리** — train_test_split
4. **머신러닝 모델링** — sklearn: LinearRegression/LogisticRegression, DecisionTree, RandomForest, (XGBoost/LightGBM 등장 이력 있음 — 확인 필요)
5. **딥러닝 모델링** — TensorFlow/Keras: Sequential, Dense, compile(optimizer/loss/metrics), fit(epochs, batch_size, validation_data), EarlyStopping/ModelCheckpoint
6. **모델 평가** — 분류: accuracy/precision/recall/f1/confusion_matrix, 회귀: MAE/MSE/RMSE/R², 학습곡선 시각화

**시각화**: matplotlib/seaborn — countplot, histplot, heatmap(상관관계), boxplot이 빈출.

## 출제 형태가 문법 학습에 주는 시사점

- 빈 셀에 코드를 채우는 형태이므로 **API 시그니처를 손으로 쓸 수 있어야** 한다 — 자동완성 의존 학습 금지, e-book 연습문제는 빈칸 채우기형 포함 권장
- pandas 체이닝·불리언 인덱싱(`df[df['col'] > 0]`)이 사실상 매 회 등장 — Part 1의 컬렉션/슬라이싱 챕터에서 미리 복선을 깔 것
- 순수 알고리즘 문제(정렬 구현 등)는 출제되지 않음 — 자료구조 심화는 범위 밖
