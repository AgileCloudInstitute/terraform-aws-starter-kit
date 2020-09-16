## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import sys  	
from pathlib import Path	
import deploymentFunctions as depfunc  

print("Hello from inside createSecurityGroupRuleFromPipeline.py ")  	

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
#$(sgKeyFileTF)

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

#The following 7 need to be made into input variables	
resourceGroupName="pipeline-resources"	
storageContainerName="terraform-backend-aws-starter-kit"
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
### Initialize terraform and remote backend from inside the network foundation directory
##########################################################################################
resourceGroupNameLine="    resource_group_name  = \""+resourceGroupName+"\"\n"	
storageAccountNameTerraformBackendLine="    storage_account_name = \""+storageAccountName+"\"\n"	
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

#############################################################################
### Create the security group rule(s)
#############################################################################
#Get Vars to pass into terraform commands:
varsFragmentSGR = ""
varsFragmentSGR = varsFragmentSGR +  " -var=\"aws_region=" + awsRegion +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"_public_access_key=" + awsPublicAccessKey +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"_secret_access_key=" + awsSecretAccessKey +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcName=" + vpc_name +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcId=" + depfunc.vpc_id +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcCidr=" + depfunc.vpc_cidr +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"sgId=" + depfunc.sg_id +"\""  
varsFragmentSGR = varsFragmentSGR +  " -var=\"sgName=" + depfunc.sg_name +"\""  
#aws_region  #_public_access_key  #_secret_access_key  #vpcName  #vpcId  #vpcCidr  #sgId  #sgName
print("varsFragmentSGR is: ", varsFragmentSGR)
applyCommandSGR = "terraform apply -auto-approve" + varsFragmentSGR
print("applyCommandSGR is: ", applyCommandSGR)
#runTerraformCommand(applyCommandSGR, pathToSecurityGroupRulesCalls)  


#DELETE BY UNCOMMENTING THE FOLLOWING DURING DEVELOPMENT, THEN MAKE SEPARATE FILE FOR RELEASE:  
# print("About to call terraform destroy.  ")    
# destroyCommand="terraform destroy -auto-approve" + varsFoundation
# runTerraformCommand(destroyCommand, subDir4 )  

