# Chapter 10. 모듈과 패키지

> **학습 목표**
> - `from ... import ...`의 어순이 JS import와 반대임을 이해하고 자유롭게 쓴다
> - `import ... as`로 별칭을 붙여 `import pandas as pd` 관례를 소화한다
> - 표준 라이브러리 모듈(`math`, `json`, `random`)을 import해 활용한다
> - `if __name__ == "__main__"` 관용구의 의미와 용도를 안다

## 10.1 import 어순 — from이 먼저다

JS의 named import는 `import { x } from 'module'`로, 가져올 이름을 먼저 쓰고 모듈을 나중에 씁니다. Python은 **정확히 반대**입니다. 모듈을 `from`으로 먼저 지정하고 이름을 `import`합니다.

| JavaScript | Python |
|---|---|
| ```import { sqrt } from 'math';``` | ```from math import sqrt``` |
| ```import * as math from 'math';``` | ```import math``` |

`import math`는 모듈 전체를 가져와 `math.sqrt(...)`처럼 접근하고, `from math import sqrt`는 특정 이름만 현재 네임스페이스로 끌어옵니다. JS의 namespace import(`* as`)와 named import의 구분과 대응합니다.

```python
import math
from math import sqrt, pi

print(math.floor(3.7))
# 출력: 3
print(sqrt(16))
# 출력: 4.0
print(round(pi, 2))
# 출력: 3.14
```

여러 이름을 한 번에 가져올 때는 쉼표로 나열합니다. 어순만 뒤집으면 JS 지식이 그대로 통합니다.

## 10.2 별칭 — import ... as

JS의 `import { x as y }`처럼 Python도 `as`로 별칭을 붙입니다. 데이터 분석 생태계에는 사실상 표준이 된 별칭 관례가 있습니다. 이 관례를 손가락에 익혀 두어야 남의 코드도 읽고 시험 답안도 씁니다.

| JavaScript | Python |
|---|---|
| ```import { x as y } from 'm';``` | ```from m import x as y``` |
| ```import * as np from 'numpy';``` | ```import numpy as np``` |

```python
import json as j

data = j.dumps({"name": "Ada", "age": 36})
print(data)
# 출력: {"name": "Ada", "age": 36}
```

> 🎯 **AICE**: 실기 첫 셀은 거의 항상 `import numpy as np`, `import pandas as pd`, `import matplotlib.pyplot as plt`로 시작합니다. 이후 모든 코드가 `pd.read_csv(...)`, `np.array(...)` 형태이므로 별칭을 틀리면 연쇄적으로 답이 무너집니다. `pd`, `np`, `plt`는 통째로 암기하세요.

## 10.3 표준 라이브러리 — 배터리 포함

Python은 "batteries included" 철학으로 방대한 표준 라이브러리를 기본 제공합니다. Node의 `fs`, `path`처럼 별도 설치 없이 import만 하면 됩니다. `random`으로 난수 예제를 볼 때는 **시드를 고정**해 재현성을 확보합니다.

```python
import random

random.seed(42)          # 시드 고정 — 항상 같은 결과
print(random.randint(1, 100))
# 출력: 82
print(random.choice(["a", "b", "c"]))
# 출력: a
```

```python
from datetime import date

d = date(2026, 7, 19)
print(d.year, d.month, d.day)
# 출력: 2026 7 19
print(d.isoformat())
# 출력: 2026-07-19
```

`json`, `math`, `random`, `datetime`, `collections` 등은 어떤 환경에서도 쓸 수 있으니 데이터 처리 전 단계에서 유용합니다.

## 10.4 if __name__ == "__main__"

이 관용구는 JS에 직접 대응이 없어 처음엔 낯섭니다. Python 파일은 두 가지로 쓰입니다. (1) `python script.py`로 **직접 실행**하거나, (2) 다른 파일에서 `import`되는 **모듈**로 쓰입니다. 파일이 직접 실행되면 그 파일의 `__name__`이 `"__main__"`이 되고, import되면 모듈 이름이 됩니다.

| JavaScript (Node) | Python |
|---|---|
| ```if (require.main === module) {}``` | ```if __name__ == "__main__":``` |

따라서 아래 관용구는 "이 파일이 직접 실행될 때만 이 블록을 돌려라"라는 뜻입니다. 함수·클래스 정의는 import해서 재사용하되, 실행 진입점 코드는 이 가드 안에 넣어 import 시 실행되지 않게 막는 것이 목적입니다.

```python
def main():
    print("직접 실행됨")

if __name__ == "__main__":
    main()
# 출력: 직접 실행됨
```

이 파일을 다른 곳에서 `import`하면 `__name__`이 파일명이 되므로 `main()`이 호출되지 않습니다. 라이브러리로도, 스크립트로도 쓸 수 있는 재사용 가능한 파일을 만드는 표준 패턴입니다.

## 연습문제

**Q1.** `math`에서 `sqrt`만 가져와 사용하도록 빈칸을 채우세요.

```python no-run
____ math ____ sqrt
print(sqrt(81))   # 9.0
```

<details><summary>정답</summary>

```python
from math import sqrt
print(sqrt(81))
# 출력: 9.0
```

`from 모듈 import 이름` 어순으로 특정 이름만 가져옵니다.
</details>

**Q2.** pandas를 `pd` 별칭으로 가져오는 관례 코드입니다. 빈칸을 채우세요. (실행 대상 아님)

```python no-run
import pandas ____ pd
```

<details><summary>정답</summary>

```python no-run
import pandas as pd
```

`as`로 별칭을 붙입니다. `pd`는 데이터 분석의 사실상 표준 별칭입니다.
</details>

**Q3.** 파일이 직접 실행될 때만 `run()`을 호출하도록 빈칸을 채우세요.

```python no-run
def run():
    print("start")

if __name__ == "____":
    run()
```

<details><summary>정답</summary>

```python
def run():
    print("start")

if __name__ == "__main__":
    run()
# 출력: start
```

직접 실행 시 `__name__`은 `"__main__"`이 됩니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `import { x } from 'm'` | `from m import x` | 어순 반대 |
| `import * as m from 'm'` | `import m` | 모듈 전체 |
| `import { x as y }` | `from m import x as y` | 별칭 |
| (관례) | `import pandas as pd` | 표준 별칭 암기 |
| `require.main === module` | `if __name__ == "__main__"` | 실행 진입점 가드 |
