# JS → Python 개념 매핑 참조

커리큘럼 설계와 챕터 집필 시 참조하는 핵심 대응표. 챕터별 "JS 대응" 컬럼과 비교 코드의 근거 자료.

## 직접 대응 (빠르게 통과)

| JS | Python | 주의점 |
|----|--------|--------|
| `const`/`let` | 그냥 할당 (상수 관례는 UPPER_CASE) | 블록 스코프 없음 — 함수 스코프 |
| 템플릿 리터럴 `` `${x}` `` | f-string `f"{x}"` | 포맷 스펙 `f"{x:.2f}"`이 더 강력 |
| `Array.isArray` / `typeof` | `isinstance(x, list)` / `type()` | |
| `arr.push/pop` | `lst.append/pop` | `push` 아님 — 최다 오타 |
| `arr.includes(x)` | `x in lst` | 연산자로 해결 |
| `Object.keys/values/entries` | `d.keys()/values()/items()` | items()가 entries() |
| `try/catch/finally` | `try/except/finally` (+`else`) | 예외 타입을 except 절에 명시 |
| `JSON.parse/stringify` | `json.loads/dumps` | 표준 라이브러리 import 필요 |
| `import { x } from 'm'` | `from m import x` | 어순 반대 |
| `async/await` + Promise | `asyncio` + coroutine | AICE 범위 밖 — 부록 처리 가능 |

## 유사하지만 함정 (콜아웃 필수)

| 주제 | JS | Python | 함정 |
|------|----|--------|------|
| 동등 비교 | `===` | `==` | Python `==`는 값 비교(JS `===`와 유사), `is`는 정체성 비교. `== null` 패턴을 `is None`으로 |
| truthiness | `[]`, `{}`는 truthy | `[]`, `{}`, `0`, `""`는 **falsy** | JS 습관으로 `if (arr)` 쓰면 빈 리스트 분기가 반대로 동작 |
| 나눗셈 | `/` 하나 | `/`(항상 float), `//`(정수) | `5/2 === 2.5` 동일하나 `//` 신개념 |
| 삼항 | `cond ? a : b` | `a if cond else b` | 어순이 값-조건-값 |
| 정렬 | `sort((a,b)=>a-b)` | `sorted(key=...)` | 비교함수가 아니라 key 함수. `sort()`는 in-place+None 반환 |
| this/self | `this` 암묵 바인딩 | `self` 명시적 첫 인자 | 메서드 정의에 self 누락이 초기 최다 에러 |
| 클로저 루프 | `let`으로 해결 | 늦은 바인딩 — `lambda x=x:` 트릭 | JS의 `var` 시절 함정이 Python에 그대로 존재 |
| 가변 기본값 | 없음 | `def f(x=[])` 공유 함정 | `None` 기본값 + 내부 생성 패턴 필수 교육 |
| 복사 | spread `[...arr]` | `lst[:]`, `list(lst)`, `copy.deepcopy` | 얕은/깊은 복사 구분 동일하나 문법 상이 |
| 스코프 | 렉시컬, 블록 | 렉시컬, **함수** 단위(LEGB) | if/for 블록이 스코프를 만들지 않음. 재할당엔 `global`/`nonlocal` |

## Python 고유 (JS 대응 없음 — 분량 증대)

- **컴프리헨션**: `[x*2 for x in xs if x > 0]` — `xs.filter(...).map(...)`의 관용 대체. dict/set/generator 컴프리헨션까지
- **슬라이싱**: `lst[1:5:2]`, `lst[::-1]` — pandas 인덱싱의 선수 지식이므로 철저히
- **tuple과 언패킹**: `a, b = b, a`, 함수 다중 반환 — 구조 분해와 유사하나 더 보편적
- **`*args` / `**kwargs`**: rest/spread와 대응하되 keyword-only 인자 등 확장 개념
- **dunder 메서드**: `__init__`, `__repr__`, `__len__`, `__getitem__` — 연산자 오버로딩 체계
- **데코레이터**: 고차함수의 문법 설탕 — sklearn/keras 코드 읽기에 필요한 수준까지만
- **NumPy 브로드캐스팅 / pandas 불리언 인덱싱**: `df[df['age'] > 30]` — JS엔 없는 벡터화 사고방식. Part 2의 핵심 전환점

## 문체 규칙에 연결

이 표의 "함정" 열 항목은 챕터에서 반드시 `> ⚠️ **JS 함정**` 콜아웃으로 다룬다 (chapter-authoring 스킬 참조).
