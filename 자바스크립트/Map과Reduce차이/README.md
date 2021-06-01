## Map vs Reduce

Map의 경우에 **Array.map((요소, 인덱스, 배열) => { return 요소 });** 실행하는 배열과 결과로 나오는 배열이 서로 다른 객체가 됩니다. 

즉, 배열을 1대1로 매핑하게 되기 때문에 기존 객체를 수정하지 않는 메소드라고 정리할 수 있습니다. 

GIST

https://gist.github.com/lllilllilllilili/65c10eaf1cbcf1c2b12f38a4813089fa.js



Reduce의 경우에는 **Array.reduce((누적값, 현재값, 인덱스) => {return 결과값}, 초기값)** 의 구조로 사용할 수 있습니다. 

일반적으로 Reduce는 누적값을 구하는데 사용할 수 있지만, 데이터를 조회하며 리듀스 함수(콜백함수)를 실행합니다.

이를 통해 배열 형태에서 원하는 형태로 값을 변환시키고 filter, sort, every 등의 기능으로 활용해서 사용할 수 있습니다. 

GIST

https://gist.github.com/lllilllilllilili/9a3b1625aa9bc973e13e1b03026670bf.js



Map의 경우 비교적 간단한 로직에서 간결하게 사용할 수 있으나

상황에 따라 Map 외에 다른 Filter 함수를 불러와 2번(Map - 1회, Filter - 2회) 사용해야할 작업을

reduce를 사용하게 되면 한번에 처리할 수 있는 등의 장점이 생깁니다. (*reference : https://2ham-s.tistory.com/289 )