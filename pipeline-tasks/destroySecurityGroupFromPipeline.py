## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import sys
from pathlib import Path
import deploymentFunctions as depfunc

print("Hello from inside destroySecurityGroupRuleFromPipeline.py ")  	

###############################################################################
### Print vars to validate that they are imported and also obscured
###############################################################################
awsPublicAccessKey=sys.argv[1]
awsSecretAccessKey=sys.argv[2]
storageAccountName=sys.argv[3]
terraBackendKey=sys.argv[4]
awsRegion=sys.argv[5]
defaultWorkingDirectory=sys.argv[6]
demoStorageKey=sys.argv[7]
foundationKeyFileTF=sys.argv[8]
sgKeyFileTF=sys.argv[9]

print("awsPublicAccessKey is: ", awsPublicAccessKey)
print("awsSecretAccessKey is: ", awsSecretAccessKey)
print("storageAccountName is: ", storageAccountName)
print("terraBackendKey is: ", terraBackendKey)
print("awsRegion is: ", awsRegion)
print("defaultWorkingDirectory is: ", defaultWorkingDirectory)
print("demoStorageKey is: ", demoStorageKey)
print("foundationKeyFileTF is: ", foundationKeyFileTF)
print("sgKeyFileTF is: ", sgKeyFileTF)
print("Python version is: ", sys.version_info[0])  	

#The following 3 need to be made into input variables	
resourceGroupName="pipeline-resources"	
storageContainerName="tfcontainer"
vpc_name="thisVPC"

####################################################################################
### Set values for pathToFoundationCalls and pathToSecurityGroupRulesCalls 
### while also listing contents of each directory  
####################################################################################
print("About to list contents of defaultWorkingDirectory")	
print(*Path(defaultWorkingDirectory).iterdir(), sep="\n")	

pathToCallsToModules=defaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules")	
print(*Path(pathToCallsToModules).iterdir(), sep="\n")	

pathToFoundationCalls=pathToCallsToModules+"aws-simple-network-foundation-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(pathToFoundationCalls).iterdir(), sep="\n")	
 
print("pathToFoundationCalls is: ", pathToFoundationCalls) 

pathToSecurityGroupRulesCalls=defaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/")	
print(*Path(pathToSecurityGroupRulesCalls).iterdir(), sep="\n")	

##########################################################################################
### Get Output variables from foundation  
##########################################################################################
print("About to configure the remote backend of the foundation module so that it can be initialized and so that its outputs can be retrieved. ")
depfunc.createBackendConfigFileTerraform(resourceGroupName, storageAccountName, storageContainerName, foundationKeyFileTF, pathToFoundationCalls ) 
print("About to initialize the foundation backend so that we can get its output variables after. ")
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\"" 
depfunc.runTerraformCommand(initCommand, pathToFoundationCalls )	
print("About to call terraform output:  ")	
outputCommand="terraform output" 
depfunc.runTerraformCommand(outputCommand, pathToFoundationCalls )	

##########################################################################################
### Initialize terraform and remote backend from inside the security group rules directory
##########################################################################################
depfunc.createBackendConfigFileTerraform(resourceGroupName, storageAccountName, storageContainerName, sgKeyFileTF, pathToSecurityGroupRulesCalls )
tfFileNameAndPath=pathToSecurityGroupRulesCalls+"/terraform.tf"	
print("About to read the file we just wrote.")	
#open and read the file after the appending:	
f = open(tfFileNameAndPath, "r")	
print(f.read()) 	

print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(pathToSecurityGroupRulesCalls).iterdir(), sep="\n")	
print("About to call terraform init:  ")	
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
depfunc.runTerraformCommand(initCommand, pathToSecurityGroupRulesCalls )	

#############################################################################
### Create the security group rule(s)
#############################################################################
#Get Vars to pass into terraform commands:
varsSGR=depfunc.getVarsSGRFromPipeline(awsRegion, awsPublicAccessKey, awsSecretAccessKey, vpc_name, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name )
print("varsSGR is: ", varsSGR)
print("About to call terraform destroy.  ")    
destroyCommand="terraform destroy -auto-approve" + varsSGR
depfunc.runTerraformCommand(destroyCommand, pathToSecurityGroupRulesCalls )  
