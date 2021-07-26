오늘은 Javascript 공부했던 `Remind` 해보면서 `KeyPoint`를 다시 짚고자 한다.

우선, Javascript Directory 구성 할 때 Component를 구성할텐데 각 기능별로 `Component`를 구성하였다.

예를 들어서, `Javascript` 의 `Debounce`를 사용한다고 생각해보자.

처음에 `API` 가 구현되는 시점에서 `Debounce`를 구현해 주었는데 그러면 `Debounce`를 구현한 Component에 묶이기 때문에 좋은 구조라고 말할 수 없다.

e.g)

```javascript
import {useDebounceFunction} from "./utils/debounce.js"

this.onUserDebounceFunction = useDebounceFunction(
    fetchAPI, 500
)

const searchInput = new SearchInput({
    $app : this.$app,
    onFetchData : async(text) => {
        this.onUseDebounceFunction(text);  //이 위치에서 Debounce를 구현하고 Parameter로 넘겨주어도 되었겠지만 추상화 하였다.
    ]
})
```

## Destructuring assignment

배열에 다른 속성값을 추가하고자 할 때 `Destructuring`을 쓰면 간편하게 확장시킬 수 있다.

예를 들어서 `restAPI` 통신을 하고 데이터를 받아왔을 때 분명 새롭게 받아온 데이터거나 업데이트 하는데 필요한 데이터 일것이다.

이런 경우 `Destructuring`을 사용하면 간편하다.
e.g)

```javascript
apiResult = await fetchAPI();

//아래와 같이 써주게 되면 apiResult로 받아온 Property들을 모두 포함시켜서 새로운 Dict 형태로 객체를 생성해 주게 된다.
/*
const newData = {
    name : apiResult.name,
    age : apiResult.age,
    isGraduated : apiResult.isGraduated,
    isLoading : true 
}
와 같은 결과를 보게 된다. 
*/
const newData = {
  ...apiResult,
  isLoading: true,
};
```

## 오류메시지 작성

`try~catch` 작성 할 때 throw e; 하는 경우가 많은데 직접 `Error` 객체를 생성해서 에러 메시지를 상황에 맞게 관리할 수 있다.

error 메시지를 관리하는 파일을 하나 만들어 두고 거기에 각 에러 메시지에 대한 정의를 수행한 뒤 묶어 준다.

하나만 만들어보면 다음과 같이 작성할 수 있다.
e.g)

```javascript
export const errorMessage = {
  CHECK_VALIDATION_IS: (data, validate) => `${data}가 ${validate} 입니다.`,
};
```

## IIFE(Immediately Invokable Function Expression)

아래 형식은 아직 활용 예제를 보며 공부한것은 아니지만 MDN 문서를 참고하면 한번만 쓰는 함수에 IIFE를 사용한다고 한다.

아래와 같은 구조로 나타낼 수 있다. 경험적으로 아래 `IIFE`는 처음에 호출하는 함수의 경우 아래와 같이 쓰곤 했다.

```javascript
(function() (
    statments
))();
```

e.g)

```javascript
//main.js에서 App을 호출하는 경우(프로젝트에서 처음 시작되는 스크립트)
import App from "./App.js";
(function () {
  const app = new App();
})();
```
