# QUERYDSL EXISTS 쿼리 성능 개선

`exists`는 주로 해당 조건의 데이터가 존재하는지 확인하기 위해 사용하는 경우가 있다.

이와, 비슷한 역할로는 `count`가 있다.

JPA EXISTS 쿼리 성능 개선에 대해 알기 위해서는 먼저 exists와 count의 성능 차이에 대해 알아야 한다.

## COUNT VS EXISTS
COUNT와 EXISTS의 역할은 비슷하지만, 데이터가 많이 적재되어 있을 때는 EXISTS의 성능이 훨씬 좋다.

EXISTS는 해당 조건과 일치하는 데이터가 있는 경우, 첫번쨰 결과에서도 바로 true를 리턴하지만, COUNT의 경우에는 전체에서 총 몇 건의 데이터가 조건에 부합하는지 확인 후 리턴한다. 그렇기 때문에, COUNT는 성능상 이슈가 생길 수 있다.

## QUERYDSL에서 exists
그런데, Querydsl에서 기본적으로 사용하는 exists는 성능상 이슈가 있는 count 쿼리 방식을 사용하고 있다.

```
@Override
public boolean exists(Predicate predicate) {
    return createQuery(predicate).fetchCount > 0;
}
```

그래서, 쿼리 구현시 다음과 같이 exists 쿼리를 직접 구현하는 것이 좋다
```
SELECT EXISTS (
    SELECT 1
      FROM USER
     WHERE NAME = :NAME
)
```

그런데, QUERYDSL은 from이 없으면 구문오류가 발생해 `SELECT EXISTS`사용할 수 없다. 
이에, QUERYDSL의 경우, EXISTS가 동작하듯이 전체를 조회하지 않고 첫번째 결과만 확인하여도 return 할 수 있도록 쿼리를 작성하는 것이 좋다.
-> LIMIT=1 로 구현

```
public Boolean existsByUsername(String username) {
    Integer result = queryFactory
                        .selectOne()
                        .from(user)
                        .where(user.username.eq(username))
                        .fetchFirst(); // LIMIT=1 과 동일 
    return result!=null;
}
```

**참고**
fetchFirst() == limit(1).fetchOne();