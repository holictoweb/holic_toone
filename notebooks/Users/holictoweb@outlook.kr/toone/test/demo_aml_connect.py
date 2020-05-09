# Databricks notebook source
from azureml.core import Workspace

subscription_id = 'e478b470-4e14-4384-bc05-0e03fe0c2d9e'
resource_group  = 'HO_analytics'
workspace_name  = 'tooneml'

try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    ws.write_config()
    print('Library configuration succeeded')
except:
    print('Workspace not found')

# COMMAND ----------

# MAGIC %md
# MAGIC - 환경 구축
# MAGIC - 기존에 구성된 환경이나 직접 설정한 환경을 구성하면 해당 환경을 재사용 가능 하며 재사용시 ARC에 있는 이미지도 재 사용이 가능함. 

# COMMAND ----------

from azureml.core import Workspace, Environment

ws = Workspace.from_config()
#env = Environment.get(workspace=ws, name="toone_env_databricks")


envs = Environment.list(workspace=ws)

for env in envs:
    if env.startswith("AzureML"):
        print("Name",env)
        print("packages", envs[env].python.conda_dependencies.serialize_to_string())


        

# COMMAND ----------

# MAGIC %md 
# MAGIC - 수동으로 환경 생성 

# COMMAND ----------

from azureml.core.environment import Environment
Environment(name="toone_env_databricks")
# 수동으로 환경 셋팅을 위한 추가 코드 필요 