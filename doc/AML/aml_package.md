

# 0. package

- 기본 설치

```
azureml-sdk
```

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









| 추가  패키지 설치(`extras`) | 사용 사례 및 설치된 패키지                                   |
| :-------------------------- | :----------------------------------------------------------- |
| `accel-models`              | `azureml-accel-models`를 설치합니다. Azure ML 하드웨어 가속 모델 서비스를 사용하여 FPGA에서 심층 신경망을 가속화합니다. |
| `automl`                    | `azureml-train-automl` 및 기타 필수 종속성을 설치합니다. 자동화된 기계 학습 실험을 빌드하고 실행하는 클래스를 제공합니다. `automl` 추가 구성 요소는 `pandas`, `numpy` 및 `scikit-learn`을 포함한 일반적인 데이터 과학 패키지도 설치합니다. `automl`을 사용하는 방법에 대한 자세한 내용은 [추가 사용 사례 지침](https://docs.microsoft.com/ko-kr/python/api/overview/azure/ml/install?view=azure-ml-py#additional-use-case-guidance)을 참조하세요. |
| `contrib`                   | 실험 기능 또는 미리 보기 기능을 포함하는 `azureml-contrib-*` 패키지를 설치합니다. |
| `databricks`                | Azure Databricks 환경에서 작업할 때 호환성을 보장하기 위해 네이티브 패키지가 아닌 패키지를 설치합니다. **이 추가 구성 요소는 다른 구성 요소와 결합할 수 없습니다**. Azure Databricks 환경에서 SDK를 사용하는 방법에 대한 자세한 내용은 [추가 사용 사례 지침](https://docs.microsoft.com/ko-kr/python/api/overview/azure/ml/install?view=azure-ml-py#additional-use-case-guidance)을 참조하세요. |
| `explain`                   | `azureml-explain-model` 및 기타 필수 종속성을 설치합니다. 자동화된 모델 튜닝의 자세한 기능 중요도를 파악하는 클래스가 포함되어 있습니다. |
| `interpret`                 | 블랙박스 및 화이트박스 모델에 대한 기능 및 클래스 중요도를 포함하여 모델 해석에 사용되는 `azureml-interpret`를 설치합니다. |
| `notebooks`                 | `azureml-widgets` 및 기타 필수 종속성을 설치합니다. Jupyter Notebook 환경에서 대화형 위젯을 지원합니다. Jupyter Notebook에서 실행되고 있지 않거나(예: PyCharm에서 빌드하는 경우) 위젯을 사용할 필요가 없는 경우에는 설치할 필요가 없습니다. |
| `services`                  | `azureml-contrib-services`를 설치합니다. 원시 HTTP 액세스를 요청하는 스크립트를 채점하는 기능을 제공합니다. |
| `tensorboard`               | `azureml-tensorboard`를 설치합니다. 실험 실행 기록을 내보내고 실험 성능과 구조를 시각화하기 위해 TensorBoard를 시작하는 클래스와 메서드를 제공합니다. |



- 추가 기능 설치 방법

```python
pip install --upgrade azureml-sdk[explain,automl]
```



- 버젼 확인

```python
import azureml.core
print(azureml.core.VERSION)
```





- 개발도구

```python
pip install ipykernel
```







# 1. widget package

```python
pip install azureml-widgets
```



Jupyter 노트북에서 기계 학습 교육 실행의 진행률을 볼 수 있는 기능을 포함 합니다.

지원 되는 실행 형식에는 [StepRun](https://docs.microsoft.com/ko-kr/python/api/azureml-pipeline-core/azureml.pipeline.core.steprun?view=azure-ml-py), [PipelineRun](https://docs.microsoft.com/ko-kr/python/api/azureml-pipeline-core/azureml.pipeline.core.run.pipelinerun?view=azure-ml-py), [HyperDriveRun](https://docs.microsoft.com/ko-kr/python/api/azureml-train-core/azureml.train.hyperdrive.hyperdriverun?view=azure-ml-py)및 [AutoMLRun](https://docs.microsoft.com/ko-kr/python/api/azureml-train-automl-client/azureml.train.automl.run.automlrun?view=azure-ml-py)가 포함 됩니다. 지원 되는 실행 형식 및 환경에 대 한 자세한 내용은 [RunDetails](https://docs.microsoft.com/ko-kr/python/api/azureml-widgets/azureml.widgets.rundetails?view=azure-ml-py)를 참조 하세요.









# 2. tensorboard



`azureml-tensorboard`를 설치합니다. 실험 실행 기록을 내보내고 실험 성능과 구조를 시각화하기 위해 TensorBoard를 시작하는 클래스와 메서드를 제공합니다.