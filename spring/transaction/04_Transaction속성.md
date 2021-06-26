# 04_ @Transaction 속성



## Isolation(격리레벨)

예) `@Transactional(isolation=Isolation.DEFAULT)`



- `DEFAULT` : DB설정, 기본 격리 수중
- `SERIALIZABLE` : 가장 높은 격리, 성능저하 우려
  데이터의 일관성 및 동시성을 위해 MVCC(multi Version Concurrency Control)을 사용하지 않음. 트랜잭션이 완료될 떄까지 SELECT문장이 사용하는 모든 데이터에 `shared lock`이 걸리므로 다른 사용자는 그 영역에 해당되는 데이터에 대한 수정 및 입력이 불가능
  (`phantom Read` 방지)

> MVCC란? 
> 다중 사용자 데이터베이스 성능을 위한 기술로 데이터조회시 LOCK을 사용하지 않고 데이터의 버전을 관리해 데이터의 일관성 및 동시성을 높이는 기술
>
> ** 이 부분은 추후 더 공부를 해야할 것 같음



- `READ_UNCOMMITED` : 커밋되지 않은 데이터에 대한 읽기를 허용 (`Dirty Read` 발생 가능)

- `READ_COMMITED`: 커밋된 데이터에 대한 읽기 허용(`Dirty Read` 방지)
- `REPEATEABLE_READ`: 동일 필드에 대해 다중 접근 시 모두 동일한 결과 보장.
트랜잭션이 완료 될때까지 SELECT쿼리가 사용하는 모든 데이터에 shared lock이 걸리므로 다른 사용자는 그 영역에 해당되는 데이터에 대한 수정이 불가능하다.

=> 선행 트랜잭션이 읽은 데이터는 트랜잭션이 종료될 떄까지 후행 트랜잭션이 갱신하거나 삭제가 불가능 하기 때문에, 같은 데이터를 두번 쿼리 했을 떄 일관성있는 결과를 리턴한다.(`Non-Repeatable Read` 방지)





## Propagation(전파속성)

예) `@Transational(propagation=Propagation.REQUIRED)`



- `PROPAGATION_MANDATORY` : 작업은 반드시 특정한 트랜잭션이 존재한 상태에서만 가능.
트랜잭션이 시작된 것이 없으면 새로 시작하는 대신 예외를 발생시킨다
(혼자 독립적으로 트랜잭션을 진행하면 안되는 경우 사용)
- `PROPAGATION_NESTED` : 기존에 트랜잭션이 있는 경우, 중첩 트랜잭션을 시작한다. 
> **중첩 트랜잭션?**
> 트랜잭션 안에 다시 트랜잭션을 만드는 것.
> 중첩된 트랜잭션은 먼저 시작된 부모 트랜잭션의 커밋과 롤백에는 영향을 받지만 자신의 커밋과 롤백은 부모 트랜잭션에 영향을 주지 않는다.

> 사용 예)
> - 어떤 작업 중 로그는 꼭 DB에 저장해야할 때
>
>   이 로그를 저장하는 작업이 실패한다고 메인 작업의 트랜잭션까지는 롤백되버린다면 특히 쇼핑몰에서 고객 주문작업 등의 경우 매출 하락까지도 발생할 수 있는 중요한 문제이다. 반대로 로그를 남긴 후 메인 작업에서 예외가 발생한다면 이때는 저장한 로그도 롤백 되어야 하는게 맞다.이럴 때 로그 작업을 메인 트랜잭션에서 분리해서 중첩 트랜잭션으로 만들어 두면 유용하게 사용할 수 있다. 이렇게 때문에 더욱 더 Business 로직을 잘 짜줘야 할 것이다
>
>   출처: https://goddaehee.tistory.com/167 


- `PROPAGATION_NEVER` : 트랜잭션을 사용하지 않도록 강제. 트랜잭션 실행되면 예외 발생

- `PROPAGATION_NOT_SUPPORTED`: 트랜잭션이 있는 경우에는 트랜잭션이 끝날때 까지 보류된 후 실행

- `PROPAGATION_SUPPORTS`: 이미 시작된 트랜잭션이 있으면 참여하고 그렇지 않으면 트랜잭션 없이 진행

- `PROPAGATION_REQUIRED`: 트랜잭션이 있으면, 그 상황에서 실행. 없으면 새로운 트랜잭션 실행(기본설정)

- `PROPAGATION_REQUIRED_NEW`: 항상 새로운 트랜잭션을 시작
  (이미 진행중인 트랜잭션이 있으면 트랜잭션을 잠시 보류)

  


## readOnly 속성

true인 경우, insert/update/delete 실행 시 예외 발생

기본은 false

### 사용 이유
- 성능 최적화
- 특정 트랜잭션 작업 안에서 쓰기 작업이 일어난 것을 의도적으로 방지


예) `@Transational(readOnly=true)`



## rollbackFor 속성

- 특정예외 발생 시, 강제로 RollBack (자주 쓰임)



예) `@Transactional(rollbackFor=Exception.class)`



## noRollbackFor 속성

- 특정 예외의 발생시, rollback 처리 되지 않음



예) `Transactional(noRollbackFor=Exception.class)`



## timeout 속성

지정 시간 내에 해당 메소드 수행이 완료되지 않은 경우 rollback 수행.

-1일 경우, notimeout(Default=-1)



예) `@Transactional(timeout=10)`

