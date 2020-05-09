







# 1 사전 준비 사항



- MachineLearningNotebooks git 다운로드

```shell
git clone https://github.com/Azure/MachineLearningNotebooks.git
```









## 1-1 설치 라이브러리

- python lib 설치 requirements 파일 참조 
- python 버젼 3.6 사용 

```python
# install just the base SDK
pip install azureml-sdk

# below steps are optional
# install the base SDK, Jupyter notebook server and tensorboard
pip install azureml-sdk[notebooks,tensorboard]

# install model explainability component
pip install azureml-sdk[explain]

# install automated ml components
pip install azureml-sdk[automl]

# install experimental features (not ready for production use)
pip install azureml-sdk[contrib]


# clone the sample repoistory
git clone https://github.com/Azure/MachineLearningNotebooks.git

```



- SDK 설치 

 [SDK installation instructions](https://docs.microsoft.com/azure/machine-learning/service/how-to-configure-environment)

- 기본적인 추가 라이브러리

```
(myenv) $ conda install -y matplotlib tqdm scikit-learn
```

- ACI 등록 설정이 되어 있지 않을 경우 아래 스크립트 수행

```shell
# check to see if ACI is already registered
(myenv) $ az provider show -n Microsoft.ContainerInstance -o table
# if ACI is not registered, run this command.
# note you need to be the subscription owner in order to execute this command successfully.
(myenv) $ az provider register -n Microsoft.ContainerInstance
```



Ipython 환경 설치 및 활성화

Ipykenel 설치 및 등록을 하지 않으면 python conda 환경으로 notebook 실행 시 오류 발생 

```python
pip install ipykernel

# powershell
ipython kernel install --user --name tonne_aml --display-name "Python (myenv)"

python -m ipykernel install --user --name tonne_aml --display-name "Python (toone_aml)"
```


- 전체 환경 설정 확인 [Install the Azure Machine Learning SDK](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-create-workspace-with-python)




# 2. Initialize Workspace

(참조) MachineLearningNotebooks 

```python
# Azure resources
subscription_id = "e478b470-4e14-4384-bc05-0e03fe0c2d9e"
resource_group = "HO_aml"  
workspace_name = "tooneaml"  
workspace_region = "Korea Central" 
```

```
ws = azureml_utils.get_or_create_workspace(
    config_path=config_path,
    subscription_id=subscription_id,
    resource_group=resource_group,
    workspace_name=workspace_name,
    workspace_region=workspace_region,
)
```





연결 설정을 하는 방법은 4가지 존재  
로컬 상에서 진행 시에는 1번 사용  
2번은 일회성  
3, 4번은 한번 인증 후 지속적으로 활용하는 MLOps에 적합

1. Interactive Login Authentication
2. Azure CLI Authentication
3. Managed Service Identity (MSI) Authentication
4. Service Principal Authentication

## 2-1 Interactive Login Authentication

[Azure Machine Learning 리소스 및 워크 플로에 대한 인증 설정](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication)

```python
from azureml.core import Workspace
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication(tenant_id="a9c21675-0cc8-4dd7-9818-d531b9ee2486")

ws = Workspace(subscription_id="e478b470-4e14-4384-bc05-0e03fe0c2d9e",
               resource_group="HO_aml",
               workspace_name="tooneaml",
               auth=interactive_auth)

```

테넌트 아이디는 Auzre Active Directory 개요에서 확인  


다운 받은 cofig.json 파일을 사용하여 연결 설정. 
```python
from azureml.core import Workspace
ws = Workspace.from_config(path=".file-path/ws_config.json")
```



### 2-2 Azure CLI Auth



```shell
az ad sp create-for-rbac --sdk-auth --name ml-auth
```



```sh
az ml workspace share -w your-workspace-name -g your-resource-group-name --user your-sp-object-id --role owner
```





# 3. datastore datasets

- 데이터 스토어를 신규로 만드는 것도 가능 

```python
from azureml.core.dataset import Dataset

datastore = ws.get_default_datastore()
datastore.upload(src_dir=data_dir, target_path=blobstore_datadir,
                    overwrite=True)
```



- 해당 데이터 스토어에서 필요한 데이터에 대해 datasets으로 지정

```python
train_dataset = Dataset.Tabular.from_delimited_files(path = [(datastore, blobstore_datadir + '/train_data.csv')])
```





# 4. Expirements / Run 설정

collection of trials( individual model runs )

- create experiments
- create run configuration
- create scriptrunconfig
- submit



[AML 실험 실행 및 메트릭 모니터링](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-track-experiments)

[Azure Machine Learning 실험을위한 파일을 저장하고 쓰는 위치](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-save-write-experiment-files)



- `./outputs`및 `./logs`폴더에 쓸 때 파일은 실행 기록에 자동으로 업로드되므로 실행이 완료되면 해당 파일에 액세스 할 수 있습니다.





### 3-1 strat logging

```python
from azureml.core import Experiment

# Get an experiment object from Azure Machine Learning
experiment = Experiment(workspace=ws, name="train-within-notebook")

# Create a run object in the experiment
run =  experiment.start_logging()
# Log the algorithm parameter alpha to the run
run.log('alpha', 0.03)

# Create, fit, and test the scikit-learn Ridge regression model
regression_model = Ridge(alpha=0.03)
regression_model.fit(data['train']['X'], data['train']['y'])
preds = regression_model.predict(data['test']['X'])

# Output the Mean Squared Error to the notebook and to the run
print('Mean Squared Error is', mean_squared_error(data['test']['y'], preds))
run.log('mse', mean_squared_error(data['test']['y'], preds))

# Save the model to the outputs directory for capture
model_file_name = 'outputs/model.pkl'

joblib.dump(value = regression_model, filename = model_file_name)

# upload the model file explicitly into artifacts 
run.upload_file(name = model_file_name, path_or_stream = model_file_name)

# Complete the run
run.complete()
```



### 3-2 RunCofnguration

- 실험에서 학습 실행을 제출 하는 데 필요한 실행 환경 설정을 캡슐화 합니다

```python
from azureml.core import ScriptRunConfig, RunConfiguration, Experiment

# create or load an experiment
experiment = Experiment(workspace, "MyExperiment")
# run a trial from the train.py code in your current directory
src = ScriptRunConfig(source_directory='./', script='train.py',
    run_config=RunConfiguration())
run = experiment.submit(src)
```

로컬 실행
```python
from azureml.core import ScriptRunConfig
import os 

script_folder = os.getcwd()
src = ScriptRunConfig(source_directory = script_folder, script = 'train.py', run_config = run_local)
run = exp.submit(src)
run.wait_for_completion(show_output = True)
```


###  3-2 tracking and monitoring experiments

run 객체에 대해 start_logging()함수로 시작 

라이브러리 설치 
```python
conda install -y tqdm matplotlib
```


###  모델 메트릭 추적
[MLflow 및 AML을 사용하여 모델 메트릭 추적](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-mlflow)





# 5. Environment

- 프로젝트의 소프트웨어 종속성을 추적하고 재현 가능
- AML은 환경을 Docker 이미지 및 conda 환경으로 빌드
- 후속 교육 실행 및 서비스 엔드 포인트 배포에서 재사용 할 수 있도록 환경을 캐시 ( ACR )
  ![test](https://docs.microsoft.com/en-us/azure/machine-learning/media/concept-environments/ml-environment.png)

환경 리스트 확인 

```python
envs = Environment.list(workspace=ws)

for env in envs:
    if env.startswith("AzureML"):
        print("Name",env)
        print("packages", envs[env].python.conda_dependencies.serialize_to_string())
```

conda or pip 로 custom 환경 구성

custom 환경을 구성 할 경우 반드시 모델을  initailizing / running 하기 위한 python 코드를 포함 시켜야함. 

```python
# From a Conda specification file
myenv = Environment.from_conda_specification(name = "myenv",
                                             file_path = "path-to-conda-specification-file")

# From a pip requirements file
myenv = Environment.from_pip_requirements(name = "myenv"
                                          file_path = "path-to-pip-requirements-file")

# 구성되어 있는 conda 환경으로 만들기
myenv = Environment.from_existing_conda_environment(name = "myenv",
                                                    conda_environment_name = "mycondaenv")



```

기존 환경에 추가

```python
from azureml.core.environment import Environment
from azureml.core.conda_dependencies import CondaDependencies

myenv = Environment(name="myenv")
conda_dep = CondaDependencies()

# Installs numpy version 1.17.0 conda package
conda_dep.add_conda_package("numpy==1.17.0")

# Installs pillow package
conda_dep.add_pip_package("pillow")

# Adds dependencies to PythonSection of myenv
myenv.python.conda_dependencies=conda_dep
```

conda dependencies 등을 활용 deploy 할 환경을 구성

```python
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies


environment = Environment('my-sklearn-environment')
environment.python.conda_dependencies = CondaDependencies.create(pip_packages=[
    'azureml-defaults',
    'inference-schema[numpy-support]',
    'joblib',
    'numpy',
    'scikit-learn'
])

```

 *환경 구성 없이 submit을 할경우 자동으로 현재 구성을 참조 하여 환경을 구성하지만 시간이 오래 걸림.*

 - 환경 등록 하기 

 ```python
 myenv.register(workspace=ws)
 ```

- 환경 가져 오기

```python
restored_environment = Environment.get(workspace=ws,name="myenv",version="1")
```

- run 객체로 부터 환경 가져 오기

```python
from azureml.core import Run
Run.get_environment()
```




# 6. compute target 설정

#### 4-1 AML Compute 생성

```python
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

# choose a name for your cluster
cluster_name = "cpu-cluster"

try:
    cpu_cluster = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing compute target')
except ComputeTargetException:
    print('Creating a new compute target...')
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2', max_nodes=4)

    # create the cluster
    cpu_cluster = ComputeTarget.create(ws, cluster_name, compute_config)

    # can poll for a minimum number of nodes and for a specific timeout. 
    # if no min node count is provided it uses the scale settings for the cluster
    cpu_cluster.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)

# use get_status() to get a detailed status for the current cluster. 
print(cpu_cluster.get_status().serialize())
```

```python

compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_NC24s_v3', min_nodes=0,     max_nodes=8)

# create the cluster
gpu_compute_target = ComputeTarget.create(ws, gpu_cluster_name, compute_config)
gpu_compute_target.wait_for_completion(show_output=True)

estimator = PyTorch(source_directory=project_folder,
                 compute_target=gpu_compute_target,
                 script_params = {...},
                 entry_script='run_squad.azureml.py',
                 node_count=node_count,
                 process_count_per_node=process_count_per_node,
                 distributed_backend='mpi',
                 use_gpu=True)
```


#### 


# 7. Inference Configuration
- custom env 를 구성할 경우 모델 배포 시 interence conf 필요

```python
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
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

service = Model.deploy(workspace=ws,
                       name=service_name,
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=aci_config)
service.wait_for_deployment(show_output=True)
```

# 8. model 

- local 환경에서 실험 실행 시 output 저장 경로

C:\Users\jilee\AppData\Local\Temp\azureml_runs\demo-040-exp_1587534816_ece19187\outputs

- 수행 시 자동으로 pkl 파일 생성  ( 모든 run에 각각의 pkl 파일이 생성 )






### 1. 모델 등록

1. Run 객체로 부터 생성된 모델을 등록

```python
description = 'My AutoML Model'
model = run.register_model(description = description,
                               tags={'area': 'mnist'})

print(run.model_id)
```

2. model 파일을 통한 등록 

```python
# Register model
model = Model.register(workspace = ws,
                        model_path ="mnist/model.onnx",
                        model_name = "onnx_mnist",
                        tags = {"onnx": "demo"},
                        description = "MNIST image classification CNN from ONNX Model Zoo",)

```

3. model 파일 등록 (sample_input_dataset output)

```python
from azureml.core import Model
from azureml.core.resource_configuration import ResourceConfiguration


model = Model.register(workspace=ws,
                       model_name='my-sklearn-model',                # Name of the registered model in your workspace.
                       model_path='./sklearn_regression_model.pkl',  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version='0.19.1',             # Version of scikit-learn used to create the model.
                       sample_input_dataset=input_dataset,
                       sample_output_dataset=output_dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='Ridge regression model to predict diabetes progression.',
                       tags={'area': 'diabetes', 'type': 'regression'})

print('Name:', model.name)
print('Version:', model.version)
```



### 2. model profiling 

CPU usage, memory usage, and response latency



At this point we only support profiling of services that expect their request data to be a string, for example: `string serialized json, text, string serialized image, etc.` The content of each row of the dataset (string) will be put into the body of the HTTP request and sent to the service encapsulating the model for scoring.









### 3. model packaging



```python
package = Model.package(ws, [model], inference_config)
package.wait_for_creation(show_output=True)  # Or show_output=False to hide the Docker build logs.
package.pull()
```

```python
package = Model.package(ws, [model], inference_config, generate_dockerfile=True)
package.wait_for_creation(show_output=True)
package.save("./local_context_dir")
```




### 4. Explain Models

- Explain the entire model behavior or individual predictions on your personal machine locally.
- Enable interpretability techniques for engineered features.
- Explain the behavior for the entire model and individual predictions in Azure. 
- Use a visualization dashboard to interact with your model explanations.
- Deploy a scoring explainer alongside your model to observe explanations during inferencing.


```python
pip install azureml-interpret
pip install azureml-contrib-interpret

```



# 9. deploy

1. Register model
2. Deploy the image as a web service in a local Docker container.
3. Quickly test changes to your entry script by reloading the local service.
4. Optionally, you can also make changes to model, conda or extra_docker_file_steps and update local service

### 1. Default deploy

```python
from azureml.core import Webservice
from azureml.exceptions import WebserviceException


service_name = 'demo-07-sklearn-service'

# Remove any existing service under the same name.
try:
    Webservice(ws, service_name).delete()
except WebserviceException:
    pass


# 일반 배포시 default 환경으로 배포가 진행 
service = Model.deploy(ws, service_name, [model])
service.wait_for_deployment(show_output=True)
```



### 2. use Custom environment  to ACI

- custom env 를 생성하게 되면 반드시 모델을 초기화 하고 실행 (initializing and runnig ) 할 수 있는 python 코드를 제출해야함.  `inferenceConfig` 임. 

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
aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

service = Model.deploy(workspace=ws,
                       name=service_name,
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=aci_config)
service.wait_for_deployment(show_output=True)
```




### 3. AKS deploy

- Provision the AKS Cluster
- Create AKS Cluster in an existing virtual network
- Enable SSL on the AKS Cluster 
- Attach existing AKS cluster

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
existing VNET에 배포하기  
- 실험과 관련된 저장소 부터 실제 실행을 위한 리소스( AKS AMLcompute 등) 에 대한 VNET 연결 설정   
[Secure Azure ML experimentation and inference jobs within an Azure Virtual Network](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-enable-virtual-network#use-azure-kubernetes-service)







### 4. Service check



- webservice 를 통해 결과 확인 

```  python
input_payload = json.dumps({
    'data': [
        [ 0.03807591,  0.05068012,  0.06169621, 0.02187235, -0.0442235,
         -0.03482076, -0.04340085, -0.00259226, 0.01990842, -0.01764613]
    ]
})

output = service.run(input_payload)

print(output)

```

- ACI 상에 배포된 결과 

![image-20200426013950513](C:\Users\jilee\AppData\Roaming\Typora\typora-user-images\image-20200426013950513.png)








# Monitor data drift on models deployed to Azure Kubernetes service

- dataset 등록 
- model 등록

dataset을 같이  model 등록하게 되면 해당 dataset에 대해서 자동적으로 capture 를 하게 됨. 

- ##### AML을 통해 AKS에 배포된 모델에 입력되는 데이터를 모니터링 하여 학습 데이터와의 드리프트 계수라고하는 데이터 드리프트의 크기를 측정합니다.
- ##### 기능별로 데이터 드리프트 기여도를 측정하여 데이터 드리프트를 일으킨 기능을 나타냅니다.
- ##### 거리 측정 항목을 측정합니다. 현재 Wasserstein과 Energy Distance가 계산됩니다.
- ##### 피처 분포를 측정합니다. 현재 커널 밀도 추정 및 히스토그램.
- ##### 이메일로 데이터 드리프트에 경고를 보냅니다.


```python
# preview
pip install azureml-datadrift
```

