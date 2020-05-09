# 0. 개발 환경 구성

- anaconda 다운로드 및 설치

https://docs.anaconda.com/anaconda/install/windows/

- conda env 생성

```python
create conda -n env_name python=3.6
activate env_name
```



- SDK 설치 

 [SDK installation instructions](https://docs.microsoft.com/azure/machine-learning/service/how-to-configure-environment)



- [`azureml-core`](https://docs.microsoft.com/python/api/azureml-core/?view=azure-ml-py)

- [`azureml-dataprep`](https://docs.microsoft.com/python/api/azureml-dataprep/?view=azure-ml-py)

- ```
  azureml-train
  ```

  - [`azureml-train-core`](https://docs.microsoft.com/python/api/azureml-train-core/?view=azure-ml-py)

- ```
  azureml-pipeline
  ```

  - [`azureml-pipeline-core`](https://docs.microsoft.com/python/api/azureml-pipeline-core/?view=azure-ml-py)
  - [`azureml-pipeline-steps`](https://docs.microsoft.com/python/api/azureml-pipeline-steps/?view=azure-ml-py)





# 1. 추가 설치 package



```python
# scrapbook 설치 
pip install seaborn

# beautifulsoup4 설치
pip install beautifulsoup4

# scikit learn
pip install scikit-learn
```



# 2.  workspace 생성

클라우드에서 머신 러닝 모델을 실험, 교육 및 배포하는 데 사용되는 기본 리소스입니다. Azure 구독 및 리소스 그룹을 쉽게 소비되는 개체에 연결합니다.

- portal -> create resource group -> create resource -> premium 

- ***workspace -> overview 상단의 config.json 파일 다운로드***

- SDK 생성

```python
from azureml.core import Workspace

ws = Workspace.create(name=workspace_name,
                      subscription_id=subscription_id,
                      resource_group=resource_group,
                      create_resource_group=True,
                      location=workspace_region
                     )
```



- 생성한 환경 파일을 재활용 하기 위해 파일 형태로 write

```python
ws.write_config(path="./file-path", file_name="ws_config.json")
```



# 3. initialize workspace



- 직접 정보 입력 하여 진행 

```python
from azureml.core import Workspace

ws = Workspace(subscription_id="e478b470-4e14-4384-bc05-0e03fe0c2d9e",
               resource_group="HO_aml",
               workspace_name="tooneaml")

```

- 다운로드 받은 파일을 통해 접속

```python
from azureml.core import Workspace
ws = Workspace.from_config(path="../tooneaml_config.json")
```



# 4. experiments

각각의 모델을 수행 하는 순서 

- create experiments
- create run configuration
- create scriptrunconfig
- submit





- 실험 등록

```python
from azureml.core.experiment import Experiment

# Choose an experiment name.
experiment_name = 'aischool-text-classification-exp-01'
experiment = Experiment(ws, experiment_name)

```



- 환경 출력

```python
output = {}
output['Subscription ID'] = ws.subscription_id
output['Workspace Name'] = ws.name
output['Resource Group'] = ws.resource_group
output['Location'] = ws.location
output['Experiment Name'] = experiment.name
pd.set_option('display.max_colwidth', -1)
outputDf = pd.DataFrame(data = output, index = [''])
outputDf.T
```



- workspace의 실험 리스트 출력

```python
list_experiments = Experiment.list(ws)
for exp in list_experiments:
    print(exp.id, exp.name)
```



# 5. compute target 설정

- compute target은 training compute 으로 생성 

```python 
from azureml.core.compute_target import ComputeTargetException

# Choose a name for your cluster.
amlcompute_cluster_name = "aischool-clu-01"

# Verify that cluster does not exist already
try:
    compute_target = ComputeTarget(workspace=ws, name=amlcompute_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(vm_size = "STANDARD_D2_V2", # CPU for BiLSTM, such as "STANDARD_D2_V2" 
                                                           # To use BERT (this is recommended for best performance), select a GPU such as "STANDARD_NC6" 
                                                           # or similar GPU option
                                                           # available in your workspace
                                                           max_nodes = 1)
    compute_target = ComputeTarget.create(ws, amlcompute_cluster_name, compute_config)

compute_target.wait_for_completion(show_output=True)
```



- 생성 가능한 vm size 확인

```python
list_vms = AmlCompute.supported_vmsizes(workspace=ws)
```





# 6. runconfiguration, scriptrunconfig, run

### . runconfiguration 설정 

- runconfiguration (compute_config) 설정

```python
from azureml.core import ScriptRunConfig, RunConfiguration

compute_config = RunConfiguration()

# Attach compute target to run config
compute_config.target = "amlcompute"
# runconfig.run_config.target = "local"

# compute_config.amlcompute.vm_size = "STANDARD_D1_V2"

from azureml.core.conda_dependencies import CondaDependencies

conda_dep = CondaDependencies()
#conda_dep.add_pip_package("scikit-learn")
#conda_dep.add_conda_package("numpy==1.17.0")
#conda_dep.add_pip_package("scikit-learn")
conda_dep.add_pip_package("nltk")
conda_dep.add_pip_package("pandas")
conda_dep.add_pip_package("matplotlib")

#conda_dep = CondaDependencies(conda_dependencies_file_path='./environment.yml', _underlying_structure=None)

compute_config.environment.python.conda_dependencies = conda_dep
```



- environment를 적용하여 runconfiguration 설정

```python
from azureml.core import ScriptRunConfig, RunConfiguration
from azureml.core.environment import Environment

aienv = Environment.from_existing_conda_environment(name = "aienv",
                                                    conda_environment_name = "toone_aml"

compute_config = RunConfiguration()

# Attach compute target to run config
compute_config.target = compute_target
# runconfig.run_config.target = "local"

# compute_config.amlcompute.vm_size = "STANDARD_D1_V2"


compute_config.environment = aienv
```



### scriptrunconfig 설정

- train 스크립트와 runconfiguration 으로  runconfiguration 설정

```python
from azureml.core import ScriptRunConfig, RunConfiguration

# run a trial from the train.py code in your current directory
src = ScriptRunConfig(source_directory='./', script='train.py',
    run_config=RunConfiguration())

```



### Run 객체

런은 실험의 단일 시도를 나타냅니다. expriments 를 제출하면서 해당 실험을 run 객체로 받게 됩니다. 

이후 Run 객체를 통해 비동기 적으로 진행 되는 실행을 모니터링 하며 결과를 분석 기록 합니다. 

- 실험 실행 전 run 객체 생성 시 logging 시작

```python
run =  experiment.start_logging()
```



- 실험 실행 환겨을 제출 하면서 해당 실험을 run 객체로 받음

```python
tags = {"prod": "phase-1-model-tests"}
run = experiment.submit(config=src, tags=tags)
```



- run의 세부 적인 사항 확인

```python
run_details = run.get_details()
```



- widgets을 통해 run 상태 확인 

```python
from azureml.widgets import RunDetails  
RunDetails(run).show()
```



- run list 조회 

```python
list_runs = experiment.get_runs()
for run in list_runs:
    print(run.id, run.name)
```



# 7. model registry

모델 등록을 사용하여 작업 영역에서 Azure 클라우드에 모델을 저장하고 버전을 지정할 수 있습니다. 등록 된 모델은 이름과 버전으로 식별됩니다. 기존 모델과 이름이 같은 모델을 등록 할 때마다 레지스트리가 버전을 증가시킵니다. Azure Machine Learning은 Azure Machine Learning 모델뿐만 아니라 Python 3을 통해로드 할 수있는 모든 모델을 지원합니다.



- model 생성 후 outputs 폴더에 저장 하면 AML로 자동으로 업로드 됨

```python
model_file_name = 'aischool_model.pkl'
with open(model_file_name, "wb") as file:
    joblib.dump(value=pipeline, filename=os.path.join('./outputs/', model_file_name))
```



- Run 객체로 부터  model 저장

```python
model = run.register_model(model_name = "aischool_model", model_path = "/outputs/aischool_model.pkl", tags={'area': 'mnist'})
```



- 생성되어 있는 모델을 통해 등록

```python
# Register model
model = Model.register(workspace = ws,
                        model_path ="mnist/model.onnx",
                        model_name = "onnx_mnist",
                        tags = {"onnx": "demo"},
                        description = "description",)

```



- 모델을 로컬로 다운로드 

```python
from azureml.core.model import Model
import os

model = Model(workspace=ws, name="churn-model-test")
model.download(target_dir=os.getcwd())
```



### Explain Models

- 


```python
pip install azureml-interpret
pip install azureml-contrib-interpret

```





# 8. Depoly ( ACI, AKS )

### Environment 정의

Azure Machine Learning 환경은 학습 및 스코어링 스크립트와 관련된 Python 패키지, 환경 변수 및 소프트웨어 설정을 지정합니다.

- 훈련 스크립트를 개발하십시오.
- 대규모 모델 교육을 위해 Azure Machine Learning Compute에서 동일한 환경을 재사용하십시오.
- 특정 컴퓨팅 유형에 묶이지 않고 동일한 환경으로 모델을 배포하십시오.



- environment 생성

```python
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies


env = Environment('my-sklearn-environment')
env.python.conda_dependencies = CondaDependencies.create(pip_packages=[
    'azureml-defaults',
    'inference-schema[numpy-support]',
    'joblib',
    'numpy',
    'scikit-learn'
])
```



- environments 리스트 확인

```python
envs = Environment.list(workspace=ws)

for env in envs:
    if env.startswith("AzureML"):
        print("Name",env)
        print("packages", envs[env].python.conda_dependencies.serialize_to_string())
```



### Inference Configuration

- 추론 환경에 대한 정의 environment 와 entry_script를 포함 하여 설정 생성

```python
python
from azureml.core import Webservice
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice
from azureml.exceptions import WebserviceException


service_name = 'my-custom-env-service'

# Remove any existing service under the same name.
try:
    Webservice(ws, service_name).delete()
except WebserviceException:
    pass

inference_config = InferenceConfig(entry_script='score.py', environment=environment)

```



### ACI 배포

```python
from azureml.core.webservice import AciWebservice
from azureml.exceptions import WebserviceException

aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

service = Model.deploy(workspace=ws,
                       name=service_name,
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=aci_config)
service.wait_for_deployment(show_output=True)
```





### AKS 배포

```python
from azureml.core.compute import AksCompute, ComputeTarget

# Use the default configuration (can also provide parameters to customize)
prov_config = AksCompute.provisioning_configuration()

aks_name = 'my-aks-9' 
# Create the cluster
aks_target = ComputeTarget.create(workspace = ws, 
                                  name = aks_name, 
                                  provisioning_configuration = prov_config)
```







# reference

[Python 용 Azure Machine Learning SDK 란 무엇입니까?](https://docs.microsoft.com/en-us/python/api/overview/azure/ml/?view=azure-ml-py)