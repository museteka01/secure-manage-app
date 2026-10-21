# Terraform

Creates a private, versioned, encrypted S3 bucket for the app.

    cp terraform.tfvars.example terraform.tfvars   # then edit the bucket name
    terraform init
    terraform plan
    terraform apply

`terraform.tfvars` and all `*.tfstate` files are git-ignored - never commit them.
