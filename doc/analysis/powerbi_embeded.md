# 0. 연결 방식



- 기본적으로는 power bi pro 라이센스를 가진 마스터 계정을 통해 배포
- service principal을 통해 토큰을 통해 연결 하는 방식 존재





[학습서 : 고객을위한 애플리케이션에 Power BI 컨텐츠 임베드](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-sample-for-customers)



# 1. Service Principal 생성

tutorial

[학습서 : 고객을위한 애플리케이션에 Power BI 컨텐츠 임베드](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-sample-for-customers)





[서비스 주체 및 응용 프로그램 암호를 사용하여 Power BI 콘텐츠 임베드](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal)



1. AD app 생성

2. secret 생성 

   app id : d3e58e09-32d2-4af2-810a-854d5b9991c4

   secret : O@@1mDY/9kKcgDRN8zE:wLhFs9-X4wd0



실제 적용을 위해서 반드시 프로 라이센스 계정이 하나는 있어야 하는것인지 확인. 

[서비스 주체 및 응용 프로그램 암호를 사용하여 Power BI 콘텐츠 임베드](https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal)