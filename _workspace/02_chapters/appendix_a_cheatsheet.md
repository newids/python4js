# Appendix A. JS → Python 치트시트

> 전 챕터의 "한눈에 보기" 표를 한곳에 모은 대조표입니다. 시험 직전 훑어보기·실무 참조용으로 쓰세요. 표 안 코드는 3줄 이하 스니펫이며, 자세한 설명·함정은 각 챕터를 참조합니다.

## A.1 실행 환경 (1장)

| JS | Python | 비고 |
|----|--------|------|
| `node app.js` | `python app.py` | 인터프리터 직접 실행 |
| `npm install X` | `pip install X` | 가상환경 활성화 후 |
| `node_modules` | `.venv` (venv) | 자동 격리 아님 |
| `package.json` 의존성 | `requirements.txt` | `pip freeze`로 생성 |
| `require.main === module` | `if __name__ == "__main__":` | 스크립트 진입점 |

## A.2 변수·타입·연산자 (2장) — 함정 밀집 구간

| JS | Python | 비고 |
|----|--------|------|
| `let` / `const` | 그냥 할당 / 대문자 관례 | `const` 없음 |
| `===` | `==` | 값 비교 |
| 동일 참조 비교 | `is` | 정체성 비교 |
| `x == null` | `x is None` | `None`은 싱글턴 |
| `Math.floor(a/b)` | `a // b` | 정수 나눗셈 |
| `[]`/`{}` truthy | `[]`/`{}` **falsy** | ⚠️ 분기 반대 |

## A.3 문자열·포매팅 (3장)

| JS | Python | 비고 |
|----|--------|------|
| `` `${x}` `` | `f"{x}"` | 따옴표 + `f` |
| `x.toFixed(2)` | `f"{x:.2f}"` | 포맷 스펙 |
| `n.toLocaleString()` | `f"{n:,}"` | 천단위 |
| `arr.join("-")` | `"-".join(arr)` | 구분자가 주어 |
| `s.trim()` | `s.strip()` | 양끝 공백 |
| `s.replaceAll(a,b)` | `s.replace(a,b)` | 기본 전체 치환 |

## A.4 컬렉션·슬라이싱 (4장)

| JS | Python | 비고 |
|----|--------|------|
| `arr.push(x)` | `lst.append(x)` | ⚠️ push 없음 |
| `arr.length` | `len(lst)` | 함수 호출 |
| `arr.slice(1,4)` | `lst[1:4]` | stop 미포함 |
| `[...arr].reverse()` | `lst[::-1]` | 새 리스트 |
| `obj["k"]`(→undefined) | `d.get("k")` | 안전 접근 |
| `new Set([...])` | `{...}` / `set()` | 빈 set은 `set()` |
| (없음) | `(x, y)` 튜플 | 불변·언패킹 |
| `includes`/`has` | `in` | 공통 연산 |

## A.5 제어 흐름 (5장)

| JS | Python | 비고 |
|----|--------|------|
| `if(...){}` | `if ...:` + 들여쓰기 | 중괄호 없음 |
| `else if` | `elif` | |
| `for (const x of arr)` | `for x in arr:` | 값 순회 |
| `for(let i=0;...)` | `for i in range(n):` | |
| `arr.forEach((v,i)=>)` | `enumerate(arr)` | (인덱스, 값) |
| (없음) | `zip(a, b)` | 시퀀스 병렬 |
| `cond ? a : b` | `a if cond else b` | ⚠️ 어순 뒤집힘 |
| `n++` | `n += 1` | 증감 없음 |

## A.6 컴프리헨션 (6장)

| JS | Python | 비고 |
|----|--------|------|
| `arr.map(f)` | `[f(x) for x in arr]` | 표현식 직접 |
| `arr.filter(p)` | `[x for x in arr if p(x)]` | 뒤쪽 if |
| `arr.filter().map()` | `[f(x) for x in arr if p(x)]` | 한 줄 |
| `Object.fromEntries` | `{k: v for ...}` | dict 컴프리헨션 |
| (지연 평가 없음) | `(f(x) for x in arr)` | 제너레이터 |

## A.7 함수 (7장)

| JS | Python | 비고 |
|----|--------|------|
| `(a,b)=>a+b` | `def f(a,b): return a+b` | 암묵 return 없음 |
| `x=>x*x` | `lambda x: x*x` | 단일 표현식만 |
| rest `...args` | `*args` (튜플) | 위치 인자 모으기 |
| (이름 인자 모으기 없음) | `**kwargs` (dict) | 키워드 모으기 |
| spread `f(...arr)` | `f(*arr)` / `f(**d)` | 언패킹 호출 |
| (함정 없음) | `def f(x=[])` 공유 | ⚠️ `None` 기본값 관용구 |

## A.8 스코프·클로저 (8장)

| JS | Python | 비고 |
|----|--------|------|
| 블록 스코프 | 함수 스코프(LEGB) | if/for는 스코프 아님 |
| 바깥 변수 그냥 수정 | `global`/`nonlocal` | 재할당엔 선언 필수 |
| `let` 루프 새 바인딩 | 늦은 바인딩 함정 | ⚠️ `lambda x=x:` 트릭 |

## A.9 클래스 (9장)

| JS | Python | 비고 |
|----|--------|------|
| `constructor()` | `__init__(self, ...)` | 생성자 dunder |
| `this` (암묵) | `self` (명시) | ⚠️ 첫 인자 항상 |
| `new C()` | `C()` | new 없음 |
| `toString()` | `__repr__` | 문자열 표현 |
| `extends`/`super()` | `(Parent)`/`super().__init__()` | 상속 |

## A.10 모듈·에러·이터레이터 (10~12장)

| JS | Python | 비고 |
|----|--------|------|
| `import { x } from 'm'` | `from m import x` | 어순 반대 |
| `import { x as y }` | `from m import x as y` | 별칭 |
| `try{}catch(e){}` | `try: ... except E as e:` | 타입 명시 |
| (없음) | `else:` 절 | 예외 없을 때 |
| `throw new Error()` | `raise ValueError()` | 예외 발생 |
| `it.next().value` | `next(it)` | 다음 값 |
| `function*(){yield}` | `def f(): yield` | 제너레이터 |

## A.11 NumPy 핵심 (13장)

| JS | Python (NumPy) | 비고 |
|----|--------|------|
| `new Float64Array([...])` | `np.array([...])` | 벡터 배열 |
| `arr.length` | `arr.shape` | 튜플(다차원) |
| `mat[i][j]` | `mat[i, j]` | 쉼표 접근 |
| `arr.map(f)` | `arr` 통째 연산 | 루프 불필요 |
| `arr.filter(x=>x>10)` | `arr[arr > 10]` | 불리언 인덱싱 |
| `&&` / `\|\|` | `&` / `\|` (괄호 필수) | `and`/`or` 아님 |
| `arr.reduce(+)` | `arr.sum(axis=0)` | axis로 방향 |

## A.12 pandas 핵심 (14~15장)

| JS | Python (pandas) | 비고 |
|----|--------|------|
| 행 객체 배열 | `pd.DataFrame({열:[...]})` | 열 딕셔너리 생성 |
| `arr[i]` | `df.iloc[i]` | 정수 위치 |
| (대응 없음) | `df.loc[라벨, 열]` | 라벨 기반 |
| `arr.filter(p=>p.x>0)` | `df[df["x"] > 0]` | 불리언 인덱싱 |
| `filter(A && B)` | `df[(A) & (B)]` | 괄호+`&` 필수 |
| `x == null` 체크 | `df.isnull()` | `==np.nan`은 항상 False |
| `x ?? 기본` | `df["c"].fillna(값)` | 결측 대치 |
| `Number(x)` | `df["c"].astype("int64")` | 타입 변환 |
| `groupby` 수동 | `df.groupby("k")["v"].mean()` | GROUP BY |
| 수동 조인 | `pd.merge(a, b, on="k")` | JOIN |

## A.13 전처리 인코딩·스케일링 (15장, 19장)

| 목적 | Python (sklearn/pandas) | 비고 |
|------|--------|------|
| 원-핫 인코딩(입력 X) | `pd.get_dummies(df, columns=[...])` | 범주 → 이진 열 |
| 라벨 인코딩(목표 y) | `LabelEncoder().fit_transform(y)` | 범주 → 정수 |
| 표준화 | `StandardScaler().fit_transform(X)` | 평균0 분산1 |
| 정규화 | `MinMaxScaler().fit_transform(X)` | 0~1 범위 |
| 결측 대치 | `SimpleImputer(strategy="mean")` | 평균/최빈 |
| train/test 분리 적용 | train `fit_transform`, test `transform` | ⚠️ 누수 방지 |

## A.14 scikit-learn 모델링 (17장, 20~22장)

| 단계 | Python (scikit-learn) | 비고 |
|------|--------|------|
| 데이터 분리 | `train_test_split(X, y, test_size=0.2, random_state=42)` | 반환 순서 고정 |
| 회귀 | `LinearRegression()` | `.fit`/`.predict` |
| 분류 | `LogisticRegression()` / `DecisionTreeClassifier(max_depth=)` | |
| 앙상블 | `RandomForestClassifier(n_estimators=)` / `GradientBoostingClassifier(learning_rate=)` | Regressor 짝 존재 |
| 학습/예측 | `model.fit(X_train, y_train)` → `model.predict(X_test)` | |
| 회귀 지표 | `r2_score` / `root_mean_squared_error` / `mean_absolute_error` | ⚠️`(정답, 예측)` 순 |
| 분류 지표 | `accuracy_score` / `f1_score` / `confusion_matrix` | ⚠️`(정답, 예측)` 순 |
| 교차검증 | `cross_val_score(model, X, y, cv=5)` | 점수 배열 반환 |
| 튜닝 | `GridSearchCV(model, param_grid, cv=5)` | `best_params_`/`best_score_` |
| 파이프라인 | `Pipeline([("prep", ...), ("clf", ...)])` | 파라미터 `clf__C` |

## A.15 Keras 딥러닝 (18장, 23장)

| 단계 | Python (Keras) | 비고 |
|------|--------|------|
| 모델 | `keras.Sequential([...])` | 순차 스택 |
| 완전연결층 | `layers.Dense(뉴런, activation="relu")` | 은닉층 |
| 입력 | `keras.Input(shape=(특성수,))` | 배치 제외 |
| 컴파일 | `model.compile(optimizer="adam", loss=, metrics=["accuracy"])` | loss↔활성화 짝 |
| 학습 | `model.fit(X, y, epochs=, batch_size=, validation_data=)` | history 반환 |
| 콜백 | `EarlyStopping(monitor="val_loss", patience=)` | `callbacks=[...]` |
| 평가 | `model.evaluate(X_test, y_test)` | [loss, metrics] |
| CNN/RNN | `Conv2D` / `LSTM` / `Embedding` | 23장 |

## A.16 시각화·텍스트 (16장, 24장)

| 목적 | Python | 비고 |
|------|--------|------|
| 범주 빈도 | `sns.countplot(data=df, x="col")` | EDA |
| 수치 분포 | `sns.histplot(data=df, x="col", bins=)` | |
| 이상치 | `sns.boxplot(data=df, x=, y=)` | 사분위 |
| 상관관계 | `sns.heatmap(df.corr(), annot=True)` | |
| 학습곡선 | `plt.plot(history.history["loss"])` + `plt.legend()` | 범례 짝 |
| BoW | `CountVectorizer().fit_transform(docs)` | 빈도 행렬 |
| TF-IDF | `TfidfVectorizer().fit_transform(docs)` | 중요도 가중 |

## A.17 JS 습관성 함정 총정리

시험·실무에서 조용히 틀리기 쉬운 핵심 함정만 추린 목록입니다.

| 함정 | 잘못된 JS 습관 | Python 정답 |
|------|--------|------|
| truthiness | `if (arr)` | `if arr is not None:` (존재 확인) |
| None 비교 | `x == None` | `x is None` |
| 정수 나눗셈 | `Math.floor(a/b)` | `a // b` |
| 리스트 추가 | `arr.push(x)` | `lst.append(x)` |
| 삼항 어순 | `cond ? a : b` | `a if cond else b` |
| self 누락 | `method() { this... }` | `def method(self):` |
| 가변 기본값 | `def f(x=[])` | `def f(x=None):` 내부 생성 |
| pandas 논리 | `df[A and B]` | `df[(A) & (B)]` |
| 지표 인자 순서 | `f1_score(pred, y)` | `f1_score(y_test, pred)` |
| NaN 비교 | `x == np.nan` | `df["c"].isnull()` |
