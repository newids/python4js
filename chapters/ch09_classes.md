# Chapter 09. 클래스와 객체

> **학습 목표**
> - `class`/`__init__`/`self`로 객체를 정의하고 JS 클래스 문법과의 차이를 안다
> - 인스턴스 속성과 클래스 속성을 구분해 공유 상태 함정을 피한다
> - dunder 메서드(`__repr__`, `__len__`)로 연산자·내장 함수 동작을 커스터마이즈한다
> - 상속과 `super()`를 사용해 sklearn/keras 객체 코드를 읽을 토대를 만든다

## 9.1 클래스 정의 — self는 명시적이다

JS의 `class` 문법과 Python의 `class`는 겉모습이 비슷합니다. 결정적 차이는 하나입니다. Python은 **모든 메서드의 첫 인자로 `self`를 명시**합니다. JS의 `this`가 암묵적으로 바인딩되는 것과 달리, Python은 인스턴스를 직접 받습니다.

| JavaScript | Python |
|---|---|
| ```class User {```<br>```  constructor(name) { this.name = name; }```<br>```}``` | ```class User:```<br>```    def __init__(self, name):```<br>```        self.name = name``` |

생성자는 `constructor`가 아니라 `__init__`이라는 dunder(double underscore) 메서드입니다. 인스턴스를 만들 때 `new` 키워드 없이 클래스를 함수처럼 호출합니다.

```python
class User:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"안녕하세요, {self.name}님"

u = User("Ada")
print(u.greet())
# 출력: 안녕하세요, Ada님
```

> ⚠️ **JS 함정**: 메서드 정의에서 `self`를 빠뜨리는 것이 Python 입문자의 최다 에러입니다. JS 습관대로 `def greet():`라고 쓰면 호출 시 `TypeError: greet() takes 0 positional arguments but 1 was given`이 납니다. 인스턴스 메서드의 첫 인자는 **항상** `self`입니다. 호출할 때는 `u.greet()`처럼 인자를 안 넘겨도, Python이 자동으로 `u`를 `self`로 전달합니다.

## 9.2 인스턴스 속성과 클래스 속성

`self.name`처럼 `self`에 붙이면 **인스턴스 속성**으로 객체마다 독립적입니다. 반면 클래스 본문에 직접 쓴 변수는 **클래스 속성**으로 모든 인스턴스가 공유합니다. JS의 `static` 필드와 비슷하되, 인스턴스에서도 읽힌다는 점이 다릅니다.

```python
class Circle:
    pi = 3.14159            # 클래스 속성 (공유)

    def __init__(self, r):
        self.r = r          # 인스턴스 속성 (개별)

    def area(self):
        return Circle.pi * self.r ** 2

c = Circle(10)
print(c.area())
# 출력: 314.159
print(Circle.pi)
# 출력: 3.14159
```

> ⚠️ **JS 함정**: 클래스 속성에 가변 객체(list·dict)를 쓰면 7장의 공유 함정이 재현됩니다. 모든 인스턴스가 같은 리스트를 공유하므로, 인스턴스별 컬렉션은 반드시 `__init__` 안에서 `self.items = []`로 만드세요.

```python
class Cart:
    def __init__(self):
        self.items = []     # 인스턴스마다 새 리스트

a, b = Cart(), Cart()
a.items.append("apple")
print(b.items)
# 출력: []
```

## 9.3 dunder 메서드 — 연산자와 내장 함수 커스터마이즈

dunder 메서드는 파이썬이 특정 문법·내장 함수를 만났을 때 자동으로 호출하는 특수 메서드입니다. JS의 `toString()`, `Symbol.iterator`, `valueOf`가 하던 일을 Python은 이름이 정해진 dunder로 처리합니다.

`__repr__`은 객체를 문자열로 표현하는 방법을 정의합니다. JS `toString()`의 대응이며, 디버깅 출력과 REPL 표시에 쓰입니다.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __len__(self):
        return 2

p = Point(3, 4)
print(p)
# 출력: Point(3, 4)
print(len(p))
# 출력: 2
```

`len(p)`를 호출하면 Python이 `p.__len__()`을 대신 불러 줍니다. 이렇게 내장 함수와 연산자 동작을 객체에 위임하는 체계가 dunder입니다.

> 🎯 **AICE**: 시험에서 dunder를 직접 구현할 일은 드뭅니다. 그러나 sklearn 모델을 셀에서 실행하면 `LogisticRegression(C=1.0, ...)` 같은 `__repr__` 출력이 뜨는데, 이것이 무엇인지 알아야 결과를 읽을 수 있습니다. 또 `model.fit(...)`, `model.predict(...)`가 전부 `self`를 받는 인스턴스 메서드라는 사실이 estimator API 이해의 바탕입니다.

## 9.4 상속과 super()

상속 문법은 클래스 이름 뒤 괄호에 부모를 적습니다. 부모 메서드 호출은 `super()`로 하며, JS와 개념이 같습니다.

| JavaScript | Python |
|---|---|
| ```class Dog extends Animal {}``` | ```class Dog(Animal):``` |
| ```super(name);``` | ```super().__init__(name)``` |

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return f"{self.name}: 멍멍"

d = Dog("바둑이")
print(d.speak())
# 출력: 바둑이: 멍멍
```

자식이 부모의 `__init__`을 확장할 때는 `super().__init__()`으로 부모 초기화를 먼저 호출합니다.

```python
class Puppy(Dog):
    def __init__(self, name, age):
        super().__init__(name)   # 부모의 name 초기화
        self.age = age

pup = Puppy("콩이", 1)
print(pup.speak(), pup.age)
# 출력: 콩이: 멍멍 1
```

이 구조가 keras에서 `class MyModel(tf.keras.Model)`처럼 프레임워크 클래스를 상속해 커스텀 모델을 만드는 패턴의 기초입니다.

## 연습문제

**Q1.** 인스턴스 메서드가 올바로 동작하도록 빈칸을 채우세요.

```python no-run
class Counter:
    def __init__(____):
        self.n = 0

    def increment(____):
        self.n += 1

c = Counter()
c.increment()
print(c.n)   # 1
```

<details><summary>정답</summary>

```python
class Counter:
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 1

c = Counter()
c.increment()
print(c.n)
# 출력: 1
```

모든 인스턴스 메서드의 첫 인자는 `self`입니다.
</details>

**Q2.** `print(book)`이 `"Book: Python"`을 출력하도록 빈칸을 채우세요.

```python no-run
class Book:
    def __init__(self, title):
        self.title = title

    def ____(self):
        return f"Book: {self.title}"

book = Book("Python")
print(book)   # Book: Python
```

<details><summary>정답</summary>

```python
class Book:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Book: {self.title}"

book = Book("Python")
print(book)
# 출력: Book: Python
```

`__repr__`이 객체의 문자열 표현을 정의합니다.
</details>

## 이 챕터의 JS→Python 대응 한눈에 보기

| JS | Python | 비고 |
|----|--------|------|
| `class C {}` | `class C:` | 문법 유사 |
| `constructor()` | `__init__(self, ...)` | 생성자 dunder |
| `this` (암묵) | `self` (명시) | 첫 인자로 항상 명시 |
| `new C()` | `C()` | new 없음 |
| `static field` | 클래스 속성 | 인스턴스에서도 읽힘 |
| `toString()` | `__repr__` | 문자열 표현 |
| `extends` / `super()` | `(Parent)` / `super().__init__()` | 상속 |
