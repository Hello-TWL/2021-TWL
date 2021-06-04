## 시작

생각 외에 많은 이슈들이 발생해서 해결하는데 시간이 걸렸습니다. 

기록해 두고, 다음에 배포할 땐 오류를 최소화 하기 위해 작성합니다. :(



## 개요

Spring boot project를 클라우드로 배포하는 과정을 수행합니다.



## CentOS

GCP 이하 Google Cloud Platform 에서 운영체제 CentOS(ver7)을 선택하였습니다.



## 배포하기 위한 작업들

**가상 머신** : centos 환경설정 → java 11버전, mvn 설치 

**Spring Project** : spring project git에 commit & push, centos에 접속 후 git clone 후 mvn package

**Google Cloud Platform** : firewall 8080 port open

 

## 발생했던 이슈들 

1) cnetOS에서 java8 버전으로 설정하고 Spring으로 mvn package 시 pom.xml 에 등록된 java 버전이 일치하지 않아 build가 수행X 

→ alternatives --config java 



![img](https://blog.kakaocdn.net/dn/BJNps/btq6u1MzhZ3/l7dFR9iaNEpGEK2RwMv0g0/img.png)Java 11로 변경



2) Error. A JNI error has occured, please check your installation and try again

프로젝트의 JDK 버전과 STS4 버전과 맞지 않아서 발생하는 문제입니다. 

→ Preferences - Compiler - JDK Compliance - Compiler compliance level : 11 



![img](https://blog.kakaocdn.net/dn/czOukz/btq6qh4rznf/3fuUVioILqp2KEiLqva0e1/img.png)



3) Please refer to dump files (if any exist) [date].dump, [date]-vmRun[N].dump and [date].dumpstream. site:stackoverflow.com
Caused by: org.apache.maven.plugin.MojoFailureException: There are test failures.
→ POM 버전을 업데이트 해서 해결할 수 있었습니다.



![img](https://blog.kakaocdn.net/dn/cVSeQf/btq6sdfWNwX/H1fMd9DGnzDwpWUA54l8N0/img.png)



 

4)sqlsessionfactory 이슈 

화면을 보면 아시다싶이 가장 큰 원인은 sqlSessionFactory를 생성하지 못하는 문제였습니다. 



![img](https://blog.kakaocdn.net/dn/lJHxa/btq6uH8D8L8/4mBgRWHjpQeEtVbK7KsNB1/img.png)



**sessionFactory**에서 Object를 불러오기전에 Mapper를 set 하는 부분이 있는데 classpath 경로로 되어있었습니다. 

해당 이슈는 mapper xml 을 읽지 못하고 Exception 을 뿜는 경우입니다. 

검색을 해보니 classpath와 classpath* 경우에 따라 쓰임이 다른것을 확인할 수 있었습니다. 

이 둘의 차이를 알아보니

**classpath** 로만 작성하면 현재 프로젝트의 리소스만 선택하게 되고

**classpath\*** 작성하게 되면 현재 프로젝트에 참조된 모든 jar를 전부 검색해서 리소스를 선택하게 됩니다. 

따라서, jar 파일의 classpath 디렉토리까지 확인할려면 classpath*를 사용해줘야 했습니다. 



![img](https://blog.kakaocdn.net/dn/44s33/btq6sd70heq/865eSiSeCMaHjb0rQTOC80/img.png)



 

java -jar OO.jar build 시 성공!



![img](https://blog.kakaocdn.net/dn/b1YcZF/btq6sjAz4yg/61K85VEliv8609bOOJ4idK/img.png)

![img](https://blog.kakaocdn.net/dn/bwNYn7/btq6wahXL4r/sty4kaodW8P43w6M6ktDVK/img.png)http://외부ip:8080/swagger-ui.html#/