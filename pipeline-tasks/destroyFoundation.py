## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import deploymentFunctions as depfunc
import os
from distutils.dir_util import copy_tree
from pathlib import Path
import platform
import shutil
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


###############################################################################################
### Functions
###############################################################################################
def destroyTheVMs(pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec):
  foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
  destinationVirtualMachineCallParent = pathToApplicationRoot + "\\calls-to-modules\\instances\\vm\\"
  #Now iterate the VM instances and remove each instance both in the cloud and then locally.
  vmInstanceNames = depfunc.getVirtualMachineInstanceNames(yamlConfigFileAndPath)
  print("vmInstanceNames is: ", vmInstanceNames)
  for vmName in vmInstanceNames: 
    print("vmName is; ", vmName)
    destinationVirtualMachineCallInstance = destinationVirtualMachineCallParent+foundationInstanceName+"-"+vmName+"-vm\\"  
    if os.path.exists(destinationVirtualMachineCallInstance) and os.path.isdir(destinationVirtualMachineCallInstance):
      ###
      ### Destroy The VM in cloud
      ###
      varsFragmentCompute = depfunc.getVarsFragmentVM(yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, depfunc.subnet_id, depfunc.sg_id, keySource, pub, sec)
      print("varsFragmentCompute for VM is: ", varsFragmentCompute)
      destroyCommandCompute = "terraform destroy -auto-approve" + varsFragmentCompute
      print("destroyCommandCompute is: ", destroyCommandCompute)
      # dirToUseVM = pathToApplicationRoot + "calls-to-modules\\aws-simple-vm-call-to-module\\"
      initCommand = 'terraform init '
      depfunc.runTerraformCommand(initCommand, destinationVirtualMachineCallInstance)
      depfunc.runTerraformCommand(destroyCommandCompute, destinationVirtualMachineCallInstance)  
      ### 
      ### Then destroy each instance of the calls to the vm modules in local agent file system
      ###
      if depfunc.terraformResult == "Destroyed": 
        print("Inside conditional block of things to do if destroy operation completed. ")
        #remove the instance of the call to the module, including its directory and any contents of that directory.  
        if os.path.exists(destinationVirtualMachineCallInstance) and os.path.isdir(destinationVirtualMachineCallInstance):
          #if not os.listdir(destinationVirtualMachineCallInstance):
          print("Directory is empty")
          path = Path(destinationVirtualMachineCallInstance)
          shutil.rmtree(path)
          #else:    
          #  print("Instance directory is not empty, so we will keep it for now:  ", destinationVirtualMachineCallInstance)
        else:
          print("Given Directory doesn't exist: ", destinationVirtualMachineCallInstance)
        #If parent is empty, delete parent directory also.  Otherwise, if parent directory is NOT empty, leave parent directory as-is.
        if os.path.exists(destinationVirtualMachineCallParent) and os.path.isdir(destinationVirtualMachineCallParent):
          if not os.listdir(destinationVirtualMachineCallParent):
            print("Directory is empty")
            path = Path(destinationVirtualMachineCallParent)
            shutil.rmtree(path)
          else:    
            print("Parent directory is not empty, so we will keep it for now: ", destinationVirtualMachineCallParent)
        else:
          print("Given Directory doesn't exist: ", destinationVirtualMachineCallParent)
    else:  
      print("The VM specified as \"", vmName, "\" does not have any corresponding call to a module that might manage it.  Either it does not exist or it is outside the scope of this program.  Specifically, the following directory does not exist: ", destinationVirtualMachineCallInstance)
      print("Therefore, we are not processing the request to remove the vm: \"", vmName, "\"")

def getOutputFromFoundation(yamlConfigFileAndPath, pathToApplicationRoot):
  foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
  # Get output from foundation
  destinationFoundationCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\network-foundation\\"+foundationInstanceName+"-network-foundation\\"  
  initCommand = 'terraform init '
  depfunc.runTerraformCommand(initCommand, destinationFoundationCallInstance)
  outputCommand = 'terraform output '  
  depfunc.runTerraformCommand(outputCommand, destinationFoundationCallInstance)
  #Now delete the tfvars file because we only want keys in the yaml input
  #os.remove(tfvarsFileAndPath)
  print("New output from foundation should have populated the following 3 variables: ")
  print("depfunc.vpc_id is: ", depfunc.vpc_id) 
  print("depfunc.subnet_id is: ", depfunc.subnet_id) 
  print("depfunc.sg_id is: ", depfunc.sg_id)

def destroyTheFoundation(yamlConfigFileAndPath, pathToApplicationRoot, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec):
  ############################################################################
  ### Destroy the Network Foundation 
  ############################################################################
  foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
  destinationFoundationCallParent = pathToApplicationRoot + "\\calls-to-modules\\instances\\network-foundation\\"
  destinationFoundationCallInstance = destinationFoundationCallParent+foundationInstanceName+"-network-foundation\\"  
  #\\NOTE: Pipeline version of this will create and use a remote backend.  But here in the demo laptop version we are using a local backend to keep it simple.
  varsFragmentNet = depfunc.getVarsFragmentFoundation(yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)
  print("varsFragmentNet is: ", varsFragmentNet)  
  destroyCommandNet = "terraform destroy -auto-approve" + varsFragmentNet
  print("destroyCommandNet is: ", destroyCommandNet)
  initCommand = 'terraform init '
  print("destinationFoundationCallInstance is: ", destinationFoundationCallInstance)
  try: 
    depfunc.runTerraformCommand(initCommand, destinationFoundationCallInstance)
    depfunc.runTerraformCommand(destroyCommandNet, destinationFoundationCallInstance)
  except NotADirectoryError:
    print("Instance of call to module does not exist, so we will not do anything here now.")
  #Now delete the tfvars file because we only want keys in the yaml input
  os.remove(tfvarsFileAndPath)
  #######################################################################################
  ### Remove the instance of the call to module, but only if the Destroyed flag was set.  
  #######################################################################################
  if depfunc.terraformResult == "Destroyed": 
    print("Inside conditional block of things to do if destroy operation completed. ")
    #remove the instance of the call to the module, including its directory and any contents of that directory.  
    path = Path(destinationFoundationCallInstance)
    shutil.rmtree(path)
    #If parent is empty, delete parent directory also.  Otherwise, if parent directory is NOT empty, leave parent directory as-is.
    if os.path.exists(destinationFoundationCallParent) and os.path.isdir(destinationFoundationCallParent):
      if not os.listdir(destinationFoundationCallParent):
        print("Directory is empty")
        path = Path(destinationFoundationCallParent)
        shutil.rmtree(path)
      else:    
        print("Parent directory is not empty, so we will keep it for now.  ")
    else:
      print("Given Directory doesn't exists")

def destroySecurityGroupRule(sgr, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, vpcCidr, sgId, sgName, destinationSecurityGroupRuleCallParent, keySource, pub, sec):
  print("sgr is: ", sgr)
  destinationSecurityGroupRuleCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\security-group-rules\\"+foundationInstanceName+"-"+sgr+"-sgr\\"  
  if os.path.exists(destinationSecurityGroupRuleCallInstance) and os.path.isdir(destinationSecurityGroupRuleCallInstance):
    print("destinationSecurityGroupRuleCallInstance is: ", destinationSecurityGroupRuleCallInstance)
    ### 
    ### Fist destroy the security group rules in the cloud
    ### 
    varsFragmentSG = depfunc.getVarsFragmentSecurityGroup(sgr, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, vpcCidr, sgId, sgName, keySource, pub, sec)  
    print("varsFragmentSG is: ", varsFragmentSG)
    destroyCommandSG = "terraform destroy -auto-approve" + varsFragmentSG
    print("destroyCommandSG is: ", destroyCommandSG)
    #dirToUseSG = pathToApplicationRoot + "calls-to-modules\\aws-simple-security-group-rules-call-to-module\\"
    initCommand = 'terraform init '
    depfunc.runTerraformCommand(initCommand, destinationSecurityGroupRuleCallInstance)
    depfunc.runTerraformCommand(destroyCommandSG, destinationSecurityGroupRuleCallInstance)
    ### 
    ### Then destroy each instance of the calls to the sgr modules in local agent file system
    ###
    #if depfunc.terraformResult == "Destroyed": 
    #  print("Inside conditional block of things to do if destroy operation completed. ")
    #remove the instance of the call to the module, including its directory and any contents of that directory.  
    if os.path.exists(destinationSecurityGroupRuleCallInstance) and os.path.isdir(destinationSecurityGroupRuleCallInstance):
      #if not os.listdir(destinationVirtualMachineCallInstance):
      print("Directory is empty")
      path = Path(destinationSecurityGroupRuleCallInstance)
      shutil.rmtree(path)
      #else:    
      #  print("Instance directory is not empty, so we will keep it for now:  ", destinationVirtualMachineCallInstance)
    else:
      print("Given Directory doesn't exist: ", destinationSecurityGroupRuleCallInstance)
    #If parent is empty, delete parent directory also.  Otherwise, if parent directory is NOT empty, leave parent directory as-is.
    if os.path.exists(destinationSecurityGroupRuleCallParent) and os.path.isdir(destinationSecurityGroupRuleCallParent):
      if not os.listdir(destinationSecurityGroupRuleCallParent):
        print("Directory is empty")
        path = Path(destinationSecurityGroupRuleCallParent)
        shutil.rmtree(path)
      else:    
        print("Parent directory is not empty, so we will keep it for now: ", destinationSecurityGroupRuleCallParent)
    else:
      print("Given Directory doesn't exist: ", destinationSecurityGroupRuleCallParent)
  else:
    print("There is no instance of a call to the security group rule module in any directory by the following name: ", destinationSecurityGroupRuleCallInstance)
    print("Add better error handling here based on the rules your organization defines. ")

def destroyTheBlobStorageInstance(blobStorageInstance, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, keySource, pub, sec):
  print("inside destroyTheBlobStorageInstance(), blobStorageInstance is: ", blobStorageInstance)
  destinationBlobStorageCallParent = pathToApplicationRoot + "\\calls-to-modules\\instances\\s3-backends\\"
  destinationBlobStorageCallInstance = destinationBlobStorageCallParent +foundationInstanceName+"-"+blobStorageInstance+"-s3\\"  
  #"\\calls-to-modules\\instances\\s3-backends\\"+foundationInstanceName+"-"+s3Instance+"-s3\\"  
  if os.path.exists(destinationBlobStorageCallInstance) and os.path.isdir(destinationBlobStorageCallInstance):
    print("destinationBlobStorageCallInstance is: ", destinationBlobStorageCallInstance)
    ### 
    ### Fist destroy the blobStorage instance in the cloud.  Note you have to empty the bucket first before terraform will allow you to delete it.  This has the potential to leave orphaned buckets in the cloud, which you will have to manage somehow.  
    ### 
    varsFragmentBlobStorage = depfunc.getVarsFragmentBlobStorage(blobStorageInstance, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, keySource, pub, sec)  
    print("varsFragmentBlobStorage is: ", varsFragmentBlobStorage)
    print("----------------------------------------------------------------------------------")
    destroyCommandBlobStorage = "terraform destroy -auto-approve" + varsFragmentBlobStorage
    print("destroyCommandBlobStorage is: ", destroyCommandBlobStorage)
    initCommand = 'terraform init '
    depfunc.runTerraformCommand(initCommand, destinationBlobStorageCallInstance)
    depfunc.runTerraformCommand(destroyCommandBlobStorage, destinationBlobStorageCallInstance)
    print("depfunc.terraformResult is: ", depfunc.terraformResult)

    if depfunc.terraformResult == "Destroyed":
      print("Inside the block only to be performed after the destroy operation was successfully completed by Terraform.  ")
      ### 
      ### Then destroy each instance of the calls to the blobStorage modules in local agent file system
      ### 
      ###
      #remove the instance of the call to the module, including its directory and any contents of that directory.  
      if os.path.exists(destinationBlobStorageCallInstance) and os.path.isdir(destinationBlobStorageCallInstance):
        #if not os.listdir(destinationS3CallInstance):
        print("Directory is empty.  About to delete: ", destinationBlobStorageCallInstance)
        path = Path(destinationBlobStorageCallInstance)
        shutil.rmtree(path)
        #else:    
        #  print("Instance directory is not empty, so we will keep it for now:  ", destinationVirtualMachineCallInstance)
      else:
        print("Given Directory doesn't exist: ", destinationBlobStorageCallInstance)
      #If parent is empty, delete parent directory also.  Otherwise, if parent directory is NOT empty, leave parent directory as-is.
      if os.path.exists(destinationBlobStorageCallParent) and os.path.isdir(destinationBlobStorageCallParent):
        if not os.listdir(destinationBlobStorageCallParent):
          print("Directory is empty")
          path = Path(destinationBlobStorageCallParent)
          shutil.rmtree(path)
        else:    
          print("Parent directory is not empty, so we will keep it for now: ", destinationBlobStorageCallParent)
      else:
        print("Given Directory doesn't exist: ", destinationBlobStorageCallParent)
  else:
    print("There is no instance of a call to the blobStorage module in any directory by the following name: ", destinationBlobStorageCallInstance)
    print("Add better error handling here based on the rules your organization defines. ")


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


#############################################################################
### Get Output Variables From Foundation Module Instance
#############################################################################
getOutputFromFoundation(yamlConfigFileAndPath, pathToApplicationRoot)

################################################################################
### Create blobStorage Backend and attach to the foundation
################################################################################
#Get some input vars from output from the network foundation module.  
#depfunc.runTerraformCommand('terraform output', dirToUseNet)
foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
print("For blobStorage: depfunc.vpc_id is: ", depfunc.vpc_id) 
blobStorageInstanceNames = depfunc.getBlobStorageInstanceNames(yamlConfigFileAndPath)
print("blobStorageInstanceNames is:", blobStorageInstanceNames)
for blobStorageInstance in blobStorageInstanceNames:
  destroyTheBlobStorageInstance(blobStorageInstance, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, keySource, pub, sec)



##############################################################################
### Destroy the Security Group Rules then destroy their call instances one by one
##############################################################################
foundationInstanceName = depfunc.getFoundationInstanceName(yamlConfigFileAndPath)
destinationSecurityGroupRuleCallParent = pathToApplicationRoot + "\\calls-to-modules\\instances\\security-group-rules\\"
sgrInstanceNames = depfunc.getSecurityGroupRuleInstanceNames(yamlConfigFileAndPath) 
print("sgrInstanceNames is: ", sgrInstanceNames)
for sgr in sgrInstanceNames:
  #Get some input vars from output from the network foundation module.  
  print("depfunc.vpc_id is: ", depfunc.vpc_id) 
  print("depfunc.vpc_cidr is: ", depfunc.vpc_cidr)
  print("depfunc.sg_id is: ", depfunc.sg_id)
  print("depfunc.sg_name is: ", depfunc.sg_name)
  destroySecurityGroupRule(sgr, pathToApplicationRoot, foundationInstanceName, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name, destinationSecurityGroupRuleCallParent, keySource, pub, sec)

##############################################################################
### Destroy the Virtual Machines then destroy their call instances one by one
##############################################################################
destroyTheVMs(pathToApplicationRoot, yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)

##########################################################################################
### Destroy the Network Foundation and the Instance of the Call To The Foundation Module
##########################################################################################
destroyTheFoundation(yamlConfigFileAndPath, pathToApplicationRoot, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#///////////////////////////////////////////////////////////////
# BELOW HERE IS OBSOLETE OLD AND TO BE REMOVED.
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#///////////////////////////////////////////////////////////////

# ################################################################################
# ### Destroy the S3 Backend 
# ################################################################################
# #Get some input vars from output from the network foundation module.  
# depfunc.runTerraformCommand('terraform output', dirToUseNet)
# print("depfunc.vpc_id is: ", depfunc.vpc_id) 
# varsFragmentS3Backend = depfunc.getVarsFragmentS3Backend(yamlConfigFileAndPath, depfunc.vpc_id)
# print("varsFragmentS3Backend is: ", varsFragmentS3Backend)
# destroyCommandS3Backend = "terraform destroy -auto-approve" + varsFragmentS3Backend
# print("destroyCommandS3Backend is: ", destroyCommandS3Backend)
# depfunc.runTerraformCommand(initCommand, dirToUseS3Backend)
# depfunc.runTerraformCommand(destroyCommandS3Backend, dirToUseS3Backend)

# #############################################################################
# ### Destroy the security group rule
# #############################################################################
# #Get some input vars from output from the network foundation module.  
# depfunc.runTerraformCommand('terraform output', dirToUseNet)
# print("depfunc.vpc_id is: ", depfunc.vpc_id) 
# print("depfunc.vpc_cidr is: ", depfunc.vpc_cidr)
# print("depfunc.sg_id is: ", depfunc.sg_id)
# print("depfunc.sg_name is: ", depfunc.sg_name)
# varsFragmentSG = depfunc.getVarsFragmentSecurityGroup(yamlConfigFileAndPath, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name)  
# print("varsFragmentSG is: ", varsFragmentSG)
# destroyCommandSG = "terraform destroy -auto-approve" + varsFragmentSG
# print("destroyCommandSG is: ", destroyCommandSG)
# depfunc.runTerraformCommand(initCommand, dirToUseSG)
# depfunc.runTerraformCommand(destroyCommandSG, dirToUseSG)

# ###############################################################################
# ### Destroy the virtual machine
# ###############################################################################
# #Get some input vars from output from the network foundation module.  
# depfunc.runTerraformCommand('terraform output', dirToUseNet)
# print("depfunc.vpc_id is: ", depfunc.vpc_id) 
# print("depfunc.subnet_id is: ", depfunc.subnet_id) 
# print("depfunc.sg_id is: ", depfunc.sg_id)
# varsFragmentCompute = depfunc.getVarsFragmentVM(yamlConfigFileAndPath, depfunc.vpc_id, depfunc.subnet_id, depfunc.sg_id)  
# print("varsFragmentCompute for VM is: ", varsFragmentCompute)
# destroyCommandCompute = "terraform destroy -auto-approve" + varsFragmentCompute
# print("destroyCommandCompute is: ", destroyCommandCompute)
# depfunc.runTerraformCommand(initCommand, dirToUseVM)
# depfunc.runTerraformCommand(destroyCommandCompute, dirToUseVM)  

# ###############################################################################
# ### Destroy the foundation 
# ###############################################################################
# varsFragmentNet = depfunc.getVarsFragmentFoundation(yamlConfigFileAndPath)
# print("varsFragmentNet is: ", varsFragmentNet)  
# destroyCommandNet = "terraform destroy -auto-approve" + varsFragmentNet
# print("destroyCommandNet is: ", destroyCommandNet)
# depfunc.runTerraformCommand(initCommand, dirToUseNet)
# depfunc.runTerraformCommand(destroyCommandNet, dirToUseNet)
