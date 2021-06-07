## New 인자가 없을 때 Error Handling

해당 내용에 대한 처리는 구글링을 통해 확인할 수 있었습니다. 

MDN에 따르면 **new.target** 속성은 함수 또는 생성자가 new 연산을 사용하여 호출되었는지 확인하게 됩니다. 

```
function TodoList(data, selector){
    
    this.state = data 
    
    Validation(this.state)
    //[Mission1] 보너스 new 키워드 안 붙이고 함수 실행 시 에러 발생하게 하기 
    if(!new.target){
        throw new Error('new로 객체를 생성해주세요');
}
```

