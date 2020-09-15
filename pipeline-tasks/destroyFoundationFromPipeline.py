## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import sys  	
import re	
import os	
import subprocess  	
from pathlib import Path	
import pip  
import deploymentFunctions as depfunc  

print("Hello from inside createStarterFromPipeline.py ")  	

###############################################################################
### Print vars to validate that they are imported and also obscured
###############################################################################
awsPublicAccessKey=sys.argv[1] 	
awsSecretAccessKey=sys.argv[2] 	
storageAccountNameTerraformBackend=sys.argv[3] 	
terraBackendKey=sys.argv[4] 	
awsRegion=sys.argv[5] 	
DefaultWorkingDirectory=sys.argv[6] 	
demoStorageKey=sys.argv[7]
#The following 7 need to be made into input variables	
resourceGroupName="pipeline-resources"	
storageAccountNameTerraformBackend='tfbkendabc123x'
storageContainerName="tfcontainer"
terraKeyFileName = "aws-simple-network-foundation-state.tf"
vpc_name="thisVPC"
system_name="thisSystem"
environment_name="thisEnvironment"
owner_name="thisOwner"
vm_name="thisVM"  

print("Python version is: ", sys.version_info[0])  	
print("awsPublicAccessKey is: ", awsPublicAccessKey)	
print("awsSecretAccessKey is: ", awsSecretAccessKey)	
print("storageAccountNameTerraformBackend is: ", storageAccountNameTerraformBackend)	
print("terraBackendKey is: ", terraBackendKey)	
print("awsRegion is: ", awsRegion)	
print("DefaultWorkingDirectory is: ", DefaultWorkingDirectory)	
print("demoStorageKey is: ", demoStorageKey)
foundationSecretsFile = '/home/azureuser/' + 'foundationSecrets.tfvars'

####################################################################################
### Set values for pathToApplicationRoot and dirToUseNet  
### while also listing contents of each directory  
####################################################################################
print("About to list contents of DefaultWorkingDirectory")	
print(*Path(DefaultWorkingDirectory).iterdir(), sep="\n")	

subDir2=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop")	
print(*Path(subDir2).iterdir(), sep="\n")	

pathToApplicationRoot = subDir2  

subDir3=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules")	
print(*Path(subDir3).iterdir(), sep="\n")	

subDir4=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(subDir4).iterdir(), sep="\n")	
  
dirToUseNet = subDir4   
print("dirToUseNet is: ", dirToUseNet)  

subDir5=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-s3-backend-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-s3-backend-call-to-module/")	
print(*Path(subDir5).iterdir(), sep="\n")	

subDir6=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/")	
print(*Path(subDir6).iterdir(), sep="\n")	

subDir7=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/")	
print(*Path(subDir7).iterdir(), sep="\n")	

##########################################################################################
### Initialize terraform and remote backend from inside the network foundation directory
##########################################################################################
depfunc.createBackendConfigFileTerraform(resourceGroupName, storageAccountNameTerraformBackend, storageContainerName, terraKeyFileName, dirToUseNet ) 
print("About to read the file we just wrote.") 
tfFileNameAndPath=dirToUseNet+"/terraform.tf" 
f = open(tfFileNameAndPath, "r") 
print(f.read())  
print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(dirToUseNet).iterdir(), sep="\n")	
print("About to call terraform init:  ")	
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
depfunc.runTerraformCommand(initCommand, dirToUseNet )	
  
#############################################################################
### Destroy the network foundation
#############################################################################
varsFoundation = depfunc.getInputVarsFoundationFromPipeline(awsRegion, vpc_name, system_name, environment_name, owner_name, awsPublicAccessKey, awsSecretAccessKey, foundationSecretsFile)  
print("varsFoundation is: ", varsFoundation)  
#applyCommandNet = "terraform apply -auto-approve" + varsFoundation
#print("applyCommandNet is: ", applyCommandNet)
print("dirToUseNet is: ", dirToUseNet)
#depfunc.runTerraformCommand(applyCommandNet, dirToUseNet)  
#print("Finished running apply command. ")

#THE FOLLOWING ARE FOR OTHER MODULES:  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"vmName=" + vm_name +"\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"amiId=ami-id-goesw-here\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"s3BucketNameTF=bucket-name-goes-here\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"dynamoDbTableNameTF=table-name-goes-here\""  

#DELETE BY UNCOMMENTING THE FOLLOWING DURING DEVELOPMENT, THEN MAKE SEPARATE FILE FOR RELEASE:  
print("About to call terraform destroy.  ")    
destroyCommand="terraform destroy -auto-approve" + varsFoundation
depfunc.runTerraformCommand(destroyCommand, subDir4 )  

#Finally delete the secrets file fo that the secrets must be retrieved from the key vault every time
print("About to remove the secrets file. ")
os.remove(foundationSecretsFile)
