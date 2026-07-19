# Chapter 07. 함수

> **학습 목표**
> - `def`로 함수를 정의하고 기본 인자·키워드 인자를 JS 대응으로 사용할 수 있다
> - `*args`/`**kwargs`로 가변 인자를 받아 rest/spread 습관을 Python으로 옮길 수 있다
> - `lambda`의 "한 줄 표현식" 제약을 이해하고 언제 def를 써야 할지 판단할 수 있다
> - 가변 기본값(`def f(x=[])`) 공유 함정을 피하는 `None` 관용구를 쓸 수 있다

## 7.1 함수 정의 — def와 화살표 함수

JS에서 함수는 값이자 일급 객체입니다. Python도 똑같습니다. 다만 화살표 함수 같은 간결 문법이 없고, 모든 함수는 `def` 키워드로 정의합니다.

| JavaScript | Python |
|---|---|
| ```const add = (a, b) => a + b;```<br>```const r = add(2, 3);``` | ```def add(a, b):```<br>```    return a + b```<br>```r = add(2, 3)``` |

가장 큰 차이는 세 가지입니다. (1) 화살표 함수의 암묵적 return이 없어 값을 돌려주려면 항상 `return`을 씁니다. (2) 블록은 중괄호가 아니라 들여쓰기입니다. (3) 함수도 값이므로 변수에 넣거나 인자로 넘길 수 있습니다.

```python
def add(a, b):
    return a + b

def apply(func, x, y):
    return func(x, y)

print(apply(add, 2, 3))
# 출력: 5
```

`return`이 없으면 JS의 `undefined`가 아니라 `None`을 반환합니다.

```python
def greet(name):
    print(f"안녕하세요, {name}님")

result = greet("Ada")
print(result)
# 출력: 안녕하세요, Ada님
```

## 7.2 기본 인자와 키워드 인자

JS의 기본 매개변수는 Python에도 있습니다. 여기에 더해 Python은 **호출 시 인자 이름을 지정**하는 키워드 인자를 언어 차원에서 지원합니다.

| JavaScript | Python |
|---|---|
| ```function f(a, b = 10) {}```<br>```f(1);``` | ```def f(a, b=10):```<br>```    ...```<br>```f(1)``` |

키워드 인자를 쓰면 인자 순서와 무관하게, 이름으로 값을 전달할 수 있습니다. 가독성이 크게 올라가므로 인자가 3개 이상인 함수 호출에서 특히 유용합니다.

```python
def connect(host, port=5432, timeout=30):
    return f"{host}:{port} (timeout={timeout})"

print(connect("db.local"))
# 출력: db.local:5432 (timeout=30)
print(connect("db.local", timeout=5))
# 출력: db.local:5432 (timeout=5)
print(connect("db.local", port=3306, timeout=5))
# 출력: db.local:3306 (timeout=5)
```

> 🎯 **AICE**: sklearn·keras API는 키워드 인자로 도배되어 있습니다. `train_test_split(X, y, test_size=0.2, random_state=42)`, `model.fit(X, y, epochs=10, batch_size=32)`처럼 대부분의 하이퍼파라미터가 키워드 인자입니다. 빈칸 채우기 문제에서 `random_state=____` 형태가 흔하므로 이름과 순서에 익숙해져야 합니다.

## 7.3 가변 인자 — *args와 **kwargs

JS의 rest 파라미터 `...args`는 Python에서 두 갈래로 나뉩니다. 위치 인자를 모으는 `*args`(튜플)와 키워드 인자를 모으는 `**kwargs`(딕셔너리)입니다.

| JavaScript | Python |
|---|---|
| ```function sum(...nums) {}``` | ```def total(*nums):``` |
| ```f(...arr)``` (spread 호출) | ```f(*arr)``` (언패킹 호출) |

`*args`는 남는 위치 인자를 튜플로 모읍니다. 호출할 때 리스트 앞에 `*`를 붙이면 반대로 펼쳐서 넘길 수 있습니다 — 이것이 JS spread의 대응입니다.

```python
def total(*nums):
    return sum(nums)

print(total(1, 2, 3, 4))
# 출력: 10

values = [10, 20, 30]
print(total(*values))
# 출력: 60
```

`**kwargs`는 이름 붙은 인자를 딕셔너리로 모읍니다. 설정값을 유연하게 받는 함수에서 자주 씁니다.

```python
def make_user(**kwargs):
    return kwargs

print(make_user(name="Ada", role="admin"))
# 출력: {'name': 'Ada', 'role': 'admin'}

config = {"host": "db.local", "port": 3306, "timeout": 5}
print(connect(**config))
# 출력: db.local:3306 (timeout=5)
```

딕셔너리 앞에 `**`를 붙이면 키워드 인자로 펼쳐집니다. 위에서 `connect(**config)`는 `connect(host="db.local", port=3306, timeout=5)`와 같습니다.

## 7.4 lambda — 화살표 함수의 축소판

JS 화살표 함수와 가장 닮은 것은 `lambda`입니다. 그러나 결정적 제약이 있습니다. **lambda 본문은 단 하나의 표현식**이어야 합니다. 문(statement)을 넣을 수 없으니 `if`문, 반복문, 여러 줄을 담지 못합니다.

| JavaScript | Python |
|---|---|
| ```const sq = x => x * x;``` | ```sq = lambda x: x * x``` |
| ```arr.sort((a,b) => a - b)``` | ```sorted(arr, key=lambda x: x)``` |

lambda는 주로 `sorted`, `map`, `filter`의 `key`/변환 함수처럼 "잠깐 쓰고 버릴" 자리에서 씁니다. 로직이 조금이라도 길어지면 미련 없이 `def`로 바꾸는 것이 Python다운 선택입니다.

```python
people = [("Ada", 36), ("Bob", 28), ("Cid", 41)]
by_age = sorted(people, key=lambda person: person[1])
print(by_age)
# 출력: [('Bob', 28), ('Ada', 36), ('Cid', 41)]
```

> ⚠️ **JS 함정**: JS에서는 화살표 함수 본문에 `{ ... }`로 여러 문장을 쓰지만, Python `lambda`는 그게 불가능합니다. `lambda x: (print(x), x*2)`처럼 억지로 쑤셔 넣지 말고, 두 줄 이상이면 `def`를 쓰세요. 삼항 표현식(`a if cond else b`)은 표현식이므로 lambda 안에서 사용할 수 있습니다.

## 7.5 가변 기본값 함정 — Python 최악의 함정

JS에는 없는, Python 초심자를 반드시 한 번은 무너뜨리는 함정입니다. **기본 인자값은 함수가 정의될 때 딱 한 번만 평가**되어, 모든 호출이 같은 객체를 공유합니다. 리스트나 딕셔너리를 기본값으로 쓰면 호출 간에 상태가 새어 나갑니다.

```python
def bad_append(item, target=[]):   # target이 모든 호출에서 공유됨
    target.append(item)
    return target

print(bad_append(1))
# 출력: [1]
print(bad_append(2))
# 출력: [1, 2]
```

두 번째 호출에서 `[2]`가 아니라 `[1, 2]`가 나옵니다. 빈 리스트가 매번 새로 생기는 게 아니기 때문입니다. JS의 `function f(x, t = [])`는 호출마다 새 배열을 만들지만, Python은 그렇지 않습니다.

> ⚠️ **JS 함정**: 가변 객체(list·dict·set)를 기본 인자로 절대 쓰지 마세요. JS 습관대로 `def f(x=[])`라고 쓰면 상태가 호출 간에 공유되어 디버깅이 극도로 어려운 버그가 됩니다.

해결책은 기본값을 `None`으로 두고 함수 안에서 새로 만드는 관용구입니다. 이 패턴을 손에 익히세요.

```python
def good_append(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

print(good_append(1))
# 출력: [1]
print(good_append(2))
# 출력: [2]
```

이제 호출마다 독립된 리스트가 생깁니다. `is None`으로 검사하는 이유는 2장에서 다룬 정체성 비교 관용구입니다.

## 연습문제

**Q1.** 임의 개수의 숫자를 받아 평균을 반환하는 함수입니다. 빈칸을 채우세요.

```python no-run
def average(____nums):
    return sum(nums) / len(nums)

print(average(10, 20, 30))   # 20.0
```

<details><summary>정답</summary>

```python
def average(*nums):
    return sum(nums) / len(nums)

print(average(10, 20, 30))
# 출력: 20.0
```

`*nums`가 위치 인자를 튜플로 모읍니다.
</details>

**Q2.** 가변 기본값 함정을 피하도록 빈칸을 채우세요.

```python no-run
def collect(value, bucket=____):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket
```

<details><summary>정답</summary>

```python
def collect(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket

print(collect(1))
# 출력: [1]
```

기본값을 `None`으로 두고 함수 내부에서 새 리스트를 생성해 호출 간 공유를 막습니다.
</details>

**Q3.** 딕셔너리 `opts`를 키워드 인자로 펼쳐 `connect`에 전달하는 코드입니다. 빈칸을 채우세요.

```python no-run
def connect(host, port=5432):
    return f"{host}:{port}"

opts = {"host": "srv", "port": 8080}
print(connect(____opts))   # srv:8080
```

<details><summary>정답</summary>

```python
def connect(host, port=5432):
    return f"{host}:{port}"

opts = {"host": "srv", "port": 8080}
print(connect(**opts))
# 출력: srv:8080
```

`**`가 딕셔너리를 키워드 인자로 펼칩니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `(a, b) => a + b` | `def f(a, b): return a + b` | 암묵 return 없음 |
| `x => x * x` | `lambda x: x * x` | 본문은 단일 표현식만 |
| 기본 매개변수 `b = 10` | `b=10` | 가변 객체 금지 |
| rest `...args` | `*args`(튜플) | 위치 인자 모으기 |
| (이름 인자 모으기 없음) | `**kwargs`(dict) | 키워드 인자 모으기 |
| spread 호출 `f(...arr)` | `f(*arr)` / `f(**d)` | 언패킹 호출 |
| (함정 없음) | `def f(x=[])` 공유 | `None` 기본값 관용구 필수 |
