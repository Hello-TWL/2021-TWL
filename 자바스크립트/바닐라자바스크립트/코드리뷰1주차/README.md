## 코드리뷰 1주차



## render 부분

innterHTML 부분에서 reduce 를 사용했을 때 data를 순회하면서 저장한 값을 innerHTML에 추가해주게 되는데

오히려, map 함수를 사용해 join으로 tag를 만들어 새로운 array로 구성할 수 있는게 인상적이었습니다. 

```
this.render = () =>{
          const todoHtmlStr = this.state.map(({text, isCompleted}) =>
            isCompleted ? `<li><s>${text}</s></li>` : `<li>${text}</li>`
            //todo=>`<li>${todo.text}</li>`
            
            ).join('')
          
          this.$target.innerHTML=todoHtmlStr
    }
```



## try~catch

render 부분에 try~catch문을 작성하였는데 오히려 이것보다 자바스크립트 객체 생성 부분에 try~catch를 거는것이 컴포넌트에서 에러 exception을 구성하는데 효과적이다라는 생각이 들었습니다. 

```
try{
  const $app = document.querySelector('#app')
  const todoList = new TodoList(data, $app);
  
}catch(error){
  alert(error.message)
}
```



## div class 생성

function scope에서 this.$target으로 저장된 부분에 우리가 web에서 보여줄 내용들을 담았는데 

$app으로 정의되는 main tag 를 저장해서 이 아래에 this.$target에 div라는 class를 생성해서 $app에 this.$target을 

append 하도록 구성하는것이 인상적이었습니다. 

또, custom component 구현에 있어서 setAttribute로 class를 추가해주는것이 코드의 가독성을 높히는데 무척 효과적이었습니다. 

```
this.$target = document.createElement('div')

$app.appendChild(this.$target);
this.$target.setAttribute('data-component-type', 'TodoList');

```



## setTimeout의 활용

setTimeout을 이용해서 데이터를 새롭게 set 하고 싶을 경우에 어떻게 해야할지? 

setTimeout을 사용하게 되면 interval을 두고 값을 변경할 수 있었습니다.

```
setTimeout(()=>{
    todoList.setState([
      ...data,
      {
        text:"first"
      }
    ])

    setTimeout(()=>{
      todoList.setState([
        ...data,
        {
          text:"second"
        }
      ])
    },2000);
  },2000);
```

