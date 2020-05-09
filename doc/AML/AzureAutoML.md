# 0. reference



[자동 기계 학습 (AutoML)이란 무엇입니까?](https://docs.microsoft.com/en-us/azure/machine-learning/concept-automated-ml)

[Python에서 자동 ML 실험 구성](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-auto-train)

[studio에서 자동화 된 기계 학습 모델 만들기, 검토 및 배포](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-automated-ml-for-ml-models)

[automl 전처리](https://docs.microsoft.com/en-us/azure/machine-learning/concept-automated-ml#automatic-preprocessing-standard)



# 1. AutoML 개요



### 1. auto ML 

|      | 기술                                                         | 예                                                           |
| :--: | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 분류 | 데이터 세트에서 특정 행의 범주를 예측하는 작업입니다.        | 신용 카드 사기 탐지. 대상 열은 *True* 또는 *False* 범주의 **사기 탐지** 입니다 . 이 경우 데이터의 각 행을 true 또는 false로 분류합니다. |
| 회귀 | 연속 수량 출력 예측 작업.                                    | 특징에 따라 자동차 비용, 목표 열은 **가격** 이 될 것 입니다. |
| 예측 | 미래 트렌드의 방향을 결정할 때 정보에 입각 한 추정을하는 작업. | 다음 48 시간 동안 에너지 수요 예측 목표 컬럼이 될 **수요** 예측 된 값은 에너지 수요의 패턴을 표시하는데 사용된다. |

수행 순서 

1. **해결** 해야 할 **ML 문제 식별** : 분류, 예측 또는 회귀
2. **레이블이 지정된 학습 데이터의 소스 및 형식을 지정하십시오** . Numpy arrays 또는 Pandas dataframe
3. [로컬 컴퓨터, Azure Machine Learning Computes, 원격 VM 또는 Azure Databricks](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-set-up-training-targets) 와 같은 **모델 교육을위한 계산 대상을 구성합니다** . [원격 리소스에](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-remote) 대한 자동 교육 [에](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-auto-train-remote) 대해 알아보십시오 .
4. 다른 모델에 대한 반복 횟수, 하이퍼 파라미터 설정, 고급 전처리 / 기능화 및 최상의 모델을 결정할 때 살펴볼 메트릭을 결정하는 **자동화 된 기계 학습 매개 변수** 를 **구성하십시오** .
5. 실험 제출 및 결과



### 2. 적용 알고리즘

| Classification                                               | Regression                                                   | Time Series Forecasting                                      |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)* | [Elastic Net](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net)* | [Elastic Net](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net) |
| [Light GBM](https://lightgbm.readthedocs.io/en/latest/index.html)* | [Light GBM](https://lightgbm.readthedocs.io/en/latest/index.html)* | [Light GBM](https://lightgbm.readthedocs.io/en/latest/index.html) |
| [Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#classification)* | [Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#regression)* | [Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#regression) |
| [Decision Tree](https://scikit-learn.org/stable/modules/tree.html#decision-trees)* | [Decision Tree](https://scikit-learn.org/stable/modules/tree.html#regression)* | [Decision Tree](https://scikit-learn.org/stable/modules/tree.html#regression) |
| [K Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-regression)* | [K Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-regression)* | [K Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-regression) |
| [Linear SVC](https://scikit-learn.org/stable/modules/svm.html#classification)* | [LARS Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lars-lasso)* | [LARS Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lars-lasso) |
| [Support Vector Classification (SVC)](https://scikit-learn.org/stable/modules/svm.html#classification)* | [Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/sgd.html#regression)* | [Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/sgd.html#regression) |
| [Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)* | [Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)* | [Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests) |
| [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees) |
| [Xgboost](https://xgboost.readthedocs.io/en/latest/parameter.html)* | [Xgboost](https://xgboost.readthedocs.io/en/latest/parameter.html)* | [Xgboost](https://xgboost.readthedocs.io/en/latest/parameter.html) |
| [DNN Classifier](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNClassifier) | [DNN Regressor](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNRegressor) | [DNN Regressor](https://www.tensorflow.org/api_docs/python/tf/estimator/DNNRegressor) |
| [DNN Linear Classifier](https://www.tensorflow.org/api_docs/python/tf/estimator/LinearClassifier) | [Linear Regressor](https://www.tensorflow.org/api_docs/python/tf/estimator/LinearRegressor) | [Linear Regressor](https://www.tensorflow.org/api_docs/python/tf/estimator/LinearRegressor) |
| [Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html#bernoulli-naive-bayes)* | [Fast Linear Regressor](https://docs.microsoft.com/python/api/nimbusml/nimbusml.linear_model.fastlinearregressor?view=nimbusml-py-latest) | [Auto-ARIMA](https://www.alkaline-ml.com/pmdarima/modules/generated/pmdarima.arima.auto_arima.html#pmdarima.arima.auto_arima) |
| [Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/sgd.html#sgd)* | [Online Gradient Descent Regressor](https://docs.microsoft.com/python/api/nimbusml/nimbusml.linear_model.onlinegradientdescentregressor?view=nimbusml-py-latest) | [Prophet](https://facebook.github.io/prophet/docs/quick_start.html) |
| [Averaged Perceptron Classifier](https://docs.microsoft.com/python/api/nimbusml/nimbusml.linear_model.averagedperceptronbinaryclassifier?view=nimbusml-py-latest) |                                                              | ForecastTCN                                                  |
| [Linear SVM Classifier](https://docs.microsoft.com/python/api/nimbusml/nimbusml.linear_model.linearsvmbinaryclassifier?view=nimbusml-py-latest)* |                                                              |                                                              |



### 3. automl의 전처리

- 기본 (표준) 전처리

모든 자동 기계 학습 실험에서 알고리즘의 성능을 높이기 위해 데이터의 크기가 자동으로 조정되거나 정규화됩니다. 모델 교육 중에는 다음 스케일링 또는 정규화 기술 중 하나가 각 모델에 적용됩니다.

| 스케일링 및 정규화                                           | 기술                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| [StandardScaleWrapper](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) | 평균을 제거하고 단위 분산으로 스케일링하여 기능 표준화       |
| [MinMaxScalar](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html) | 각 열을 해당 열의 최소값 및 최대 값으로 스케일링하여 기능을 변환합니다. |
| [MaxAbsScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MaxAbsScaler.html#sklearn.preprocessing.MaxAbsScaler) | 각 기능의 최대 절대 값을 조정                                |
| [RobustScalar](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html) | 이 스케일러는 Quantile 범위에 따라 제공됩니다.               |
| [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) | 더 작은 차원 공간으로 데이터를 투사하기 위해 데이터의 특이 값 분해를 사용한 선형 차원 축소 |
| [TruncatedSVDWrapper](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) | 이 변압기는 잘린 단일 값 분해 (SVD)를 통해 선형 차원 축소를 수행합니다. PCA와 달리이 추정기는 특이 값 분해를 계산하기 전에 데이터를 중앙 집중화하지 않으므로 scipy.sparse 행렬을 효율적으로 사용할 수 있습니다. |
| [SparseNormalizer](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html) | 0이 아닌 성분이 하나 이상인 각 샘플 (즉, 데이터 행렬의 각 행)은 다른 샘플과 독립적으로 크기가 조정되어 표준 (l1 또는 l2)이 1이됩니다. |



- 고급 전처리 및 기능화

데이터 가드 레일, 인코딩 및 변환과 같은 추가 고급 전처리 및 기능도 사용할 수 있습니다. [포함 된 기능에 대해 자세히 알아보십시오](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-automated-ml-for-ml-models#featurization) . 다음을 사용하여이 설정을 활성화하십시오.





### 3. 요구 사항

교육 데이터 요구 사항 :

- 데이터는 테이블 형식이어야합니다.
- 예측하려는 값 (대상 열)이 데이터에 있어야합니다.



# 2. 사전 설치 사항



```bash
pip install azureml-sdk[automl]

pip install azureml-explain-model

pip install Azureml-train-automl-runtime
```

**사전 설치 오류 발생 ** automl은 별도의 환경으로 구성



- 자주 사용하는 패키지 

```python

from azureml.train.automl import AutoMLConfig
from azureml.core.dataset import Dataset

```





# 3. Dataset 설정



```python
from azureml.core.dataset import Dataset

ds = ws.get_default_datastore()

```





# 3. automated ML 설정 구성



- 실험 타임 아웃 시간을 30 분으로 설정하고 교차 검증 배를 2 회 설정 한 AUC 가중치를 1 차 메트릭으로 사용한 분류 실험

```python
    automl_classifier=AutoMLConfig(
            task='classification',
            primary_metric='AUC_weighted',
            experiment_timeout_minutes=30,
            blacklist_models=['XGBoostClassifier'],
            training_data=train_data,
            label_column_name=label,
            n_cross_validations=2)
```

- 5 개의 검증 교차로 60 분 후에 종료되도록 설정된 회귀 실험의 예입니다.

```python
automl_regressor = AutoMLConfig(
       task='regression',
       experiment_timeout_minutes=60,
       whitelist_models=['KNN'],
       primary_metric='r2_score',
       training_data=train_data,
       label_column_name=label,
       n_cross_validations=5)
```





```python
from azureml.train.automl import AutoMLConfig

automl_settings = {
    "experiment_timeout_minutes": 20,
    "primary_metric": 'accuracy',
    "max_concurrent_iterations": 4, 
    "max_cores_per_iteration": -1,
    "enable_dnn": True,
    "enable_early_stopping": True,
    "validation_size": 0.3,
    "verbosity": logging.INFO,
    "enable_voting_ensemble": False,
    "enable_stack_ensemble": False,
}

automl_config = AutoMLConfig(task = 'classification',
                             debug_log = 'automl_errors.log',
                             compute_target=compute_target,
                             training_data=train_dataset,
                             label_column_name=target_column_name,
                             **automl_settings
                            )
```



- AutoMLConfig 은 실험 제출시 포함

```pytho
automl_run = experiment.submit(automl_config, show_output=True)
```





| Property                      | Description                                                  |
| ----------------------------- | ------------------------------------------------------------ |
| **task**                      | classification or regression or forecasting                  |
| **primary_metric**            | This is the metric that you want to optimize. Classification supports the following primary metrics:  *accuracy* *AUC_weighted* *average_precision_score_weighted* *norm_macro_recall* *precision_score_weighted* |
| **iteration_timeout_minutes** | Time limit in minutes for each iteration.                    |
| **blacklist_models**          | *List* of *strings* indicating machine learning algorithms for AutoML to avoid in this run.   Allowed values for **Classification** *LogisticRegression* *SGD* *MultinomialNaiveBayes* *BernoulliNaiveBayes* *SVM* *LinearSVM* *KNN* *DecisionTree* *RandomForest* *ExtremeRandomTrees* *LightGBM* *GradientBoosting* *TensorFlowDNN* *TensorFlowLinearClassifier*  Allowed values for **Regression** *ElasticNet* *GradientBoosting* *DecisionTree* *KNN* *LassoLars* *SGD* *RandomForest* *ExtremeRandomTrees* *LightGBM* *TensorFlowLinearRegressor* *TensorFlowDNN*  Allowed values for **Forecasting** *ElasticNet* *GradientBoosting* *DecisionTree* *KNN* *LassoLars* *SGD* *RandomForest* *ExtremeRandomTrees* *LightGBM* *TensorFlowLinearRegressor* *TensorFlowDNN* *Arima* *Prophet* |
| **whitelist_models**          | *List* of *strings* indicating machine learning algorithms for AutoML to use in this run. Same values listed above for **blacklist_models** allowed for **whitelist_models**. |
| **experiment_exit_score**     | Value indicating the target for *primary_metric*.  Once the target is surpassed the run terminates. |
| **experiment_timeout_hours**  | Maximum amount of time in hours that all iterations combined can take before the experiment terminates. |
| **enable_early_stopping**     | Flag to enble early termination if the score is not improving in the short term. |
| **featurization**             | 'auto' / 'off' Indicator for whether featurization step should be done automatically or not. Note: If the input data is sparse, featurization cannot be turned on. |
| **n_cross_validations**       | Number of cross validation splits.                           |
| **training_data**             | Input dataset, containing both features and label column.    |
| **label_column_name**         | The name of the label column.                                |



# 4. primary metric



| Classification                   | Regression                         | Time Series Forecasting            |
| :------------------------------- | :--------------------------------- | :--------------------------------- |
| accuracy                         | spearman_correlation               | spearman_correlation               |
| AUC_weighted                     | normalized_root_mean_squared_error | normalized_root_mean_squared_error |
| average_precision_score_weighted | r2_score                           | r2_score                           |
| norm_macro_recall                | normalized_mean_absolute_error     | normalized_mean_absolute_error     |
| precision_score_weighted         |                                    |                                    |







# 5. widgets



```python
from azureml.widgets import RunDetails
from azureml.core.run import Run

ws = Workspace.from_config(path="../tooneaml_config.json")

experiment = Experiment (ws, 'automl-classification-text-dnn')
run_id = 'AutoML_a164aada-6b42-4095-ab67-2a1336486283' #replace with run_ID
run = Run(experiment, run_id)
RunDetails(run).show()
```





```python
from azureml.widgets import RunDetails

RunDetails(remote_run).show()
```

