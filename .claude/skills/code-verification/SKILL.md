---
name: code-verification
description: "e-book 마크다운 챕터의 Python 코드 블록을 추출·실행·검증하는 스킬. 코드 검증, 예제 실행 확인, 검증 보고서 생성, '코드 돌아가는지 확인해줘', '예제 검증해줘', 'ch05 다시 검증' 요청 시 반드시 사용. 눈으로 코드를 훑는 것으로 검증을 대체하지 말 것."
---

# Code Verification — 코드 블록 실행 검증 스킬

챕터 마크다운의 모든 ` ```python ` 블록을 실제로 실행하여 검증한다. LLM이 "올바라 보인다"고 판단한 코드의 상당수가 실제로는 NameError·오타·버전 차이로 실패하므로, 검증은 반드시 실행으로 한다.

## 사용법

```bash
python3 .claude/skills/code-verification/scripts/verify_code_blocks.py _workspace/02_chapters/ch03_strings.md
# 여러 파일 또는 디렉토리도 가능
python3 .claude/skills/code-verification/scripts/verify_code_blocks.py _workspace/02_chapters/
```

종료 코드: 0 = 전체 PASS, 1 = FAIL 존재, 2 = 사용법 오류.

## 스크립트가 하는 일 (계약)

1. 파일에서 ` ```python ` 펜스 블록을 순서대로 추출한다. ` ```python no-run ` 블록은 SKIP.
2. 한 파일의 블록들을 **같은 네임스페이스에서 위에서 아래로 순차 실행**한다 — 챕터 앞부분 변수를 뒤에서 쓰는 서술 흐름을 지원하기 위함.
3. `# 출력: {expected}` 주석이 있으면 해당 블록의 stdout 첫 줄이 expected로 시작하는지 대조한다. 불일치는 `OUTPUT_MISMATCH` 실패.
4. ImportError는 `DEPENDENCY_MISSING`으로 분류한다 — 코드 결함이 아니라 환경 문제이므로 리더에게 패키지 설치 여부를 확인받는다.
5. matplotlib은 Agg 백엔드로 강제되어 창을 띄우지 않는다. `plt.show()`는 no-op.

## 보고서 형식

검증 결과는 `_workspace/03_verification_report.md`에 챕터별 섹션으로 누적한다:

```markdown
## ch03_strings.md — 12 PASS / 1 FAIL / 2 SKIP (재검증 2회차)
| # | 상태 | 상세 |
|---|------|------|
| 5 | FAIL | NameError: name 'txt' is not defined (블록 5, 3행) |
| 7 | SKIP | no-run |
```

실패 발견 시 보고서 기록과 **동시에** chapter-writer에게 SendMessage로 블록 번호·에러 전문을 전달한다 — 보고서만 쓰고 알리지 않으면 파이프라인이 멈춘다.

## 판단 규칙

- 실패의 원인이 코드가 아니라 `# 출력:` 주석 쪽 오타로 보여도, 수정은 chapter-writer의 몫이다. 검증자가 챕터 파일을 직접 고치지 않는다 (역할 경계).
- 난수·시간처럼 실행마다 출력이 달라지는 예제에 `# 출력:` 주석이 붙어 있으면 chapter-writer에게 시드 고정(`random.seed`, `np.random.seed`) 또는 주석 제거를 요청한다.
- 같은 블록 3회 연속 실패 시 리더에게 에스컬레이션한다.
