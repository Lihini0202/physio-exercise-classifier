terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# 1. A NEW Resource Group for the Physio App
resource "azurerm_resource_group" "physio_rg" {
  name     = "physio-predictor-rg" # New, unique name!
  location = var.region
}

# 2. A NEW Container Registry for the Physio App
resource "azurerm_container_registry" "physio_acr" {
  name                = "physioacr${random_id.acr_suffix.hex}" # New name!
  resource_group_name = azurerm_resource_group.physio_rg.name
  location            = azurerm_resource_group.physio_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "random_id" "acr_suffix" {
  byte_length = 4
}

# 3. The Physio App Itself
resource "azurerm_container_group" "physio_app" {
  name                = "physio-app-instance"
  location            = azurerm_resource_group.physio_rg.location
  resource_group_name = azurerm_resource_group.physio_rg.name
  os_type             = "Linux"
  ip_address_type     = "Public"

  image_registry_credential {
    server   = azurerm_container_registry.physio_acr.login_server
    username = azurerm_container_registry.physio_acr.admin_username
    password = azurerm_container_registry.physio_acr.admin_password
  }

  container {
    name   = "physio-predictor-container"
    image  = "${azurerm_container_registry.physio_acr.login_server}/physio-predictor:latest"
    cpu    = 1
    memory = 2 # This is a bigger model, use 2GB
    ports {
      port     = 8501
      protocol = "TCP"
    }
  }
}

# 4. Outputs
output "physio_acr_name" {
  value = azurerm_container_registry.physio_acr.name
}

output "physio_app_url" {
  value = "http://${azurerm_container_group.physio_app.ip_address}:8501"
}
