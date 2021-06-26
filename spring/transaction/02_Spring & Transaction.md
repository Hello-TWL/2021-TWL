# 02_ Spring과 Transaction



스프링은 코드기반의 트랜잭션(Programmatic Transaction) 처리 뿐만 아니라, 선언적 트랜잭션(Declarative Transaction)을 지원한다.



## 스프링에서 트랜잭션 처리방법



스프링이 제공하는 트랜잭션 템플릿 클래스를 이용하거나, 설정파일/어노테이션을 이용해서 트랜잭선의 범위 및 규칙을 정의할 수 있다



### 선언적 트랜잭션

- `<tx:advice>`태그
- `@Transactional` 어노테이션 (주로 사용)
- 

### @Transactional 처리 순서

1. 클래스, 메서드 위에 `@Transactional` 추가

2. 클래스 트랜잭션 기능이 적용된, 프록시객체 생성

3. 해당 프록시 객체는 `@Transactional`기능이 포함된, 메소드가 호출될 경우 `PlatformTransactionManager`을 사용하여, 트랜잭션을 시작
4. 정상 여부에 따라 Commit/Rollback 시행



## Transaction 적용

- xml 방식 : root-context.xml 

```xml
<!-- 트랜젝션 매니저 -->
<bean id="transactionManager"
	 class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource"></property>
</bean>
	
<!-- @Transactional 애노테이션을 sacn하기 위한 설정 -->
<tx:annotation-driven/>
```



- JavaConfig 방식

```java
@EnableTransactionManagement
public class TransationConfig {

	@Bean
	public PlatformTransactionManager tranasactionManager() throws Exception {
		return new DataSourceTransactionManager(dataSource());
	}
}
```





------



- 쿼리문을 처리하는 과정에서 에러가 났을 경우, 자동으로 Rollback처리를 해준다.

- 데이터 값을 추가/변경/삭제하는 경우 @Transactional을 추가하여, 트랜잭션을 설정한다.

