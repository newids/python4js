---
name: aice-python-curriculum
description: "AICE 자격증 대비 Python e-book 커리큘럼 설계 스킬. e-book 목차 설계, 챕터 구성, 학습 로드맵, AICE 시험 범위 확인, JS 개발자용 Python 학습 순서를 다룰 때 반드시 사용. '목차 만들어줘', '커리큘럼 수정', '챕터 추가/삭제/순서 변경' 요청 시에도 사용."
---

# AICE Python Curriculum — 커리큘럼 설계 스킬

JS 숙련 개발자가 AICE 자격증 실기를 통과하기 위한 Python e-book의 목차를 설계하는 방법.

## 설계 원리

**왜 "JS 대응" 축이 필요한가:** 시니어 개발자는 개념을 처음 배우는 게 아니라 이미 아는 개념의 새 표기법을 배운다. 모든 챕터를 "JS의 X는 Python의 Y"로 정렬하면 학습 전이가 일어나 습득 속도가 수 배 빨라진다. 반대로 JS 대응이 없는 Python 고유 개념(컴프리헨션, 슬라이싱, pandas)은 별도로 표시해 더 많은 분량을 배정한다.

**왜 "AICE 연관도" 축이 필요한가:** 목표는 교양이 아니라 자격증 합격이다. AICE Associate 실기는 pandas 데이터 전처리와 sklearn/keras 모델링이 배점의 대부분을 차지한다. 연관도 '상' 개념에 분량과 연습문제를 집중 배정해야 한다. 시험 범위는 `references/aice-syllabus.md` 참조.

## 목차 산출물 형식

`_workspace/01_curriculum_outline.md`에 다음 구조로 작성한다:

```markdown
# {책 제목}
> 대상 독자 / 목표 / 총 챕터 수 / 예상 학습 시간

## Part 1: Python 문법 — JS 개발자의 눈으로
| 챕터 | 제목 | 학습 목표 | 개념 목록 | JS 대응 | AICE 연관도 | 선수 챕터 |
|------|------|----------|----------|---------|------------|----------|
| 01 | ... | ... | ... | ... | 상/중/하 | - |

## Part 2: AICE 실전 — 데이터 핸들링과 모델링
(동일 표 구조)

## Appendix
(치트시트, 시험 팁 등)
```

## 기본 목차 골격 (출발점)

아래는 검증된 출발점이다. 그대로 복사하지 말고 사용자 요구에 맞게 조정하라. 상세 개념 매핑은 `references/js-python-mapping.md` 참조.

**Part 1 — Python 문법 (JS 대응 중심):**
1. 개발 환경과 실행 모델 (node/npm ↔ python/pip/venv, REPL)
2. 변수·타입·연산자 (동적 타이핑 공통점, `===` 부재, 정수 나눗셈, truthiness 차이)
3. 문자열과 포매팅 (템플릿 리터럴 ↔ f-string, 문자열 메서드 대응)
4. 컬렉션 (Array↔list, Object/Map↔dict, Set↔set, tuple 신개념, 슬라이싱)
5. 제어 흐름 (들여쓰기 블록, `for...of`↔`for in`, enumerate/zip, 삼항 표현식 어순)
6. 컴프리헨션 (map/filter/reduce ↔ comprehension — Python 고유 관용구, 분량 증대)
7. 함수 (화살표 함수↔lambda 제약, 기본값·키워드 인자, *args/**kwargs ↔ spread/rest)
8. 스코프와 클로저 (렉시컬 스코프 공통점, LEGB, global/nonlocal 함정)
9. 클래스와 객체 (prototype↔class, this↔self, dunder 메서드, 상속)
10. 모듈과 패키지 (ESM import↔Python import, `__name__ == "__main__"`)
11. 에러 처리 (try/catch↔try/except/else/finally, 예외 계층)
12. 이터레이터·제너레이터 (Symbol.iterator↔iter/next, function*↔yield)

**Part 2 — AICE 실전 (연관도 전부 '상'):**
13. NumPy 기초 (배열 연산, 브로드캐스팅 — JS에 대응 없음)
14. Pandas I: Series와 DataFrame (JSON 배열 다루기와의 대응)
15. Pandas II: 전처리 (결측치, groupby, merge — AICE 최다 출제 영역)
16. 시각화 (matplotlib/seaborn 핵심 패턴)
17. Scikit-learn 모델링 프로세스 (train_test_split → fit → predict → 평가)
18. Keras 딥러닝 기초 (Sequential 모델, 컴파일·학습·평가)

**Appendix:** A. JS→Python 치트시트 / B. AICE 시험 팁과 자주 하는 실수

## 조정 규칙

- 사용자가 시험 트랙을 명시하면(Basic/Associate/Professional) `references/aice-syllabus.md`의 트랙별 범위로 Part 2를 조정한다. 명시가 없으면 **Associate**를 기본으로 한다.
- 챕터 하나의 개념 목록이 7개를 넘으면 분할한다 — 학습 시간 30~60분 상한의 근거.
- async/await 챕터는 AICE 연관도 '하'이므로 기본 목차에서 제외했다. 사용자가 실무 활용까지 원하면 Part 1 말미에 추가한다.
