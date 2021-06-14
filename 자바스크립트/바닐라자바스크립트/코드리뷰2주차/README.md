## 코드리뷰 2주차



## 시작

js코드를 작성하면서 기존에 알고있던대로 작성하다 굉장히 삽질을 많이했다. ❗️❗️

그래서 구글링과 다른 사람들의 코드를 참조하며 과제를 수행했다. 📌

Component 단위로 작성하는 과정은

데이터의 갱신과 같은 Component간의 독립적이지만서도 연관되어 있는 부분이 존재한다면 이를 처리하기가 여간 번거로운것이 아니다. 

여기서 오는 과정과 해결방법들에 대해 나는 어떻게 해결했는지, 다른 사람들의 코드는 어떤지 한번 살펴볼것이다. ✔️

##  

## 삽질1

삽질의 시작은 Component에서 데이터갱신에 대한 처리방법이다. 

todolist 데이터를 갱신처리하는 부분에서

```
this.handleSubmit = (event) =>{
      event.preventDefault();
      const curValue = todoInput.value;
      //alldata(curValue);

      const newData = [
        ...this.state
        ,{
        id : this.state.length+1,
        text : curValue,
        isCompleted : false
      }
    ];
      this.setState(newData);
      this.drawTodo(curValue);
      todoInput.value = '';
    }
    
```



newData를 handleSubmit안에 두고 값을 갱신했다. 이것은 나중에 한파일에 있었던 input Component를 분리하게 되면서 큰 골칫덩이가 된다. 

tag 관리를 엉망으로 했다. 보통의 경우 index.html 에는 최상위 tag에 id를 지정하여 이 tag 밑으로 Component를 append 하여 사용하곤 한다. 



나의 경우에는 index.html 에도 여러 tag를 두고 사용하고, Component에서도 tag를 생성하는 코드를 삽입하여 이 둘이 overlap이 되어 Dom 구조를 파악할 때 굉장히 헷갈렸다. 



```
const todoCount = document.querySelector('#todoCount');
const todoCompleted = document.querySelector('#todoCompleted');

- todolist.js

/////////////////////////////////////////////////////////////////

<div id="App"></div>
    <form id="todo-form">
      <input type="text" placeholder="할일을 입력해주세요."/>
    </form>
    <div id="todoCompleted"></div>
    <div id="todoCount"></div>
    <ul class="todoUl" id="todoList"></ul>
    
- index.html
```



## 삽질2

처음 구조에 대해 별 다른 생각이 접근하게 되면서 index.html 과 todolist.js에 태그를 혼용하여 사용하니 

input으로 입력받는 데이터들이 잘못된 태그에 삽입되어 이를 발견하는데 다소 시간이 걸렸다. 



아래 코드를 보게 되면 drawTodo에서 span 으로 값 과 ❌ 로 화면에 render가 된다. 



그런데 아래 보면 이미 render함수를 만들어두고 또 drawTodo를 생성하게 되니 render 되는 부분이 2개가 되고 tag도 2배가 되었다. 

이전 코드에서 기능을 추가하는것이라 render 함수가 있는것을 발견하지 못했던게 가장 큰 문제였지만, 

태그를 html과 .js 동시에 사용하게 되면 의도치 않게 중복 의도가 있는 코드를 작성할 확률이 크다는것을 새삼 느낄 수 있었다. 

```
this.drawTodo = (text) =>{
      const li = document.createElement('li');
      const span = document.createElement('span');
      const delBtn = document.createElement('button');
      li.id=this.state.length+1
      span.classList.add('complete_false');
      delBtn.classList.add('todoBtn');
      span.innerText = text;
      delBtn.innerText= "❌";
      li.appendChild(span);
      li.appendChild(delBtn);
      li.classList.add('todoli');
      todoList.appendChild(li);  
}
//////////////////////////////////////////////////////
 this.render = () =>{
                const todoHtmlStr = this.state.map(({id, text, isCompleted}) =>
                `<li id=${id} class="complete_${isCompleted}">
                 <span class="complete_false">${text}</span>
                 <span class="todoBtn">${'❌'}</span>
                 </li>`
               ).join('')
               this.$target.innerHTML=todoHtmlStr
}
```



## Component에서 유기적인 데이터 처리와 갱신

우선 각 기능을 수행하는 Component를 독립시키다 보니 데이터 갱신 처리가 문제가 되었다. 

어느 한곳에 정의하여 사용하기에는 javascript에서 부모 컴포넌트를 찾기 데이터를 전달할 수 있는 방법이 쉽지 않았기 때문이다.



그래서, github에서 공유된 다른 사람들의 코드를 살펴보니 Component의 파라미터로 또 함수를 전달해서 거기서 setState로 데이터를 갱신하고 있는것을 확인할 수 있었다. 

해당 코드를 살펴보고 있으니 전적으로 Component안에서만 처리해야 한다는 내 생각이 무척 단순했다는것을 다시금 느낄 수 있었다.

어쨋든, Component의 파라미터안에서 정의된 함수는 해당 Component에서 callback 되어 사용되며 실행시 setState로 이동하여 화면에 render되는 TodoList Component에서 값이 전달되어지게 된다. 

그리고 갱신된 값에 따라 화면이 render가 된다. 

```
//todoInput : 데이터를 받아올 인풋 컴포넌트
  this.todoInput = new TodoInput($target, (text) =>{
    const newData = [
      ...this.$state
      ,{
      id : this.$state.length+1,
      text : text,
      isCompleted : false
    }
  ];
  this.setState(newData);
  });

 this.setState = (nextState) =>{
      this.$state = nextState;
      localStorage.setItem("Todo", JSON.stringify(this.$state));
      this.todoList.setState(this.$state);
  }
```



![img](https://blog.kakaocdn.net/dn/bk7lwS/btq6N3RNmci/ByAYkctSMISwdVGoeEQN2K/img.png)동작원리



 

## 그래서 뭘 했는데?

구현 사항
\- [x] [미션2] TodoApp 업그레이드하기 #75
\- [x] [미션2] 보너스 구현사항 - input 컴포넌트화 하기 #76
\- [x] [미션2] 보너스 구현 사항 - TodoCount 컴포넌트 #77
\- [x] [미션2] 보너스 구현사항 - Event delegate #81
\- [x] [미션2] 보너스 구현 사항 - 커스텀 이벤트 #90
\- [x] [미션2] 보너스 구현사항 - localStorage #91

Dir 구조

```
11th
|-- components
|       `-- TodoCount.js
|       `-- TodoDeleteAll.js
|       `-- TodoInput.js
|       `-- TodoList.js
|-- App.js
|-- index.css
|-- index.html
|-- index.js
|--
```

노트
\- #75 처음 설계시에 App으로 컴포넌트를 관리하는것이 아니라, index.html에서 정의해논 tag를 불러와 Todolist에서 기능들을 구현해주었다.(drawTodo, deleteTodo) todo에 입력받은 데이터를 추가할 때 입력이 종료되는 trigger 발생 시 `기존 data를 destructuring + 입력 데이터 추가` 로 구현해주었다.
\- #76 input을 컴포넌트화 하게되면서 #75에서 todoList에서 입력 데이터를 추가하는 방법은 더이상 사용할 수 없었다. 한정원님의 코드를 참고해서 Component 생성 시 매개변수에 function을 추가해 App.js에서 입력 데이터에 대한 todolist 갱신을 처리할 수 있었다. 
\- #77 TodoList안에 TodoCount 컴포넌트를 구현해주었고, 넘어온 데이터를 카운팅하여 화면에 render 해주었다.
\- #81 앞서 설계한 코드에서 .html 에서 작성한 태그와 .js에서 생성한 태그들이 오버랩되면서 DOM 구조를 확인하는데 매우 혼란스러웠다. .js에서 태그를 생성하는것으로 모든 컴포넌트를 수정하였고, 처음 설계를 완전히 바꾸게 되었다. 오히려, .js에서 태그를 생성해서 root 역할을 하는 `id=App`에 컴포넌트를 추가해서 확인하니 구조가 눈에 확 들어오게 되었다. ul-li 구조로 구현을 수행하였고, ul에 event를 걸어두어 trigger시 class 이름으로 조건 분기 처리하여 closet으로 li.id를 확인해 Toggle과 Delete 기능을 구현하였다. 
\- #90 removeAll 이벤트를 생성하여, click시 removeAll로 만들어진 리스너로 디스패치하였고 함수의 인자로 넘겨받은 setState가 값을 초기화하도록 구현하였다. 
\- #91 데이터 처리 부분을 localStorage를 사용해 JSON구조로 값을 추가하였다.

