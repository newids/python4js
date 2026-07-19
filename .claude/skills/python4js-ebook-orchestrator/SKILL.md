---
name: python4js-ebook-orchestrator
description: "JS 개발자용 AICE 대비 Python e-book 에이전트 팀을 조율하는 오케스트레이터. 'e-book 만들어줘', '책 생성', 'Python 교재 만들어줘', 'AICE 교재' 등 초기 생성 요청 시 반드시 사용. 후속 작업에도 반드시 사용: e-book 다시 실행/재실행/업데이트/수정/보완, '챕터만 다시 써줘', '목차 수정', '코드 재검증', 'QA 다시', '재빌드', '이전 결과 개선', 챕터 추가/삭제 요청."
---

# Python4JS E-book Orchestrator

JS 숙련 개발자의 AICE 자격증 대비 Python 문법 e-book을 에이전트 팀으로 생성하는 통합 스킬.

## 실행 모드: 에이전트 팀

파이프라인 + 생성-검증 복합 패턴. 집필자↔검증자↔QA 간 SendMessage 실시간 피드백이 재작업을 최소화하므로 팀 모드를 사용한다.

## 에이전트 구성

| 팀원 | 에이전트 타입 | 역할 | 스킬 | 출력 |
|------|-------------|------|------|------|
| curriculum-architect | curriculum-architect | 목차 설계 | aice-python-curriculum | `_workspace/01_curriculum_outline.md` |
| chapter-writer | chapter-writer | 챕터 집필 | chapter-authoring | `_workspace/02_chapters/ch{NN}_{slug}.md` |
| code-verifier | code-verifier (general-purpose급 도구 필요 — 스크립트 실행) | 코드 실행 검증 | code-verification | `_workspace/03_verification_report.md` |
| qa-reviewer | qa-reviewer (general-purpose급 도구 필요) | 정합성 QA | (경계면 교차 비교 — 에이전트 정의 내 인라인) | `_workspace/04_qa_report.md` |
| ebook-builder | ebook-builder | HTML 조판 | ebook-building | `dist/python4js-ebook.html` |

모든 Agent/TeamCreate 호출에 `model: "opus"`를 명시한다.

## 워크플로우

### Phase 0: 컨텍스트 확인 (후속 작업 지원)

1. `_workspace/` 존재 여부 확인
2. 실행 모드 결정:
   - **미존재** → 초기 실행. Phase 1로
   - **존재 + 부분 수정 요청** (예: "ch05만 다시", "재검증", "재빌드") → **부분 재실행**. 해당 에이전트만 재호출. 요청 범위에 따라 하류 단계 연쇄 실행: 챕터 수정 → 검증 → QA → 재빌드 / 목차 수정 → 영향 챕터 재집필부터 전체 연쇄
   - **존재 + 새 입력** (다른 시험 트랙, 다른 독자층) → **새 실행**. 기존 `_workspace/`를 `_workspace_{YYYYMMDD_HHMMSS}/`로 이동 후 Phase 1로
3. 부분 재실행 시 이전 산출물 경로와 사용자 피드백을 에이전트 프롬프트에 포함한다

### Phase 1: 준비

1. 사용자 요구 분석 — 시험 트랙(기본: Associate), 분량 선호, 추가 주제 여부
2. `_workspace/`, `_workspace/02_chapters/` 생성, 사용자 요구를 `_workspace/00_input/requirements.md`에 저장

### Phase 2: 팀 구성

```
TeamCreate(
  team_name: "python4js-ebook-team",
  members: [
    { name: "curriculum-architect", agent_type: "curriculum-architect", model: "opus" },
    { name: "chapter-writer",       agent_type: "chapter-writer",       model: "opus" },
    { name: "code-verifier",        agent_type: "code-verifier",        model: "opus" },
    { name: "qa-reviewer",          agent_type: "qa-reviewer",          model: "opus" },
    { name: "ebook-builder",        agent_type: "ebook-builder",        model: "opus" }
  ]
)
```

TaskCreate로 작업 등록 (의존성 명시):

| 작업 | 담당 | depends_on |
|------|------|-----------|
| 커리큘럼 설계 | curriculum-architect | - |
| ch01~chNN 집필 (챕터당 1작업) | chapter-writer | 커리큘럼 설계 |
| ch{NN} 검증 (챕터당 1작업) | code-verifier | 해당 챕터 집필 |
| ch{NN} QA (챕터당 1작업) | qa-reviewer | 해당 챕터 검증 |
| 최종 빌드 | ebook-builder | 전체 QA |

> 챕터가 많으면(15+) 집필 작업을 Part 단위 배치로 묶어 팀원당 작업 수를 5~6개 이내로 유지한다.

### Phase 3: 파이프라인 실행 (팀원 자체 조율)

핵심 흐름 — **점진 검증 파이프라인**:

```
[curriculum-architect] → 목차 확정 공지
        ↓
[chapter-writer] ch01 완성 ──"검증 요청"──→ [code-verifier]
        ↑                                        │ PASS → [qa-reviewer]
        └────── 실패 블록·QA 지적 반려 ←──────────┘
(writer는 다음 챕터를 병행 진행 — 반려 수정은 우선 처리)
```

- 통신 규칙은 각 에이전트 정의의 "팀 통신 프로토콜" 섹션을 따른다
- 리더는 TaskGet으로 진행률을 모니터링하고, 반려 2회 순환 시 개입한다
- 초반 3개 챕터의 검증·QA 결과에서 **반복 결함 패턴**이 보이면 리더가 chapter-writer에게 패턴을 공지해 이후 챕터에 선반영시킨다 (결함 복제 방지)

### Phase 4: 최종 빌드

1. 전 챕터 QA 통과 확인 (`04_qa_report.md`에 OPEN CRITICAL/HIGH 없음)
2. ebook-builder가 `dist/python4js-ebook.html` 생성, 자체 점검 결과 보고

### Phase 5: 정리

1. 팀원 종료 요청(SendMessage) 후 TeamDelete
2. `_workspace/` 보존 (감사 추적·후속 부분 재실행용)
3. 사용자 보고: 산출물 경로, 챕터 수, 검증 통계(PASS/FAIL 이력), 미해결 LOW/MEDIUM 지적 요약
4. 피드백 기회 제공: "개선할 부분이 있나요?" — 피드백은 CLAUDE.md 변경 이력 및 해당 스킬/에이전트에 반영

## 데이터 전달 프로토콜

태스크 기반(조율) + 파일 기반(산출물) + 메시지 기반(반려·통과 신호). 파일명 컨벤션: `{phase}_{artifact}.md`, 챕터는 `02_chapters/ch{NN}_{slug}.md`. 최종 산출물만 `dist/`에.

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| 팀원 1명 중지 | SendMessage로 상태 확인 → 재시작. 재실패 시 대체 팀원 생성 |
| 코드 블록 3회 연속 실패 | 리더가 예제 단순화를 지시, 그래도 실패 시 해당 예제 no-run 전환 + 보고서에 명시 |
| DEPENDENCY_MISSING | 리더가 사용자에게 패키지 설치 여부 확인 (임의 설치 금지). 미설치 결정 시 해당 블록 no-run 전환 + 챕터에 설치 안내 추가 |
| writer↔verifier 무한 반려 | 2회 순환 후 리더 개입, 상충 시 출처 병기하고 삭제하지 않음 |
| 과반 실패 | 사용자에게 알리고 진행 여부 확인 |
| 타임아웃 | 완료된 챕터만으로 부분 빌드, 미완 챕터를 보고서에 명시 |

## 테스트 시나리오

### 정상 흐름
1. 사용자: "AICE Associate 대비 e-book 만들어줘"
2. Phase 1: 요구 저장 → Phase 2: 5인 팀 + 챕터별 작업 등록
3. Phase 3: 목차 18챕터 확정 → 챕터별 집필→검증→QA 점진 파이프라인
4. Phase 4: `dist/python4js-ebook.html` 생성 (목차 링크 전수 유효)
5. Phase 5: 팀 정리, 통계 보고
6. 예상 결과: 단일 HTML e-book + `_workspace/` 4종 산출물

### 에러 흐름
1. Phase 3에서 ch14(pandas) 검증 중 `DEPENDENCY_MISSING: pandas`
2. code-verifier → 리더 보고 → 리더가 사용자에게 설치 여부 확인
3. 설치 승인 시 재검증 진행 / 거부 시 Part 2 코드 블록 no-run 전환 + 챕터 서두에 설치 안내 삽입
4. 최종 보고서에 "Part 2 코드는 실행 검증 생략됨" 명시
