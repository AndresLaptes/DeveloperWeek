# This file is used to configure the MongoDB Atlas provider
terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.10.0"
    }
  }

  required_version = ">= 1.3.0"
}

provider "mongodbatlas" {
  public_key  = var.mongodb_public_key
  private_key = var.mongodb_private_key
}

resource "mongodbatlas_project_ip_access_list" "omar" {
  project_id = var.mongodb_project_id
  ip_address = "89.129.149.205" 
  comment    = "Omar's IP address"
}

resource "mongodbatlas_project_ip_access_list" "Rubén" {
  project_id = var.mongodb_project_id
  ip_address = "83.50.134.98" 
  comment    = "Rubén's IP address"
}


resource "mongodbatlas_project_ip_access_list" "Andres" {
  project_id = var.mongodb_project_id
  ip_address = "79.116.132.232"
  comment    = "Andres's IP address"
}

resource "mongodbatlas_database_user" "omar_user" {
  project_id          = var.mongodb_project_id
  username            = "omar_user"
  password            = "123"
  auth_database_name  = "admin"
  roles {
    role_name         = "readWrite"
    database_name     = "example_db"
  }
}

resource "mongodbatlas_database_user" "ruben_user" {
  project_id          = var.mongodb_project_id
  username            = "ruben_user"
  password            = "123"
  auth_database_name  = "admin"
  roles {
    role_name         = "readWrite"
    database_name     = "example_db"
  }
}

resource "mongodbatlas_database_user" "andres_user" {
  project_id          = var.mongodb_project_id
  username            = "andres_user"
  password            = "123"
  auth_database_name  = "admin"
  roles {
    role_name         = "readWrite"
    database_name     = "example_db"
  }
}

