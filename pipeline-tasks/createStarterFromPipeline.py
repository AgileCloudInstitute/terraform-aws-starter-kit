import sys  	
import re	
import os	
import subprocess  	
from pathlib import Path	

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')	

print("Hello from inside createSimpleExample.py ")  	

awsPublicAccessKey=sys.argv[1] 	
awsSecretAccessKey=sys.argv[2] 	
storageAccountNameTerraformBackend=sys.argv[3] 	
terraBackendKey=sys.argv[4] 	
awsRegion=sys.argv[5] 	
DefaultWorkingDirectory=sys.argv[6] 	
#The following 7 need to be made into input variables	
resourceGroupName="pipeline-resources"	
storageContainerName="terraform-backend-aws-simple"	
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
  
#######################################################################################################  
#######################################################################################################  
###  Start Imported Stuff  
#######################################################################################################  
#######################################################################################################  
  
import pip  
failed = pip.main(["install", 'requests'])  
print("status of requests install: ", failed)  
failed = pip.main(["install", 'pyyaml'])  
print("status of pyyaml install: ", failed)  
  
import deploymentFunctions as depfunc  
import re  
  
pathToApplicationRoot = 'C:\\projects\\terraform\\sandbox\\terraform-aws-simple-example\\'  
dirOfYamlFile = "C:\\projects\\terraform\\tfvars\\terraform-aws-simple-example\\"
nameOfYamlFile = 'varsFromDevLaptop.yaml'
yamlFileAndPath = dirOfYamlFile + nameOfYamlFile
  
#######################################################################################################  
#######################################################################################################  
###  End Imported Stuff  
#######################################################################################################  
#######################################################################################################  
  

# #print(*Path("/home/username/www/").iterdir(), sep="\n")	

# def runTerraformCommand(commandToRun, workingDir ):	
#     print("Inside runTerraformCommand(..., ...) function. ")	
#     print("commandToRun is: " +commandToRun)	
#     print("workingDir is: " +workingDir)	

#     proc = subprocess.Popen( commandToRun,cwd=workingDir,stdout=subprocess.PIPE, shell=True)	
#     while True:	
#       line = proc.stdout.readline()	
#       if line:	
#         thetext=line.decode('utf-8').rstrip('\r|\n')	
#         decodedline=ansi_escape.sub('', thetext)	
#         print(decodedline)	
#       else:	
#         break	


print("About to list contents of DefaultWorkingDirectory")	
print(*Path(DefaultWorkingDirectory).iterdir(), sep="\n")	

subDir1=DefaultWorkingDirectory+"/_terraform-aws-starter-kit"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit")	
print(*Path(subDir1).iterdir(), sep="\n")	

subDir2=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop")	
print(*Path(subDir2).iterdir(), sep="\n")	

subDir3=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules")	
print(*Path(subDir3).iterdir(), sep="\n")	

subDir4=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(subDir4).iterdir(), sep="\n")	
  
subDir5=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-s3-backend-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-s3-backend-call-to-module/")	
print(*Path(subDir5).iterdir(), sep="\n")	

subDir6=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-security-group-rules-call-to-module/")	
print(*Path(subDir6).iterdir(), sep="\n")	

subDir7=DefaultWorkingDirectory+"/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/"	
print("About to list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-vm-call-to-module/")	
print(*Path(subDir7).iterdir(), sep="\n")	

# resourceGroupNameLine="    resource_group_name  = \""+resourceGroupName+"\"\n"	
# storageAccountNameTerraformBackendLine="    storage_account_name = \""+storageAccountNameTerraformBackend+"\"\n"	
# storageContainerNameLine="    container_name       = \""+storageContainerName+"\"\n"	
# terraBackendKeyLine="    key                  = \""+terraBackendKey+"\"\n"	

# tfFileNameAndPath=subDir4+"/terraform.tf"	
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

# print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-simple-example/drop/calls-to-modules/terraform-aws-simple-example-call-to-module")	
# print(*Path(subDir4).iterdir(), sep="\n")	


# print("About to call terraform init:  ")	
# initCommand="terraform init -backend=true -backend-config=\"access_key="+terraBackendKey+"\""  	

# runTerraformCommand(initCommand, subDir4 )	

# print("About to call terraform apply.  ")	

# applyCommand="terraform apply -auto-approve -var 'aws_region="+awsRegion+"' -var '_public_access_key="+awsPublicAccessKey+"' -var '_secret_access_key="+awsSecretAccessKey+"' -var 'vpcName="+vpc_name+"' -var 'systemName="+system_name+"' -var 'environmentName="+environment_name+"' -var 'ownerName="+owner_name+"' -var 'vmName="+vm_name+"'" 	
# runTerraformCommand(applyCommand, subDir4 )	

# #destroyCommand="terraform destroy -auto-approve -var 'aws_region="+awsRegion+"' -var '_public_access_key="+awsPublicAccessKey+"' -var '_secret_access_key="+awsSecretAccessKey+"' -var 'vpcName="+vpc_name+"' -var 'systemName="+system_name+"' -var 'environmentName="+environment_name+"' -var 'ownerName="+owner_name+"' -var 'vmName="+vm_name+"'" 	
# #runTerraformCommand(destroyCommand, subDir4 )
