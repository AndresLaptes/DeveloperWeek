#!/bin/sh
terraform init
terraform plan
terraform apply -auto-approve

# Keep the container running
tail -f /dev/null