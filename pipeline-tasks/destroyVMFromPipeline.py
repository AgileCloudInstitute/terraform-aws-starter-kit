## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import sys  	
from pathlib import Path	
import deploymentFunctions as depfunc  

print("Hello from inside destroyVMFromPipeline.py ")  	

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
foundationKeyFileTF=sys.argv[8]
vmKeyFileTF=sys.argv[9]

#The following 7 need to be made into input variables	
resourceGroupName="pipeline-resources"	
storageContainerName="tfcontainer"
vpc_name="thisVPC"
system_name="thisSystem"
environment_name="thisEnvironment"
owner_name="thisOwner"
vm_name="thisVM"
ami_id="placerholder for later when packer is used"

print("Python version is: ", sys.version_info[0]) 
print("awsPublicAccessKey is: ", awsPublicAccessKey) 
print("awsSecretAccessKey is: ", awsSecretAccessKey) 
print("storageAccountNameTerraformBackend is: ", storageAccountNameTerraformBackend) 
print("terraBackendKey is: ", terraBackendKey) 
print("awsRegion is: ", awsRegion) 
print("DefaultWorkingDirectory is: ", DefaultWorkingDirectory) 
print("demoStorageKey is: ", demoStorageKey) 
print("foundationKeyFileTF is: ", foundationKeyFileTF) 
print("vmKeyFileTF is: ", vmKeyFileTF) 

####################################################################################
### Set values for pathToFoundationCalls and pathToVirtualMachineCalls 
### while also listing contents of each directory  
####################################################################################
print("About to list contents of DefaultWorkingDirectory")	
print(*Path(DefaultWorkingDirectory).iterdir(), sep="\n")	

pathToCallsToModules=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules")	
print(*Path(pathToCallsToModules).iterdir(), sep="\n")	

pathToFoundationCalls=pathToCallsToModules+"aws-simple-network-foundation-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(pathToFoundationCalls).iterdir(), sep="\n")	
 
print("pathToFoundationCalls is: ", pathToFoundationCalls) 
  
pathToVirtualMachineCalls=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/")	
print(*Path(pathToVirtualMachineCalls).iterdir(), sep="\n")	

#########################################################################################
### Get output variables from foundation
#########################################################################################
print("About to configure the remote backend of the foundation module so that it can be initialized and so that its outputs can be retrieved. ")
depfunc.createBackendConfigFileTerraform(resourceGroupName, storageAccountNameTerraformBackend, storageContainerName, foundationKeyFileTF, pathToFoundationCalls ) 
print("About to initialize the foundation backend so that we can get its output variables after. ")
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\"" 
depfunc.runTerraformCommand(initCommand, pathToFoundationCalls )	
print("About to call terraform output:  ")	
outputCommand="terraform output" 
depfunc.runTerraformCommand(outputCommand, pathToFoundationCalls )	
  
##########################################################################################
### Initialize terraform and remote backend from inside the virtual machine directory
##########################################################################################
#Create the config file for the terraform backend
depfunc.createBackendConfigFileTerraform(resourceGroupName, storageAccountNameTerraformBackend, storageContainerName, vmKeyFileTF, pathToVirtualMachineCalls )
tfFileNameAndPath=pathToVirtualMachineCalls+"terraform.tf"
print("About to read the file we just wrote.")	
#open and read the file after the appending:	
f = open(tfFileNameAndPath, "r")	
print(f.read()) 	

print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/")	
print(*Path(pathToVirtualMachineCalls).iterdir(), sep="\n")	
print("About to call terraform init:  ")	
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
depfunc.runTerraformCommand(initCommand, pathToVirtualMachineCalls )	

#############################################################################
### Destroy the virtual machine
#############################################################################
#Get Vars to pass into terraform commands:
varsVM=depfunc.getVarsVMFromPipeline( awsRegion, awsPublicAccessKey, awsSecretAccessKey, depfunc.vpc_id, system_name, environment_name, owner_name, vm_name, ami_id, depfunc.subnet_id, depfunc.sg_id )
print("varsVM is: ", varsVM)  
print("About to call terraform destroy.  ")    
destroyCommand="terraform destroy -auto-approve" + varsVM
depfunc.runTerraformCommand(destroyCommand, pathToVirtualMachineCalls )  
