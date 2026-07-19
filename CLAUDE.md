# python4js

## 하네스: JS 개발자용 AICE 대비 Python e-book 생성

**목표:** JavaScript 숙련 개발자가 AICE 자격증(기본: Associate)을 준비하는 데 필요한 Python 문법 e-book을 에이전트 팀으로 생성·유지보수한다.

**트리거:** e-book 생성·수정·재실행, 목차/챕터/코드 검증/QA/빌드 관련 작업 요청 시 `python4js-ebook-orchestrator` 스킬을 사용하라. 단순 질문(Python 문법 질문 등)은 직접 응답 가능.

**배포:** https://newids.github.io/python4js/ — GitHub `newids/python4js`, Pages는 `main:/docs` 서빙. 재빌드 시 `dist/python4js-ebook.html` → `docs/index.html` 복사 후 푸시 필요 (ebook-building 스킬의 배포 섹션 참조).

**변경 이력:**
| 날짜 | 변경 내용 | 대상 | 사유 |
|------|----------|------|------|
| 2026-07-19 | 초기 구성 (에이전트 5, 스킬 5) | 전체 | - |
| 2026-07-19 | 빌드 스크립트가 `appendix*.md`도 챕터 뒤에 포함하도록 패치 | skills/ebook-building | 부록 3편이 `ch*.md` glob에 안 잡히는 결함 발견 |
| 2026-07-19 | 1차 e-book 생성 실행 완료 (24챕터+부록 3, Associate+Professional). 환경에 팀 도구(TeamCreate) 부재로 서브 에이전트 모드로 대체 실행 — 점진 검증은 집필자 자가 검증 + 독립 검증자 이중화로 구현 | 운영 기록 | 실행 환경 제약 |
