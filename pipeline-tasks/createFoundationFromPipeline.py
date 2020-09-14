import sys  	
import re	
import os	
import subprocess  	
from pathlib import Path	
import pip  
import deploymentFunctions as depfunc  
 
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')	

print("Hello from inside createStarterFromPipeline.py ")  	

def runShellCommand(commandToRun):
    print("Inside runShellCommand(..., ...) function. ")
    print("commandToRun is: " +commandToRun)

    proc = subprocess.Popen( commandToRun,cwd=None, stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
      else:
        break

#Re-usable function that will be replaced with something already in depfunc
def runTerraformCommand(commandToRun, workingDir ):	
    print("Inside runTerraformCommand(..., ...) function. ")	
    print("commandToRun is: " +commandToRun)	
    print("workingDir is: " +workingDir)	
    proc = subprocess.Popen( commandToRun,cwd=workingDir,stdout=subprocess.PIPE, shell=True)	
    while True:	
      print("there is a subprocess.  ")
      line = proc.stdout.readline()	
      if line:	
        print("there is a line. ")
        thetext=line.decode('utf-8').rstrip('\r|\n')	
        decodedline=ansi_escape.sub('', thetext)	
        print(decodedline)	
      else:	
        print("About to break. ")
        break	

###############################################################################
### Check to see if storage key environment variable was set
###############################################################################
print("about to echo ARM_ACCESS_KEY : ")
runShellCommand("echo $ARM_ACCESS_KEY")


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
#clientSecret=sys.argv[8]
#subscriptionId=sys.argv[9]
#tenandId=sys.argv[10]
#$(client-id)  $(client-secret)  $(subscription-id)  $(tenant-id)  
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

# exportString = 'export ARM_ACCESS_KEY=' +demoStorageKey +"\n"
# with open(os.path.expanduser("/home/azureuser/.bashrc"), "a") as outfile:
#     # 'a' stands for "append"  
#     outfile.write(exportString)
# #"export MYVAR=MYVALUE"
# print("About to read the /home/azureuser/.bashrc file we just wrote to.")	
# #open and read the file after the appending: 
# f = open("/home/azureuser/.bashrc", "r") 
# print(f.read()) 

print("about to whoami: ")
runShellCommand("whoami")
 
# print("about to echo ARM_ACCESS_KEY : ")
# runShellCommand("echo $ARM_ACCESS_KEY")
#print(os.environ)
#print("ARM_ACCESS_KEY environment variable is: ", os.environ['ARM_ACCESS_KEY'])
print("Python version is: ", sys.version_info[0])  	
print("awsPublicAccessKey is: ", awsPublicAccessKey)	
print("awsSecretAccessKey is: ", awsSecretAccessKey)	
print("storageAccountNameTerraformBackend is: ", storageAccountNameTerraformBackend)	
print("terraBackendKey is: ", terraBackendKey)	
print("awsRegion is: ", awsRegion)	
print("DefaultWorkingDirectory is: ", DefaultWorkingDirectory)	
print("demoStorageKey is: ", demoStorageKey)
foundationSecretsFile = '/home/azureuser/' + 'foundationSecrets.tfvars'
#print("clientSecret is: ", clientSecret)
#print("subscriptionId is: ", subscriptionId)
#print("tenandId is: ", tenandId)

#Set environment variable
#os.environ["ARM_ACCESS_KEY"] = demoStorageKey

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
resourceGroupNameLine="    resource_group_name  = \""+resourceGroupName+"\"\n"	
storageAccountNameTerraformBackendLine="    storage_account_name = \""+storageAccountNameTerraformBackend+"\"\n"	
storageContainerNameLine="    container_name       = \""+storageContainerName+"\"\n"	
terraBackendKeyLine="    key                  = \""+terraKeyFileName+"\"\n"	

# terraform {
#   backend "azurerm" {
#     resource_group_name   = "pipeline-resources"
#     storage_account_name  = "tstate17202"
#     container_name        = "tstate"
#     key                   = "terraform.tfstate"
#   }
# }


tfFileNameAndPath=dirToUseNet+"/terraform.tf"	
print("tfFileNameAndPath is: ", tfFileNameAndPath)	
print("About to write 8 lines to a file.")	
f = open(tfFileNameAndPath, "w")	
f.write("terraform {\n")	
f.write("  backend \"azurerm\" {\n")	
f.write(resourceGroupNameLine)	
f.write(storageAccountNameTerraformBackendLine)	
f.write(storageContainerNameLine)	
f.write(terraBackendKeyLine)	
f.write("  }\n")	
f.write("}\n")	
f.close()	

print("About to read the file we just wrote.")	
#open and read the file after the appending:	
f = open(tfFileNameAndPath, "r")	
print(f.read()) 	

print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
print(*Path(dirToUseNet).iterdir(), sep="\n")	


print("About to call terraform init:  ")	
#initCommand="terraform init -backend=true "  	
initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
# initCommand="terraform init "
# -backend=true -backend-config=\"client_id="+clientId+"\" " + "-backend-config=\"client_secret="+clientSecret+"\" " + "-backend-config=\"subscription_id="+subscriptionId+"\" " + "-backend-config=\"tenant_id="+tenandId+"\""  	

runTerraformCommand(initCommand, dirToUseNet )	
  
#############################################################################
### Create the network foundation
#############################################################################
#Get Vars to pass into terraform commands:
varsFragmentFoundation = ""  
varsFragmentFoundation = varsFragmentFoundation + " -var=\"aws_region=" + awsRegion +"\""  
varsFragmentFoundation = varsFragmentFoundation + " -var=\"vpcName=" + vpc_name +"\""  
varsFragmentFoundation = varsFragmentFoundation + " -var=\"systemName=" + system_name +"\""  
varsFragmentFoundation = varsFragmentFoundation + " -var=\"environmentName=" + environment_name +"\""  
varsFragmentFoundation = varsFragmentFoundation + " -var=\"ownerName=" + owner_name +"\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"_public_access_key=" + awsPublicAccessKey +"\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"_secret_access_key=" + awsSecretAccessKey +"\""  
if len(awsPublicAccessKey)>2 or len(awsSecretAccessKey)>2 :  
  with open(foundationSecretsFile, "w") as file:
    if len(awsPublicAccessKey) > 2:
      lineToAdd = "_public_access_key=\""+awsPublicAccessKey +"\"\n"
      file.write(lineToAdd)
    if len(awsSecretAccessKey) > 2:
      lineToAdd = "_secret_access_key=\""+awsSecretAccessKey +"\"\n"
      file.write(lineToAdd)
  varsFragmentFoundation = varsFragmentFoundation + " -var-file=\""+ foundationSecretsFile +"\""

varsFoundation = varsFragmentFoundation
print("varsFoundation is: ", varsFoundation)  
applyCommandNet = "terraform apply -auto-approve" + varsFoundation
print("applyCommandNet is: ", applyCommandNet)
print("dirToUseNet is: ", dirToUseNet)
runTerraformCommand(applyCommandNet, dirToUseNet)  

print("Finished running apply command. ")

#THE FOLLOWING ARE FOR OTHER MODULES:  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"vmName=" + vm_name +"\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"amiId=ami-id-goesw-here\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"s3BucketNameTF=bucket-name-goes-here\""  
#varsFragmentFoundation = varsFragmentFoundation + " -var=\"dynamoDbTableNameTF=table-name-goes-here\""  


#DELETE BY UNCOMMENTING THE FOLLOWING DURING DEVELOPMENT, THEN MAKE SEPARATE FILE FOR RELEASE:  
# print("About to call terraform destroy.  ")    
# destroyCommand="terraform destroy -auto-approve" + varsFoundation
# runTerraformCommand(destroyCommand, subDir4 )  
