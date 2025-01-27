# Use the official HashiCorp Terraform image from Docker Hub
FROM hashicorp/terraform:1.5.5

# Install MongoDB Shell (mongosh)
RUN apk add --no-cache mongodb-tools

# Set the working directory inside the container
WORKDIR /app

# Copy the Terraform configuration files and the shell script into the container
COPY . /app
COPY entrypoint.sh /entrypoint.sh

# Set entrypoint to the shell script
ENTRYPOINT ["/entrypoint.sh"]
