## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import deploymentFunctions as depfunc
import os
from distutils.dir_util import copy_tree
from pathlib import Path
import platform
import sys

#Dummy key values that will be replaced by pipeline inputs
pub = "empty"
sec = "empty"

print("len(sys.argv) is: ", len(sys.argv))
if len(sys.argv) > 1:  
  keySource=sys.argv[1]
  if keySource != "keyVault":
    print("keySource is NOT set to a valid value.  ")
else:  
  keySource = "keyFile"

print("keySource is: ", keySource)

  
#############################################################################
### Functions
#############################################################################
def createTheFoundation(pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec):
  ############################################################################
  ### Copy the foundation template into a new instance.  Modify for OS. 
  ############################################################################
  foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
  sourceOfFoundationCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\network-foundation\\"
  destinationFoundationCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\network-foundation\\"+foundationInstanceName+"-network-foundation\\"  
  #Create destination directory if it does not already exist 
  Path(destinationFoundationCallInstance).mkdir(parents=True, exist_ok=True)
  #Copy config and secret templates outside app path before they can be safely populated
  copy_tree(sourceOfFoundationCallTemplate, destinationFoundationCallInstance)
  #Modify main.tf so that it points to the correct module directory
  fileName = destinationFoundationCallInstance + "main.tf"
  #Isolating error by commenting the next block.
  if platform.system() == 'Windows':
    print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
    searchTerm = "/modules/"
    depfunc.deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
  else: 
    print("Need to write code to handle Linux separately.  ")
  newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-network-foundation\""
  searchTerm = "\\modules\\"
  depfunc.changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)

  #\\NOTE: Pipeline version of this will create and use a remote backend.  But here in the demo laptop version we are using a local backend to keep it simple.

  #############################################################################
  ### Create the network foundation
  #############################################################################
  varsFragmentNet = depfunc.getVarsFragmentFoundation(yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)
  print("varsFragmentNet is: ", varsFragmentNet)  
  applyCommandNet = "terraform apply -auto-approve" + varsFragmentNet
  print("applyCommandNet is: ", applyCommandNet)
  initCommand = 'terraform init '
  depfunc.runTerraformCommand(initCommand, destinationFoundationCallInstance)
  validationCommand = 'terraform validate'  
  depfunc.runTerraformCommand(validationCommand, destinationFoundationCallInstance)
  #upgradeCommand = 'terraform 0.12upgrade -auto-approve'
  #depfunc.runTerraformCommand(upgradeCommand, destinationFoundationCallInstance)
  depfunc.runTerraformCommand(applyCommandNet, destinationFoundationCallInstance)
  #Now delete the tfvars file because we only want keys in the yaml input
  os.remove(tfvarsFileAndPath)


def createTheVMs(foundationInstanceName, vmInstanceNames, pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec):
  for vmName in vmInstanceNames: 
    print("vmName is; ", vmName)
    sourceOfVirtualMachineCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\vm\\"
    destinationVirtualMachineCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\vm\\"+foundationInstanceName+"-"+vmName+"-vm\\"  
    #Create destination directory if it does not already exist 
    Path(destinationVirtualMachineCallInstance).mkdir(parents=True, exist_ok=True)
    #Copy config and secret templates outside app path before they can be safely populated
    copy_tree(sourceOfVirtualMachineCallTemplate, destinationVirtualMachineCallInstance)
    #Modify main.tf so that it points to the correct module directory
    fileName = destinationVirtualMachineCallInstance + "main.tf"
    #Isolating error by commenting the next block.
    if platform.system() == 'Windows':
      print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
      searchTerm = "/modules/"
      depfunc.deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    else: 
      print("Need to write code to handle Linux separately.  ")
    newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-vm\""
    #newPointerLine="  source = \"" + destinationVirtualMachineCallInstance + "\"""
    searchTerm = "\\modules\\"
    depfunc.changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)

    ##############################################################################
    ### Create Virtual Machine and attach to the foundation
    ##############################################################################
    print("depfunc.vpc_id is: ", depfunc.vpc_id) 
    print("depfunc.subnet_id is: ", depfunc.subnet_id) 
    print("depfunc.sg_id is: ", depfunc.sg_id)
    varsFragmentCompute = depfunc.getVarsFragmentVM(yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, depfunc.subnet_id, depfunc.sg_id, keySource, pub, sec)
    print("varsFragmentCompute for VM is: ", varsFragmentCompute)
    applyCommandCompute = "terraform apply -auto-approve" + varsFragmentCompute
    print("applyCommandCompute is: ", applyCommandCompute)
    # dirToUseVM = pathToApplicationRoot + "calls-to-modules\\aws-simple-vm-call-to-module\\"
    initCommand = 'terraform init '
    depfunc.runTerraformCommand(initCommand, destinationVirtualMachineCallInstance)
    depfunc.runTerraformCommand(applyCommandCompute, destinationVirtualMachineCallInstance)  

    if depfunc.terraformResult == "Applied": 
      print("Apply operation succeeded for VM.  If it had failed, this block of code would instead automatically quit the program. ")
    else: 
        quit("Terminating program because the Apply operation failed for a VM in Terraform.")


def createTheSecurityGroupRule(sgr, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, vpcCidr, sgId, sgName, keySource, pub, sec):
  print("...................................................................................................")
  print("sgr is: ", sgr)
  sourceOfSecurityGroupRuleCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\security-group-rules\\"
  destinationSecurityGroupRuleCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\security-group-rules\\"+foundationInstanceName+"-"+sgr+"-sgr\\"  
  print("sourceOfSecurityGroupRuleCallTemplate is: ", sourceOfSecurityGroupRuleCallTemplate)
  print("destinationSecurityGroupRuleCallInstance is: ", destinationSecurityGroupRuleCallInstance)
  #Create destination directory if it does not already exist 
  Path(destinationSecurityGroupRuleCallInstance).mkdir(parents=True, exist_ok=True)
  #Copy config and secret templates outside app path before they can be safely populated
  copy_tree(sourceOfSecurityGroupRuleCallTemplate, destinationSecurityGroupRuleCallInstance)
  #Modify main.tf so that it points to the correct module directory
  fileName = destinationSecurityGroupRuleCallInstance + "main.tf"
  #Isolating error by commenting the next block.
  if platform.system() == 'Windows':
    print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
    searchTerm = "/modules/"
    depfunc.deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
  else: 
    print("Need to write code to handle Linux separately.  ")
  newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-security-group-rules\""
  #newPointerLine="  source = \"" + destinationVirtualMachineCallInstance + "\"""
  searchTerm = "\\modules\\"
  depfunc.changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  varsFragmentSG = depfunc.getVarsFragmentSecurityGroup(sgr, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, vpcCidr, sgId, sgName, keySource, pub, sec)  
  print("varsFragmentSG is: ", varsFragmentSG)
  print("----------------------------------------------------------------------------------")
  applyCommandSG = "terraform apply -auto-approve" + varsFragmentSG
  print("applyCommandSG is: ", applyCommandSG)
  initCommand = 'terraform init '
  depfunc.runTerraformCommand(initCommand, destinationSecurityGroupRuleCallInstance)
  depfunc.runTerraformCommand(applyCommandSG, destinationSecurityGroupRuleCallInstance)

def createTheBlobStorageInstance(blobStorageInstance, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, keySource, pub, sec):
  print("Inside createTheBlobStorageInstance(), blobStorageInstance is: ", blobStorageInstance)
  sourceOfBlobStorageCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\s3-backend\\"
  destinationBlobStorageCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\s3-backends\\"+foundationInstanceName+"-"+blobStorageInstance+"-s3\\"  
  print("sourceOfBlobStorageCallTemplate is: ", sourceOfBlobStorageCallTemplate)
  print("destinationBlobStorageCallInstance is: ", destinationBlobStorageCallInstance)
  #Create destination directory if it does not already exist 
  Path(destinationBlobStorageCallInstance).mkdir(parents=True, exist_ok=True)
  #Copy config and secret templates outside app path before they can be safely populated
  copy_tree(sourceOfBlobStorageCallTemplate, destinationBlobStorageCallInstance)
  #
  #Modify main.tf so that it points to the correct module directory
  fileName = destinationBlobStorageCallInstance + "main.tf"
  #Isolating error by commenting the next block.
  if platform.system() == 'Windows':
    print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
    searchTerm = "/modules/"
    depfunc.deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
  else: 
    print("Need to write code to handle Linux separately.  ")
  newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-S3-backend\""
  #newPointerLine="  source = \"" + destinationVirtualMachineCallInstance + "\"""
  searchTerm = "\\modules\\"
  depfunc.changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  varsFragmentBlobStorage = depfunc.getVarsFragmentBlobStorage(blobStorageInstance, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, keySource, pub, sec)  
  print("varsFragmentBlobStorage is: ", varsFragmentBlobStorage)
  print("----------------------------------------------------------------------------------")
  applyCommandBlobStorage = "terraform apply -auto-approve" + varsFragmentBlobStorage
  print("applyCommandBlobStorage is: ", applyCommandBlobStorage)
  initCommand = 'terraform init '
  depfunc.runTerraformCommand(initCommand, destinationBlobStorageCallInstance)
  depfunc.runTerraformCommand(applyCommandBlobStorage, destinationBlobStorageCallInstance)



#############################################################################
### Import path locations relative to application root
#############################################################################
app_parent_path = os.path.dirname(os.path.realpath("..\\"))
dirOfYamlFile = app_parent_path+"\\config-and-secrets-outside-app-path\\" + "vars\\yamlInputs\\"
nameOfYamlConfigFile = 'varsFromDevLaptop.yaml'
yamlConfigFileAndPath = dirOfYamlFile + nameOfYamlConfigFile
nameOfYamlKeysFile = 'keys.yaml'
yamlKeysFileAndPath = dirOfYamlFile + nameOfYamlKeysFile 
pathToApplicationRoot = os.path.dirname(os.path.realpath(""))
dirOfTfvarsFile = app_parent_path+"\\config-and-secrets-outside-app-path\\vars\\VarsForTerraform\\"
nameOfTfvarsFile = 'keys.tfvars'
tfvarsFileAndPath = dirOfTfvarsFile + nameOfTfvarsFile


##############################################################################
### Create Infrastructure By Calling The Functions
##############################################################################
createTheFoundation(pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)

if depfunc.terraformResult == "Applied": 
  print("Apply operation succeeded.  Now inside Python conditional block to do only after the Apply operation has succeeded. ")
  ##############################################################################
  ### Copy the template into a new instance of a call to the vm module
  ##############################################################################
  foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
  vmInstanceNames = depfunc.getVirtualMachineInstanceNames(yamlConfigFileAndPath)
  print("vmInstanceNames is: ", vmInstanceNames)
  createTheVMs(foundationInstanceName, vmInstanceNames, pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)
  
  ###############################################################################
  ### Create Security Group Rule and attach to the foundation and VM.  
  ###############################################################################
  #
  sgrInstanceNames = depfunc.getSecurityGroupRuleInstanceNames(yamlConfigFileAndPath) 
  print("sgrInstanceNames is: ", sgrInstanceNames)
  for sgr in sgrInstanceNames:
    #Create each security group rule
    createTheSecurityGroupRule(sgr, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name, keySource, pub, sec)

  ################################################################################
  ### Create S3 Backend and attach to the foundation
  ################################################################################
  #Get some input vars from output from the network foundation module.  
  #depfunc.runTerraformCommand('terraform output', dirToUseNet)
  print("For blobStorage: depfunc.vpc_id is: ", depfunc.vpc_id) 
  blobStorageInstanceNames = depfunc.getBlobStorageInstanceNames(yamlConfigFileAndPath)
  print("blobStorageInstanceNames is:", blobStorageInstanceNames)
  for blobStorageInstance in blobStorageInstanceNames:
    createTheBlobStorageInstance(blobStorageInstance, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, keySource, pub, sec)
