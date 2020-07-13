#!/bin/bash

echo 'About to demonstrate that keys remain encrypted but are also imported: '  
echo "AWS private key is: $(-aws-public-access-key)"  
echo "AWS secret key: $(-aws-secret-access-key)"  
echo "storageAccountNameTerraformBackend is: $(storageAccountNameTerraformBackend)"  
echo "Storage account terra-backend-key key is: $(terra-backend-key)"
echo "About to set environment variables for public key and secret key.  "
export 'AWS_PUB=$(-aws-public-access-key)' >> $HOME/.bashrc
export 'AWS_SECRET=$(-aws-secret-access-key)' >> $HOME/.bashrc
export 'STOR_SECRET=$(terra-backend-key)' >> $HOME/.bashrc
echo public environment var is: 
echo "$AWS_PUB" 
echo secret environment var is: 
echo "$AWS_SECRET" 
echo storage key environment var is:  
echo "$STOR_SECRET"
  
echo "About to demonstrate the pipeline variables have been imported as clear-text: "  
echo "AWS region is: $(aws-region)"  

#echo "Now the imported x509 cert is: $(imported-for-aws-demo) "
  
echo "The location of Python is: "  
which python  
echo "The version of Python running is: "  
python --version  
echo "The version of Python 3.7 running is: "
python3.7 -V
echo "The version of terraform running is: "  
terraform -version  
echo "About to list contents of current directory: "  
ls -al  
echo "About to list contents of working subdirectory $(System.DefaultWorkingDirectory)/_terraform-aws-simple-example"
cd $(System.DefaultWorkingDirectory)/_terraform-aws-simple-example
ls -al
echo "About to list contents of working subdirectory $(System.DefaultWorkingDirectory)/_terraform-aws-simple-example/drop "
cd drop
ls -al 
echo "About to list contents of working subdirectory $(System.DefaultWorkingDirectory)/_terraform-aws-simple-example/drop/calls-to-modules "  
cd calls-to-modules
ls -al  
echo "About to list contents of working subdirectory $(System.DefaultWorkingDirectory)/_terraform-aws-simple-example/drop/calls-to-modules/terraform-aws-simple-example-call-to-module "  
cd terraform-aws-simple-example-call-to-module
ls -al  
echo "About to create terraform tf file to refer to backend: "

cat << 'EOF' > terraform.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "pipeline-resources"
    storage_account_name = "storage-account-name"
    container_name       = "terraform-backend"
    key                  = "aws.terraform.tfstate"
  }
}
EOF
  
echo about to list all of ..
ls -al ..
echo "about to list all of .. / .. "
ls -al ../..
echo "about to list all of .. / .. / modules "
ls -al ../../modules

echo "About to call terraform init:  "
#terraform init -backend=true -backend-config="access_key=$(terra-backend-key)"  

#path_to_ssh_keys=/home/azureuser/keys/
#name_of_ssh_key=aws-demo-key
  
echo "About to call the python script with a variable passed in: "
#python3.7 pipeline-network-apply.py $(aws-region) "/home/azureuser/keys/" "aws-demo-key"
