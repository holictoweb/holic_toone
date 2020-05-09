 # ML
# 1. workspace
az ml workspace create -w toonews -g HW_aischool

# create compute
az ml computetarget create amlcompute -n holic-amlcompute-01 --min-nodes 1 --max-nodes 1 -s STANDARD_D3_V2

# 기존 서비스에 연결
## storage account 
az storage account show --name <storage-account-name> --query "id"
## application insight
az monitor app-insights component show --app <application-insight-name> -g <resource-group-name> --query "id"
## key vault
az keyvault show --name <key-vault-name> --query "ID"
## container registry
az acr show --name <acr-name> -g <resource-group-name> --query "id"
 
