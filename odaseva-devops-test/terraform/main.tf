provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "odaseva-devops-rg"
  location = "East US"
}

resource "azurerm_cosmosdb_account" "cosmosdb" {
  name                = "odaseva-cosmosdb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}

resource "azurerm_storage_account" "storage" {
  name                     = "odasevastorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_function_app" "function_app" {
  name                       = "odaseva-function-app"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  app_settings = {
    "COSMOSDB_ENDPOINT" = azurerm_cosmosdb_account.cosmosdb.endpoint
    "COSMOSDB_KEY"      = azurerm_cosmosdb_account.cosmosdb.primary_master_key
  }
}

resource "azurerm_api_management" "apim" {
  name                = "odaseva-apim"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  publisher_name      = "Odaseva"
  publisher_email     = "admin@odaseva.com"

  sku {
    name     = "Developer"
    capacity = 1
  }
}