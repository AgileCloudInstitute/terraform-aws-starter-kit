## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import sys  	
from pathlib import Path	
import deploymentFunctions as depfunc  

print("Hello from inside createVMFromPipeline.py ")  	

###############################################################################
### Print vars to validate that they are imported and also obscured
###############################################################################
#$(-aws-public-access-key)  
#$(-aws-secret-access-key)  
#$(storageAccountNameTerraformBackend)  
#$(terra-backend-key)  
#$(aws-region)  
#$(System.DefaultWorkingDirectory)   
#$(demoStorageKey)  
#$(foundationKeyFileTF)  
#$(vmKeyFileTF)

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
storageContainerName="terraform-backend-aws-starter-kit"
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

##########################################################################################
### Initialize terraform and remote backend from inside the network foundation directory
##########################################################################################
resourceGroupNameLine="    resource_group_name  = \""+resourceGroupName+"\"\n"	
storageAccountNameTerraformBackendLine="    storage_account_name = \""+storageAccountNameTerraformBackend+"\"\n"	
storageContainerNameLine="    container_name       = \""+storageContainerName+"\"\n"	
terraBackendKeyLine="    key                  = \""+foundationKeyFileTF+"\"\n"

# tfFileNameAndPath=dirToUseNet+"/terraform.tf"	
# print("tfFileNameAndPath is: ", tfFileNameAndPath)	
# print("About to write 8 lines to a file.")	
# f = open(tfFileNameAndPath, "w")	
# f.write("terraform {\n")	
# f.write("  backend \"azurerm\" {\n")	
# f.write(resourceGroupNameLine)	
# f.write(storageAccountNameTerraformBackendLine)	
# f.write(storageContainerNameLine)	
# f.write(terraBackendKeyLine)	
# f.write("  }\n")	
# f.write("}\n")	
# f.close()	

# print("About to read the file we just wrote.")	
# #open and read the file after the appending:	
# f = open(tfFileNameAndPath, "r")	
# print(f.read()) 	

print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(pathToFoundationCalls).iterdir(), sep="\n")	

print("About to call terraform output:  ")	
outputCommand="terraform output" 
depfunc.runTerraformCommand(outputCommand, pathToFoundationCalls )	
  
# #############################################################################
# ### Create the virtual machine
# #############################################################################
# #Get Vars to pass into terraform commands:
varsFragmentVM = ""
varsFragmentVM = varsFragmentVM + " -var=\"aws_region=" + awsRegion +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"_public_access_key=" + awsPublicAccessKey +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"_secret_access_key=" + awsSecretAccessKey +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"vpcId=" + depfunc.vpc_id +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"systemName=" + system_name +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"environmentName=" + environment_name +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"ownerName=" + owner_name +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"vmName=" + vm_name +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"amiId=" + ami_id +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"subnetId=" + depfunc.subnet_id +"\""  
varsFragmentVM = varsFragmentVM + " -var=\"sgId=" + depfunc.sg_id +"\""  

print("varsFragmentVM is: ", varsFragmentVM)  
applyCommandVM = "terraform apply -auto-approve" + varsFragmentVM
print("applyCommandVM is: ", applyCommandVM)
# #runTerraformCommand(applyCommandNet, dirToUseNet)  

#DELETE BY UNCOMMENTING THE FOLLOWING DURING DEVELOPMENT, THEN MAKE SEPARATE FILE FOR RELEASE:  
# print("About to call terraform destroy.  ")    
# destroyCommand="terraform destroy -auto-approve" + varsFoundation
# runTerraformCommand(destroyCommand, subDir4 )  

