# Chapter 01. 개발 환경과 실행 모델

> **학습 목표**
> - `python`/`pip`/`venv`를 node/npm/nvm 경험에 매핑해 설명할 수 있다
> - REPL과 스크립트 실행, 그리고 Jupyter 노트북 셀 실행 모델의 차이를 이해할 수 있다
> - import 경로가 어떻게 해석되는지, 스크립트와 모듈이 어떻게 다른지 구분할 수 있다

## 1.1 런타임과 패키지 매니저 — node/npm의 대응물

JS에서 `node app.js`로 스크립트를 돌리고 `npm install`로 의존성을 받던 흐름을 그대로 옮겨봅니다. 이름만 바뀔 뿐 역할은 거의 1:1로 대응합니다.

| JavaScript | Python |
|---|---|
| `node app.js` | `python app.py` |
| `npm install requests` | `pip install requests` |
| `node -v` / `nvm use 20` | `python --version` / `pyenv` |

`node`처럼 `python`이 인터프리터입니다. 단, 여러 버전이 깔린 시스템에서는 `python`이 구버전(2.x)을 가리킬 수 있어, 실무에서는 `python3`을 명시하는 습관이 안전합니다.

```python
import sys
print(sys.version_info.major)
# 출력: 3
```

> 🎯 **AICE**: 실기 환경은 Python 3.x가 설치된 Jupyter입니다. 버전 확인은 `import sys; sys.version` 또는 `!python --version`으로 합니다.

## 1.2 가상환경 — node_modules 대신 venv

JS는 `node_modules`가 프로젝트 폴더에 격리됩니다. Python은 전역 설치가 기본이라, 프로젝트별 격리를 위해 **가상환경(virtual environment)**을 명시적으로 만듭니다.

```python no-run
# 셸에서 실행 (프로젝트별 의존성 격리)
python3 -m venv .venv          # .venv 폴더 생성 (node_modules 대응)
source .venv/bin/activate      # 활성화 (Windows: .venv\Scripts\activate)
pip install pandas             # 이제 .venv 안에만 설치됨
```

`package.json` + `package-lock.json`에 대응하는 것은 `requirements.txt`입니다. `pip freeze > requirements.txt`로 만들고 `pip install -r requirements.txt`로 복원합니다.

> ⚠️ **JS 함정**: `venv`를 활성화하지 않고 `pip install`하면 전역 파이썬을 오염시킵니다. `node_modules`처럼 자동 격리되지 않으므로 `activate`를 잊지 마세요.

## 1.3 REPL — node 대화형 셸과 동일

인자 없이 `python3`을 실행하면 node의 대화형 REPL과 똑같은 프롬프트가 뜹니다. 표현식을 입력하면 값이 바로 출력됩니다.

```python
# REPL에서 한 줄씩 입력한다고 상상하세요
2 ** 10          # node라면 2 ** 10, 결과는 동일
result = 2 ** 10
print(result)
# 출력: 1024
```

REPL에서는 `print` 없이 표현식만 쳐도 값이 표시되지만, 스크립트(`.py` 파일)에서는 `print`로 명시 출력해야 합니다. 이 차이는 다음 절의 Jupyter로 이어집니다.

## 1.4 Jupyter 노트북 셀 실행 모델

AICE 실기의 핵심 환경입니다. Jupyter는 REPL을 웹에 올린 형태로, 코드를 **셀(cell)** 단위로 나눠 실행합니다. 각 셀은 실행 순서를 공유하는 하나의 네임스페이스에서 위에서 아래로 돌아갑니다.

```python
# [셀 1] 변수를 정의하면
tax_rate = 0.1

# [셀 2] 다음 셀에서 그대로 참조됩니다 (전역 네임스페이스 공유)
price = 1000
total = price * (1 + tax_rate)
print(total)   # Jupyter 셀이라면 마지막 줄에 total만 써도 표시됩니다
# 출력: 1100.0
```

셀의 **마지막 표현식**은 자동으로 표시되는 것이 REPL과 같지만, 셀 실행 순서를 사람이 임의로 바꿀 수 있다는 점이 함정입니다.

> ⚠️ **JS 함정**: 셀을 위→아래 순서가 아니라 실행한 순서대로 상태가 쌓입니다. 아래 셀을 먼저 실행하고 위 셀을 나중에 실행하면, 코드 순서와 무관하게 마지막 실행 값이 남습니다. 채점 전 반드시 **"Restart & Run All"**로 위에서부터 다시 돌려 재현성을 확인하세요.

> 🎯 **AICE**: 실기는 셀 곳곳의 `____` 빈칸을 채운 뒤 위에서부터 순서대로 실행해 오류 없이 통과하는지로 채점됩니다. 셀 간 변수 공유를 전제로 문제가 이어집니다.

## 1.5 import 경로와 스크립트 vs 모듈

JS의 `import { x } from './m.js'`처럼 Python도 파일을 모듈로 불러옵니다. 어순이 반대(`from m import x`)라는 점은 10장에서 자세히 다루고, 여기서는 실행 모델만 봅니다.

| JavaScript | Python |
|---|---|
| `import { add } from './util.js'` | `from util import add` |
| `require('./util')` | `import util` |

같은 `.py` 파일이 **직접 실행될 때**와 **import될 때**를 구분하는 관용구가 있습니다. JS의 `require.main === module` 패턴과 정확히 대응합니다.

```python
# 이 파일이 python xxx.py로 직접 실행되면 __name__ == "__main__"
# 다른 파일이 import하면 __name__ == 모듈 이름
if __name__ == "__main__":
    print("스크립트로 직접 실행됨")
# 출력: 스크립트로 직접 실행됨
```

검증 환경은 이 코드를 `__main__`으로 실행하므로 위 분기가 참이 됩니다. 모듈로 import하면 이 블록은 건너뜁니다.

> ⚠️ **JS 함정**: import 경로는 실행 위치(현재 작업 디렉터리)와 `sys.path`를 기준으로 해석됩니다. JS의 상대경로(`./`)처럼 파일 기준이 아니어서, 다른 폴더에서 실행하면 `ModuleNotFoundError`가 날 수 있습니다.

## 연습문제

**Q1.** 현재 파이썬 버전의 major 번호(예: 3)를 출력하도록 빈칸을 채우세요.

```python no-run
import sys
print(sys.____.major)
```

<details><summary>정답</summary>

```python
import sys
print(sys.version_info.major)
# 출력: 3
```

`sys.version_info`는 (major, minor, micro, ...) 형태의 네임드 튜플입니다.
</details>

**Q2.** 이 파일이 직접 실행될 때만 메시지를 출력하는 관용구입니다. 빈칸을 채우세요.

```python no-run
if __name__ == "____":
    print("main")
```

<details><summary>정답</summary>

```python
if __name__ == "__main__":
    print("main")
# 출력: main
```

JS의 `require.main === module`에 대응하는 스크립트 진입점 관용구입니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `node app.js` | `python app.py` | 인터프리터 직접 실행 |
| `npm install X` | `pip install X` | 가상환경 활성화 후 실행 |
| `node_modules` | `.venv` (venv) | 자동 격리 아님 — 명시적 생성·활성화 |
| `package.json` 의존성 | `requirements.txt` | `pip freeze`로 생성 |
| `require.main === module` | `if __name__ == "__main__":` | 스크립트 진입점 |
| REPL(`node`) | REPL(`python3`) / Jupyter 셀 | 마지막 표현식 자동 표시 |
