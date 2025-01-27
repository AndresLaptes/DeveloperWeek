# MongoDB Atlas Configuration with Terraform

This project configures resources in MongoDB Atlas using Terraform and Docker. It provides the infrastructure to manage database access and automatically configure users, especially in development environments. The configured resources include IP access lists and database users.
Project Files
## 1. main.tf

This file contains the main Terraform configuration to interact with MongoDB Atlas. It defines the following resources:

* MongoDB Atlas Provider: Sets the required keys to access MongoDB Atlas.
* IP Access Lists: Adds specific IP addresses with temporary access permissions to MongoDB Atlas databases.
* Database Users: Creates users with read and write permissions on specific databases within the MongoDB Atlas project.

## 2. variables.tf

This file defines the variables used in the Terraform configuration. Variables are necessary to provide flexible values, such as the public and private keys for MongoDB and the MongoDB Atlas project ID.
## 3. terraform.tfvars

This file assigns actual values to the variables defined in variables.tf. You should ensure that the corresponding keys and the MongoDB Atlas project ID are properly configured.
## 4. Dockerfile

Defines the configuration for a Docker container that will include the necessary tools to run Terraform. In this case, it installs the necessary MongoDB tools and configures the container to automatically run Terraform commands when it starts.
## 5. entrypoint.sh

This script runs when the Docker container starts. It automates the process of initializing Terraform (terraform init), planning (terraform plan), and applying the infrastructure (terraform apply). After running the Terraform commands, it keeps the container running to check any changes or further processing.
* ### Instructions for Use

    #### Build the Docker Image:
        In the root directory of the project, build the Docker image 
        with the following command:
        
        sudo docker build -t terraform-mongo .

    #### Run the Container:

        Once the image is built, run the container to apply the     
        Terraform configuration:

        sudo docker run terraform-mongo

        This command will run the process inside the Docker container, 
        automatically applying the configurations to MongoDB Atlas.
    
    #### Destroy the Infrastructure:

        If you need to destroy the resources you created in MongoDB 
        Atlas using Terraform, follow these steps:

        First, list the running Docker containers with docker ps:

        docker ps

        Find the container ID of the running container and enter it using docker exec:

        docker exec -it <container_id> /bin/sh

        Inside the container, run the terraform destroy command to destroy the resources:

        terraform destroy -auto-approve

        This will remove the infrastructure and all related resources from MongoDB Atlas.