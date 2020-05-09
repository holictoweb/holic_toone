

# 0. 환경 구성



- visual studio 확장 설치

https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects





# Deploy process



###### 1. 배포하면 **서버** 속성에 지정된 인스턴스에 연결됩니다 . 

###### 2. **데이터베이스** 인스턴스에 지정된 이름의 새 모델 데이터베이스 또는 데이터 세트 가없는 경우 해당 인스턴스에 작성됩니다. 

###### 3. 모델 프로젝트의 Model.bim 파일의 메타 데이터는 배포 서버의 모델 데이터베이스에서 개체를 구성하는 데 사용됩니다

##### 4. **처리 옵션을** 사용하면 모델 `메타 데이터 만 배포`할지, `모델 데이터베이스를 생성`하는지 또는 **기본** 또는 **전체** 인지를 지정할 수 있습니다

###### 5. 데이터 소스에 연결하는 데 사용되는 가장 자격 증명이 메모리 내 모델 작업 공간 데이터베이스에서 배포 된 모델 데이터베이스로 전달됩니다. 

###### 6. Analysis Services는 처리를 실행하여 배포 된 모델에 데이터를 채 웁니다. 







##### 1. [web designer 중단](https://azure.microsoft.com/en-us/updates/azure-analysis-services-web-designer-to-be-discontinued/)

Azure Portal 의 Azure Analysis Services [웹 디자이너](https://analysisservices.azure.com/)  2018 년 10 월에 폐기되어 향후 어느 시점에 중단 될 수 있습니다. 완전히 중단하지 않으려 고 노력했지만 특정 규정 준수 요구 사항으로 인해 2019 년 3 월 1 일부터 포털에서 제거 될 예정입니다.

웹 디자이너 대신 Azure Analysis Services 모델을 작성하고 관리하기 위해 SQL Server Data Tools 및 SQL Server Management Studio를 사용하는 것이 좋습니다.

`PBIX에서 가져 오기 기능에 대한 대안은 현재 없습니다. 이 기능은 처음부터 안정성 문제가 있었지만 모델링 도구로 Power BI Desktop의 인기로 인해 크게 사용되었습니다`. 우리는 Power BI와 Analysis Services 간의 격차를 해소 할 수있는 더 우수하고 강력한 방법을 연구하고 있습니다. 아직 발표 할 일정이나 세부 사항은 없지만 최대한 빨리 더 많은 정보를 공유 할 것입니다.