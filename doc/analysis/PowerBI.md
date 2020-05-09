# 0. 



#### 0. [Microsoft Power BI: Enterprise modeling with Power BI and Azure Analysis Services - BRK3064](https://www.youtube.com/watch?v=gJPgbJMC_HU)

4:12

self-hosted power bi + Azure analysis services = Power bi Premium 





# 1. 데이터 전처리 (ETL)

- 최초 데이터를 가져 올때 power query를 통해 원하는 데이터로 변환하는 작업을 정의 할 수 있음 
  - power query 는 다양한 리소스와의 연결을 지원함.
  - hadoop등에 대한 연결도 해당 커넥터를 통해 실제 쿼리 결과를 받을 수 있음.
-  power bi desktop을 사용할 경우 이 작을 위한 리소스 들 (용량 cpu)이 로컬에서 동작하게 됨
  - ETL 이후 스토리지 역시 pbix 파일에 포함되는 것인지 확인 필요 

- 운영 환경에서 대용량 데이터 처리 시에는 Data Factory를 통해 대체 가능한 부분





# 2. 모델링 

- DAX를 사용 하여 분석 하기 위한 모델링 작업을 진행 
- 모델링 해당 부분은 analysis service로 대체 가능하며 





# 3. 시각화

- 시각화 작업 진행

