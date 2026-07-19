---
name: ebook-building
description: "검수 완료된 마크다운 챕터를 단일 HTML e-book으로 조립하는 스킬. e-book 빌드, 조판, HTML 생성, 재빌드, '책으로 만들어줘', 'e-book 뽑아줘', '빌드 다시 해줘' 요청 시 반드시 사용."
---

# E-book Building — 조판·빌드 스킬

`_workspace/02_chapters/*.md`를 자기완결형 단일 HTML e-book(`dist/python4js-ebook.html`)으로 조립한다.

## 사용법

```bash
python3 .claude/skills/ebook-building/scripts/build_ebook.py \
  --outline _workspace/01_curriculum_outline.md \
  --chapters _workspace/02_chapters \
  --out dist/python4js-ebook.html
```

스크립트는 챕터 파일명(`ch{NN}_*.md`)의 번호순으로 정렬해 조립하고, 목차 사이드바·챕터 앵커·코드 하이라이팅용 마크업을 생성한다. `markdown` 패키지가 있으면 사용하고, 없으면 내장 미니 변환기(제목·문단·펜스 코드·표·목록·콜아웃·details)로 폴백한다.

## 빌드 전 게이트

1. `_workspace/04_qa_report.md`를 읽고 CRITICAL/HIGH 지적 중 OPEN 상태가 있으면 빌드하지 않는다 — 리더에게 보고하고 대기.
2. 목차의 챕터 수와 `02_chapters/` 파일 수가 일치하는지 확인한다. 누락 챕터는 임의로 건너뛰지 말고 리더에게 확인받는다.

## 디자인 방향 (템플릿에 반영됨)

방향은 **테크니컬 에디토리얼** — 기술 서적의 절제된 조판에 두 언어의 아이덴티티 컬러를 의미론적으로 사용한다:

- JS 코드 = 노랑 계열 액센트 보더, Python 코드 = 파랑 계열 액센트 보더 — 색이 장식이 아니라 "어느 언어인가"의 신호
- 본문 한글 시스템 폰트 스택(Pretendard → Apple SD Gothic Neo → sans-serif), 코드는 ui-monospace 스택
- 라이트/다크 모두 지원 (`prefers-color-scheme`)
- 사이드바 목차는 Part 구분 + 현재 위치 하이라이트, 모바일에서는 접힘
- 콜아웃(⚠️ JS 함정 / 🎯 AICE)은 배경 티트가 다른 인용 블록으로 구분

## 빌드 후 자체 점검

- 목차 앵커 링크 전수 클릭 검사(HTML 내 id 존재 확인으로 대체 가능)
- 챕터 수·순서가 목차와 일치하는지
- 파일 하나로 열리는지 (외부 CSS/JS/폰트 URL 참조가 없어야 함 — CDN 참조 금지)

콘텐츠 결함(오탈자·깨진 표)을 발견하면 직접 고치지 말고 chapter-writer에게 보고한다.

## 배포 (GitHub Pages)

이 책은 GitHub Pages로 배포된다: https://newids.github.io/python4js/ (저장소 `newids/python4js`, `main` 브랜치 `/docs` 폴더 서빙).

**재빌드 후 반드시** `dist/python4js-ebook.html`을 `docs/index.html`로 복사하고 커밋·푸시해야 라이브 사이트에 반영된다 — dist/만 갱신하면 배포본은 구버전으로 남는다. 푸시는 리더(오케스트레이터)가 사용자 확인 후 수행한다.
