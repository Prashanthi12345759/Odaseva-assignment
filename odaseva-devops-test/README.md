# Odaseva DevOps Test

This repository contains the solution for the Odaseva DevOps test.

## Prerequisites

- Azure CLI
- Terraform
- Node.js

## Deployment

1. Clone the repository.
2. Navigate to the `terraform` directory and run `terraform init` and `terraform apply`.
3. Deploy the Azure Functions using the Azure CLI or Azure Portal.
CreateCandidate:
func azure functionapp publish odaseva-function-app --python
GetCandidate:
func azure functionapp publish odaseva-function-app --python
GetCandidatesBySpecialty:
func azure functionapp publish odaseva-function-app --python

## Testing

Use the `test-api.sh` script to test the API endpoints.

## Folder Structure

- `terraform/`: Contains Terraform configuration files.
- `azure-functions/`: Contains Azure Functions code.
- `scripts/`: Contains deployment and testing scripts.