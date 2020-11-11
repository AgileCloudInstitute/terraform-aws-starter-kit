## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess
import yaml
import re
import fileinput 
import os 
<<<<<<< HEAD
import platform
from distutils.dir_util import copy_tree
from pathlib import Path
import shutil
import sys

=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

vpc_id = ''  
vpc_cidr = ''  
subnet_id = ''  
sg_id = ''  
sg_name = ''  
<<<<<<< HEAD
vm_ip_pub = ''
=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031
terraformResult = ''  

def runShellCommand(commandToRun):
    print("Inside runShellCommand(...) function. ")
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

def runShellCommandInWorkingDir(commandToRun, workingDir):
    print("Inside runShellCommandInWorkingDir(...) function. ")
    print("commandToRun is: " +commandToRun)

    proc = subprocess.Popen( commandToRun,cwd=workingDir, stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
      else:
        break

def getFoundationInstanceName(yamlFileAndPath):
  instanceName = ""  
  with open(yamlFileAndPath) as f:  
    topLevel_dict = yaml.safe_load(f)
    for item in topLevel_dict:
      if re.match("networkFoundation", item):
        foundationItems = topLevel_dict.get(item)
        for foundationItem in foundationItems: 
          if re.match("instanceName", foundationItem):
            instanceName = foundationItems.get(foundationItem)
  #if len(instanceName) < 2:
  #  exit(1)
  return instanceName

def getVirtualMachineInstanceNames(yamlFileAndPath):
  instanceNames = []
  with open(yamlFileAndPath) as f:  
    topLevel_dict = yaml.safe_load(f)
    for item in topLevel_dict:
      if re.match("standaloneVms", item):
        vms = topLevel_dict.get(item)
        for vm in vms: 
          instanceName = vm.get("vmName")
          if len(instanceName) > 0:
            print("len(instanceName) is: ", len(instanceName))
            instanceNames.append(instanceName)
  return instanceNames

def getSecurityGroupRuleInstanceNames(yamlFileAndPath):
  instanceNames = []
  with open(yamlFileAndPath) as f:  
    topLevel_dict = yaml.safe_load(f)
    for item in topLevel_dict:
      if re.match("securityGroupRules", item):
        sgrs = topLevel_dict.get(item)
        print("sgrs is: ", sgrs)
        for sgr in sgrs: 
          instanceName = sgr.get("ruleName")
          if len(instanceName) > 0:
            print("len(instanceName) is: ", len(instanceName))
            instanceNames.append(instanceName)
  return instanceNames

def getBlobStorageInstanceNames(yamlFileAndPath):
  instanceNames = []
  with open(yamlFileAndPath) as f:  
    topLevel_dict = yaml.safe_load(f)
    for item in topLevel_dict:
      if re.match("blobStorage", item):
        blobs = topLevel_dict.get(item)
        print("blobs is: ", blobs)
        for blob in blobs: 
          instanceName = blob.get("bucketName")
          if len(instanceName) > 0:
            print("len(instanceName) is: ", len(instanceName))
            instanceNames.append(instanceName)
  return instanceNames

<<<<<<< HEAD
#def getStandaloneVirtualMachineNames(yamlFileAndPath):
#  vmNames = []
#  with open(yamlFileAndPath) as f:  
#    topLevel_dict = yaml.safe_load(f)
#    for item in topLevel_dict:
#      if re.match("standaloneVms", item):
#        vms = topLevel_dict.get(item)
#        print("vms is: ", vms)
#        for vm in vms: 
#          vmName = vm.get("vmName")
#          if len(vmName) > 0:
#            print("len(vmName) is: ", len(vmName))
#            vmNames.append(vmName)
#  return vmNames

=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031
def changePointerLineInCallToModule(fileName, searchTerm, newPointerLine): 
  print("inside depfunc.changePointerLineInCallToModule(...)")
  print("newPointerLine is: ", newPointerLine)
  with fileinput.FileInput(fileName, inplace = True) as f: 
    for line in f: 
      if searchTerm in line: 
        #print(newPointerLine) 
        print(newPointerLine, end ='\n') 
      else: 
        print(line, end ='') 

def deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm): 
  with fileinput.FileInput(fileName, inplace = True) as f: 
    for line in f: 
      if searchTerm in line: 
        print('', end ='\n') 
      else: 
        print(line, end ='') 


# #Took the following from createFoundationFromPipeline.py .  Note to delete this version if tests pass.  
# #Re-usable function that will be replaced with something already in depfunc
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
#         print("About to break. ")
#         break	

def runTerraformCommand(commandToRun, workingDir ):
    print("Inside deploymentFunctions.py script and runTerraformCommand(..., ...) function. ")
    print("commandToRun is: " +commandToRun)
    print("workingDir is: " +workingDir)

    proc = subprocess.Popen( commandToRun,cwd=workingDir,stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
        if "Outputs:" in decodedline:  
          print("Reached \"Outputs\" section: ")
          print("decodedline is: " +decodedline)
        if "vpc_id" in decodedline:
          print("Found vpc_id!")
          global vpc_id
          vpc_id=decodedline[9:]
          print("vpc_id in deploymentFunctions.py is: ", vpc_id)
        if "vpc_cidr" in decodedline:
          print("Found vpc_cidr!")
          global vpc_cidr
          vpc_cidr=decodedline[11:]
          print("vpc_cidr in deploymentFunctions.py is: ", vpc_cidr)
        if "subnet_id" in decodedline:
          print("Found subnet_id!")
          global subnet_id
          subnet_id=decodedline[12:]
          print("subnet_id in deploymentFunctions.py is: ", subnet_id)
        if "sg_id" in decodedline:
          print("Found sg_id!")
          global sg_id
          sg_id=decodedline[8:]
          print("sg_id in deploymentFunctions.py is: ", sg_id)
        if "sg_name" in decodedline:
          print("Found sg_name!")
          global sg_name
          sg_name=decodedline[10:]
          print("sg_name in deploymentFunctions.py is: ", sg_name)
<<<<<<< HEAD
        if "public_ip_of_ec2_instance" in decodedline:
          print("Found public_ip_of_ec2_instance!")
          global vm_ip_pub
          vm_ip_pub=decodedline[28:].replace('"', '')
          print("public_ip_of_ec2_instance in deploymentFunctions.py is: ", vm_ip_pub)
=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031
        if "Destroy complete!" in decodedline:
          print("Found Destroy complete!!")
          global terraformResult
          terraformResult="Destroyed"
        if "Apply complete!" in decodedline:
          print("Found Apply complete!!")
          #global terraformResult
          terraformResult="Applied"
      else:
        break

<<<<<<< HEAD
def createBackendConfigFileTerraform(dir_to_use_net, **params): 
  resource_group_name = params.get('resGroupName')
  storage_account_name_terraform_backend = params.get('storageAccountNameTerraformBackend')
  storage_container_name = params.get('storContainerName')
  terra_key_file_name = params.get('keyFileTF')
=======
def createBackendConfigFileTerraform(resource_group_name, storage_account_name_terraform_backend, storage_container_name, terra_key_file_name, dir_to_use_net ): 
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031
  resourceGroupNameLine="    resource_group_name  = \""+resource_group_name+"\"\n"	
  storageAccountNameTerraformBackendLine="    storage_account_name = \""+storage_account_name_terraform_backend+"\"\n"	
  storageContainerNameLine="    container_name       = \""+storage_container_name+"\"\n"	
  terraBackendKeyLine="    key                  = \""+terra_key_file_name+"\"\n"	
  tfFileNameAndPath=dir_to_use_net+"/terraform.tf" 
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
<<<<<<< HEAD
  print("About to read the file we just wrote.") 
  f = open(tfFileNameAndPath, "r") 
  print(f.read())  
=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031

def getInputVarsFoundationFromPipeline(aws_region, vpcName, systemName, environmentName, owner_name, aws_public_access_key, aws_secret_access_key, foundation_secrets_file):  
  varsFragmentFoundation = ""  
  varsFragmentFoundation = varsFragmentFoundation + " -var=\"aws_region=" + aws_region +"\""  
  varsFragmentFoundation = varsFragmentFoundation + " -var=\"vpcName=" + vpcName +"\""  
  varsFragmentFoundation = varsFragmentFoundation + " -var=\"systemName=" + systemName +"\""  
  varsFragmentFoundation = varsFragmentFoundation + " -var=\"environmentName=" + environmentName +"\""  
  varsFragmentFoundation = varsFragmentFoundation + " -var=\"ownerName=" + owner_name +"\""  
  if len(aws_public_access_key)>2 or len(aws_secret_access_key)>2 :  
    with open(foundation_secrets_file, "w") as file:
      if len(aws_public_access_key) > 2:
        lineToAdd = "_public_access_key=\""+aws_public_access_key +"\"\n"
        file.write(lineToAdd)
      if len(aws_secret_access_key) > 2:
        lineToAdd = "_secret_access_key=\""+aws_secret_access_key +"\"\n"
        file.write(lineToAdd)
    varsFragmentFoundation = varsFragmentFoundation + " -var-file=\""+ foundation_secrets_file +"\""
  return varsFragmentFoundation

#Old version below being commented out until integration tests run later.  
#def getVarsFragmentFoundation(yamlConfigFileAndPath):  
#  varsFragmentFoundation = ""  
#  with open(yamlConfigFileAndPath) as f:  
#    my_dict = yaml.safe_load(f)  
#    for key, value in my_dict.items():  
#      print(key, " is: ", value)  
#      if re.match("aws_region", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("vpcName", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("systemName", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("environmentName", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("ownerName", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("_public_access_key", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#      if re.match("_secret_access_key", key):  
#        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
#  return varsFragmentFoundation

def getVarsFragmentFoundation(yamlConfigFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, keySource, pub, sec):  
  varsFragmentFoundation = ""
  instanceName = ''
  keyPairName = ''
  secretKeyLine = ''
  publicKeyLine = ''
  with open(yamlConfigFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("networkFoundation", key):
        netFoundationItems = my_dict.get(key)
        for networkItem in netFoundationItems:
          if re.match("instanceName", networkItem):
            instanceName = netFoundationItems.get(networkItem)
            keyPairName = instanceName + 'KeyPair'
          if re.match("region", networkItem):
            varsFragmentFoundation = varsFragmentFoundation + " -var=\"aws_region="+netFoundationItems.get(networkItem) +"\""  
      if re.match("tags", key):
        tags = my_dict.get(key)
        for tag in tags:
          if re.match("networkName", tag):
            varsFragmentFoundation = varsFragmentFoundation + " -var=\"vpcName="+tags.get(tag) +"\""  
          if re.match("systemName", tag):
            varsFragmentFoundation = varsFragmentFoundation + " -var=\"systemName="+tags.get(tag) +"\""  
          if re.match("environmentName", tag):
            varsFragmentFoundation = varsFragmentFoundation + " -var=\"environmentName="+tags.get(tag) +"\""  
          if re.match("ownerName", tag):
            varsFragmentFoundation = varsFragmentFoundation + " -var=\"ownerName="+tags.get(tag) +"\""  
  if keySource == "keyFile":
    with open(yamlKeysFileAndPath) as f:  
      keypairs_dict = yaml.safe_load(f)
      for key, value in keypairs_dict.items():  
        print(key, " is: ", value)  
        if re.match("keyPairs", key):
          keyPairs = keypairs_dict.get(key)
          for keyPair in keyPairs:
            for keyPairItem in keyPair:
              if re.match("name", keyPairItem):
                if keyPairName == keyPair.get(keyPairItem):
                  publicKeyLine = "_public_access_key=\""+keyPair.get("_public_access_key")+"\"\n"
                  secretKeyLine = "_secret_access_key=\""+keyPair.get("_secret_access_key")+"\"\n"
  elif keySource == "keyVault":
    publicKeyLine = "_public_access_key=\""+pub+"\"\n"
    secretKeyLine = "_secret_access_key=\""+sec+"\"\n"
  else: 
    print("Invailid keySource value.  Add error handling here to fit your organization's policites.  ")
  if len(publicKeyLine)>2 and len(secretKeyLine)>2:
    print("About to open and write to: ", tfvarsFileAndPath)
    f = open(tfvarsFileAndPath, "w")
    f.write(publicKeyLine)
    f.write(secretKeyLine)
    f.close()
    print("Finished writing to: ", tfvarsFileAndPath)
    print("Contents of tfvarsFileAndPath are: ")
    with open(tfvarsFileAndPath, 'r') as fin:
      print(fin.read())
    varsFragmentFoundation = varsFragmentFoundation + " -var-file=\"" + tfvarsFileAndPath +"\""
  return varsFragmentFoundation

def getVarsFragmentVM(yamlFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, subnetId, sgId, keySource, pub, sec):  
  publicKeyLine = ""
  secretKeyLine = ""
  varsFragmentVM = ""  
  keyPairName = ''
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("networkFoundation", key):
        netFoundationItems = my_dict.get(key)
        for networkItem in netFoundationItems:
          if re.match("region", networkItem):
            varsFragmentVM = varsFragmentVM + " -var=\"aws_region="+netFoundationItems.get(networkItem) +"\""  
      if re.match("tags", key):
        tags = my_dict.get(key)
        for tag in tags:
          if re.match("systemName", tag):
            varsFragmentVM = varsFragmentVM + " -var=\"systemName="+tags.get(tag) +"\""  
          if re.match("environmentName", tag):
            varsFragmentVM = varsFragmentVM + " -var=\"environmentName="+tags.get(tag) +"\""  
          if re.match("ownerName", tag):
            varsFragmentVM = varsFragmentVM + " -var=\"ownerName="+tags.get(tag) +"\""  
      if re.match("standaloneVms", key):
        vms = my_dict.get(key)
        vmCounter = 0
        for vm in vms:
          print("vm is: ", vm)
          if vmCounter < 2:
            instanceName = vm.get("vmName")
            keyPairName = instanceName + 'KeyPair'
            varsFragmentVM = varsFragmentVM + " -var=\"vmName="+vm.get("vmName") +"\""  
            varsFragmentVM = varsFragmentVM + " -var=\"amiId="+vm.get("amiId") +"\""  
            vmCounter += 1
          else:
            print("You have exceeded the number of VMs allowed for this instance of this module.  Either create a separate instantiation of the module or consider creating a scaleset if you need more VMs.")
  if keySource == "keyFile":
    with open(yamlKeysFileAndPath) as f:  
      keypairs_dict = yaml.safe_load(f)
      for key, value in keypairs_dict.items():  
        print(key, " is: ", value)  
        if re.match("keyPairs", key):
          keyPairs = keypairs_dict.get(key)
          for keyPair in keyPairs:
            for keyPairItem in keyPair:
              if re.match("name", keyPairItem):
                if keyPairName == keyPair.get(keyPairItem):
                  publicKeyLine = "_public_access_key=\""+keyPair.get("_public_access_key")+"\"\n"
                  secretKeyLine = "_secret_access_key=\""+keyPair.get("_secret_access_key")+"\"\n"
  elif keySource == "keyVault":
    publicKeyLine = "_public_access_key=\""+pub+"\"\n"
    secretKeyLine = "_secret_access_key=\""+sec+"\"\n"
  else: 
    print("Invailid keySource value.  Add error handling here to fit your organization's policites.  ")
  if len(publicKeyLine)>2 and len(secretKeyLine)>2:
    print("About to open and write to: ", tfvarsFileAndPath)
    f = open(tfvarsFileAndPath, "w")
    f.write(publicKeyLine)
    f.write(secretKeyLine)
    f.close()
    print("Finished writing to: ", tfvarsFileAndPath)
    print("Contents of tfvarsFileAndPath are: ")
    with open(tfvarsFileAndPath, 'r') as fin:
      print(fin.read())
    varsFragmentVM = varsFragmentVM + " -var-file=\"" + tfvarsFileAndPath +"\""
  varsFragmentVM = varsFragmentVM + " -var=\"vpcId="+ vpcId +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"subnetId="+ subnetId +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"sgId="+ sgId +"\""
  return varsFragmentVM

def getVarsFragmentSecurityGroup(sgr, yamlFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, vpcCidr, sgId, sgName, keySource, pub, sec):  
  print("inside getVarsFragmentSecurityGroup(vpcId)")  
  varsFragmentSecurityGroup = ""  
  #print("1: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)  
  cidrBlocks = ''
  keyPairName = ''
  publicKeyLine = ''
  secretKeyLine = ''
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      #print(key, " is: ", value)  
      if re.match("networkFoundation", key):
        netFoundationItems = my_dict.get(key)
        for networkItem in netFoundationItems:
          if re.match("instanceName", networkItem):
            instanceName = netFoundationItems.get(networkItem)
            keyPairName = instanceName + 'KeyPair'
          if re.match("region", networkItem):
            varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"aws_region="+netFoundationItems.get(networkItem) +"\""  
      if re.match("tags", key):
        tags = my_dict.get(key)
        for tag in tags:
          if re.match("networkName", tag):
            varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcName="+tags.get(tag) +"\""  
      #/////
      if re.match("securityGroupRules", key):
        sgrs = my_dict.get(key)
        for sgRule in sgrs:
          print("sgRule is: ", sgRule)
          for ruleItem in sgRule:
            if re.match("ruleName", ruleItem):
              print("ruleName is: ", sgRule.get(ruleItem))
            if sgr == sgRule.get(ruleItem):
              print(sgr, " is the only rule for which we are populating config during this pass through the loop.  ")
              #/////
              with open(yamlFileAndPath) as f:  
                sgr_dict = yaml.safe_load(f)  
                for key, value in sgr_dict.items():  
                  print(key, " is: ", value)  
                  if re.match("securityGroupRules", key):
                    sgrs = sgr_dict.get(key)
                    print("sgrs is: ", sgrs)
                    newDict = next((item for item in sgrs if item["ruleName"] == sgr), None)
                    print("newDict is: ", newDict)
                    #/////
                    print("type is: ", newDict["type"])
                    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"ruleType="+newDict["type"] +"\""  
                    print("fromPort is: ", newDict["fromPort"])
                    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"fromPort="+str(newDict["fromPort"]) +"\""  
                    print("toPort is: ", newDict["toPort"])
                    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"toPort="+str(newDict["toPort"]) +"\""  
                    print("cidrBlocks is: ", newDict["cidrBlocks"])
                    import requests
                    if newDict["cidrBlocks"] == 'admin':
                      adminCidr1 = (requests.get('https://api.ipify.org').text).rstrip() + "/32"
                      #print('adminCidr1 is:', adminCidr1)
                      adminCidr2 =  (requests.get('http://ipv4.icanhazip.com').text).rstrip() + "/32"
                      #print('adminCidr2 is:', adminCidr2)
                      if adminCidr1 == adminCidr2:  
                        cidrBlocks = adminCidr1
                        print("The external IP of the agent was validated by two independent sources. ")
                      else:
                        print("The external IP of the agent could not be validated by two independent sources.  We are therefore NOT poppulating the cidrBlocks variable.  Check the logs to research what happened. ")
                    elif newDict["cidrBlocks"] == 'public':
                      cidrBlocks = '0.0.0.0/0'
                    else:
                      print("cidr block not valid.")
                    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"cidrBlocks="+cidrBlocks +"\""  
                    #/////
  if keySource == "keyFile":
    if len(keyPairName) > 2:
      with open(yamlKeysFileAndPath) as f:  
        keypairs_dict = yaml.safe_load(f)
        for key, value in keypairs_dict.items():  
          #print(key, " is: ", value)  
          if re.match("keyPairs", key):
            keyPairs = keypairs_dict.get(key)
            for keyPair in keyPairs:
              for keyPairItem in keyPair:
                if re.match("name", keyPairItem):
                  if keyPairName == keyPair.get(keyPairItem):
                    publicKeyLine = "_public_access_key=\""+keyPair.get("_public_access_key")+"\"\n"
                    secretKeyLine = "_secret_access_key=\""+keyPair.get("_secret_access_key")+"\"\n"
  elif keySource == "keyVault":
    publicKeyLine = "_public_access_key=\""+pub+"\"\n"
    secretKeyLine = "_secret_access_key=\""+sec+"\"\n"
  else: 
    print("Invailid keySource value.  Add error handling here to fit your organization's policites.  ")

  if len(publicKeyLine)>2 and len(secretKeyLine)>2:
    #print("About to open and write to: ", tfvarsFileAndPath)
    f = open(tfvarsFileAndPath, "w")
    f.write(publicKeyLine)
    f.write(secretKeyLine)
    f.close()
    #print("Finished writing to: ", tfvarsFileAndPath)
    #print("Contents of tfvarsFileAndPath are: ")
    #with open(tfvarsFileAndPath, 'r') as fin:
    #  print(fin.read())
    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var-file=\"" + tfvarsFileAndPath +"\""
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcId="+ vpcId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcCidr="+ vpcCidr +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgId="+ sgId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgName="+ sgName +"\""  
  #print("5: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)
  return varsFragmentSecurityGroup  
  
def getVarsFragmentBlobStorage(blobStorageInstance, yamlFileAndPath, yamlKeysFileAndPath, tfvarsFileAndPath, vpcId, keySource, pub, sec) :  
  varsFragmentBlobStorage = ""  
  keyPairName = ''
  publicKeyLine = ''
  secretKeyLine = ''
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      if re.match("networkFoundation", key):
        netFoundationItems = my_dict.get(key)
        for networkItem in netFoundationItems:
          if re.match("instanceName", networkItem):
            instanceName = netFoundationItems.get(networkItem)
            keyPairName = instanceName + 'KeyPair'
          if re.match("region", networkItem):
            varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"aws_region="+netFoundationItems.get(networkItem) +"\""  
      if re.match("tags", key):
        tags = my_dict.get(key)
        for tag in tags:
          if re.match("systemName", tag):
            varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"systemName="+tags.get(tag) +"\""  
          if re.match("environmentName", tag):
            varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"environmentName="+tags.get(tag) +"\""  
          if re.match("ownerName", tag):
            varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"ownerName="+tags.get(tag) +"\""  
  if keySource == "keyFile":
    if len(keyPairName) > 2:
      with open(yamlKeysFileAndPath) as f:  
        keypairs_dict = yaml.safe_load(f)
        for key, value in keypairs_dict.items():  
          if re.match("keyPairs", key):
            keyPairs = keypairs_dict.get(key)
            for keyPair in keyPairs:
              for keyPairItem in keyPair:
                if re.match("name", keyPairItem):
                  if keyPairName == keyPair.get(keyPairItem):
                    publicKeyLine = "_public_access_key=\""+keyPair.get("_public_access_key")+"\"\n"
                    secretKeyLine = "_secret_access_key=\""+keyPair.get("_secret_access_key")+"\"\n"
  elif keySource == "keyVault":
    publicKeyLine = "_public_access_key=\""+pub+"\"\n"
    secretKeyLine = "_secret_access_key=\""+sec+"\"\n"
  else: 
    print("Invailid keySource value.  Add error handling here to fit your organization's policites.  ")
  if len(publicKeyLine)>2 and len(secretKeyLine)>2:
    f = open(tfvarsFileAndPath, "w")
    f.write(publicKeyLine)
    f.write(secretKeyLine)
    f.close()
    varsFragmentBlobStorage = varsFragmentBlobStorage + " -var-file=\"" + tfvarsFileAndPath +"\""
  varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"s3BucketNameTF="+ blobStorageInstance +"\""  
  varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"dynamoDbTableNameTF="+ blobStorageInstance +"\""  
  varsFragmentBlobStorage = varsFragmentBlobStorage + " -var=\"vpcId="+ vpcId +"\""  
  return varsFragmentBlobStorage

def getVarsVMFromPipeline( aws_Region, aws_PublicAccessKey, aws_SecretAccessKey, vpc_Id, system_Name, environment_Name, owner_Name, vm_Name, ami_Id, subnet_Id, sg_Id ):
  varsFragmentVM = ""
  varsFragmentVM = varsFragmentVM + " -var=\"aws_region=" + aws_Region +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"_public_access_key=" + aws_PublicAccessKey +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"_secret_access_key=" + aws_SecretAccessKey +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"vpcId=" + vpc_Id +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"systemName=" + system_Name +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"environmentName=" + environment_Name +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"ownerName=" + owner_Name +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"vmName=" + vm_Name +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"amiId=" + ami_Id +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"subnetId=" + subnet_Id +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"sgId=" + sg_Id +"\""  
  return varsFragmentVM

def getVarsSGRFromPipeline(aws_Region, aws_PublicAccessKey, aws_SecretAccessKey, vpc_Name, vpc_Id, vpc_Cidr, sg_Id, sg_Name ):
  varsFragmentSGR = ""
  varsFragmentSGR = varsFragmentSGR +  " -var=\"aws_region=" + aws_Region +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"_public_access_key=" + aws_PublicAccessKey +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"_secret_access_key=" + aws_SecretAccessKey +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcName=" + vpc_Name +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcId=" + vpc_Id +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"vpcCidr=" + vpc_Cidr +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"sgId=" + sg_Id +"\""  
  varsFragmentSGR = varsFragmentSGR +  " -var=\"sgName=" + sg_Name +"\""  
  return varsFragmentSGR
<<<<<<< HEAD

def instantiateFoundationCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, keySource, demoStorageKey, **kw):
  ############################################################################
  ### Copy the foundation template into a new instance.  Modify for OS. 
  ############################################################################
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  if platform.system() == 'Windows':
    sourceOfFoundationCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\network-foundation\\"
    destinationFoundationCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\network-foundation\\"+foundationInstanceName+"-network-foundation\\"  
  else:
    sourceOfFoundationCallTemplate = pathToApplicationRoot + "calls-to-modules/templates/network-foundation/"
    destinationFoundationCallInstance = pathToApplicationRoot + "calls-to-modules/instances/network-foundation/"+foundationInstanceName+"-network-foundation/"  
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
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-network-foundation\""
    searchTerm = "\\modules\\"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  else: 
    searchTerm = "\\modules\\"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"../../../../modules/aws-simple-network-foundation\""
    searchTerm = "/modules/"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  #\\NOTE: Pipeline version of this will create and use a remote backend.  But here in the demo laptop version we are using a local backend to keep it simple.
  ##############################################################################################################################
  ### Initialize terraform from inside the network foundation directory.  Conditionally make backend remote if from pipeline
  ##############################################################################################################################
  if keySource == "keyVault":
    kw['keyFileTF']  =  foundationInstanceName + "-networkFoundation"
    createBackendConfigFileTerraform(destinationFoundationCallInstance, **kw) 
    print("About to refresh list contents of (DefaultWorkingDirectory)/_terraform-aws-starter-kit/drop/calls-to-modules/aws-simple-network-foundation-call-to-module/")	
    print(*Path(destinationFoundationCallInstance).iterdir(), sep="\n") 
    print("About to call terraform init:  ")	
    initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
  else:
    initCommand = 'terraform init '
  runTerraformCommand(initCommand, destinationFoundationCallInstance )	
  #Add error handling to validate that init command succeeded.
  return destinationFoundationCallInstance

def instantiateBlobStorageCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, blobStorageInstance, keySource, demoStorageKey, **kw):
  ############################################################################
  ### Copy the blob storsge template into a new instance.  Modify for OS. 
  ############################################################################
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  if platform.system() == 'Windows':
    sourceOfBlobStorageCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\s3-backend\\"
    destinationBlobStorageCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\s3-backends\\"+foundationInstanceName+"-"+blobStorageInstance+"-s3\\"  
  else:
    sourceOfBlobStorageCallTemplate = pathToApplicationRoot + "calls-to-modules/templates/s3-backend/"
    destinationBlobStorageCallInstance = pathToApplicationRoot + "calls-to-modules/instances/s3-backend/"+foundationInstanceName+"-"+blobStorageInstance+"-s3/"  
  #Create destination directory if it does not already exist 
  Path(destinationBlobStorageCallInstance).mkdir(parents=True, exist_ok=True)
  #Copy config and secret templates outside app path before they can be safely populated
  copy_tree(sourceOfBlobStorageCallTemplate, destinationBlobStorageCallInstance)
  #Modify main.tf so that it points to the correct module directory
  fileName = destinationBlobStorageCallInstance + "main.tf"
  #Isolating error by commenting the next block.
  if platform.system() == 'Windows':
    print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
    searchTerm = "/modules/"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-S3-backend\""
    searchTerm = "\\modules\\"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  else: 
    searchTerm = "\\modules\\"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"../../../../modules/aws-simple-S3-backend\""
    searchTerm = "/modules/"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  #\\NOTE: Pipeline version of this will create and use a remote backend.  But here in the demo laptop version we are using a local backend to keep it simple.
  ##############################################################################################################################
  ### Initialize terraform from inside the network foundation directory.  Conditionally make backend remote if from pipeline
  ##############################################################################################################################
  kw['keyFileTF']  =  foundationInstanceName + "-" + blobStorageInstance + "-s3"
  if keySource == "keyVault":
    createBackendConfigFileTerraform(destinationBlobStorageCallInstance, **kw) 
    print("About to refresh list contents of: ", destinationBlobStorageCallInstance)	
    print(*Path(destinationBlobStorageCallInstance).iterdir(), sep="\n") 
    print("About to call terraform init:  ")	
    initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
  else:
    initCommand = 'terraform init '
  runTerraformCommand(initCommand, destinationBlobStorageCallInstance )	
  #Add error handling to validate that init command succeeded.
  return destinationBlobStorageCallInstance

def instantiateStandaloneVirtualMachineCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, vmInstance, keySource, demoStorageKey, **kw):
  ############################################################################
  ### Copy the virtual machine call template into a new instance.  Modify for OS. 
  ############################################################################
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  if platform.system() == 'Windows':
    sourceOfVirtualMachineCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\vm\\"
    destinationVirtualMachineCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\vm\\"+foundationInstanceName+"-"+vmInstance+"-vm\\"  
  else:
    sourceOfVirtualMachineCallTemplate = pathToApplicationRoot + "calls-to-modules/templates/vm/"
    destinationVirtualMachineCallInstance = pathToApplicationRoot + "calls-to-modules/instances/vm/"+foundationInstanceName+"-"+vmInstance+"-vm/"  
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
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-vm\""
    searchTerm = "\\modules\\"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  else: 
    searchTerm = "\\modules\\"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"../../../../modules/aws-simple-vm\""
    searchTerm = "/modules/"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  #\\NOTE: Pipeline version of this will create and use a remote backend.  But here in the demo laptop version we are using a local backend to keep it simple.
  ##############################################################################################################################
  ### Initialize terraform from inside the network foundation directory.  Conditionally make backend remote if from pipeline
  ##############################################################################################################################
  kw['keyFileTF']  =  foundationInstanceName + "-" + vmInstance + "-vm"
  if keySource == "keyVault":
    createBackendConfigFileTerraform(destinationVirtualMachineCallInstance, **kw) 
    print("About to refresh list contents of: ", destinationVirtualMachineCallInstance)	
    print(*Path(destinationVirtualMachineCallInstance).iterdir(), sep="\n") 
    print("About to call terraform init:  ")	
    initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
  else:
    initCommand = 'terraform init '
  runTerraformCommand(initCommand, destinationVirtualMachineCallInstance )	
  #Add error handling to validate that init command succeeded.
  return destinationVirtualMachineCallInstance

def instantiateSecurityGroupRuleCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, sgr, keySource, demoStorageKey, **kw):
  ############################################################################
  ### Copy the virtual machine call template into a new instance.  Modify for OS. 
  ############################################################################
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  if platform.system() == 'Windows':
    sourceOfSecurityGroupRuleCallTemplate = pathToApplicationRoot + "\\calls-to-modules\\templates\\security-group-rules\\"
    destinationSecurityGroupRuleCallInstance = pathToApplicationRoot + "\\calls-to-modules\\instances\\security-group-rules\\"+foundationInstanceName+"-"+sgr+"-sgr\\"  
  else:
    sourceOfSecurityGroupRuleCallTemplate = pathToApplicationRoot + "calls-to-modules/templates/security-group-rules/"
    destinationSecurityGroupRuleCallInstance = pathToApplicationRoot + "/calls-to-modules/instances/security-group-rules/"+foundationInstanceName+"-"+sgr+"-sgr/"  
  #Create destination directory if it does not already exist 
  Path(destinationSecurityGroupRuleCallInstance).mkdir(parents=True, exist_ok=True)
  #Copy config and secret templates outside app path before they can be safely populated
  copy_tree(sourceOfSecurityGroupRuleCallTemplate, destinationSecurityGroupRuleCallInstance)
  #Modify main.tf so that it points to the correct module directory
  fileName = destinationSecurityGroupRuleCallInstance + "main.tf"
  if platform.system() == 'Windows':
    print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
    searchTerm = "/modules/"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-security-group-rules\""
    searchTerm = "\\modules\\"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  else: 
    searchTerm = "\\modules\\"
    deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
    newPointerLine="  source = \"../../../../modules/aws-simple-security-group-rules\""
    searchTerm = "/modules/"
    changePointerLineInCallToModule(fileName, searchTerm, newPointerLine)
  ##############################################################################################################################
  ### Initialize terraform from inside the network foundation directory.  Conditionally make backend remote if from pipeline
  ##############################################################################################################################
  kw['keyFileTF']  =  foundationInstanceName + "-" + sgr + "-sgr"
  if keySource == "keyVault":
    createBackendConfigFileTerraform(destinationSecurityGroupRuleCallInstance, **kw) 
    print("About to refresh list contents of: ", destinationSecurityGroupRuleCallInstance)	
    print(*Path(destinationSecurityGroupRuleCallInstance).iterdir(), sep="\n") 
    print("About to call terraform init:  ")	
    initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
  else:
    initCommand = 'terraform init '
  runTerraformCommand(initCommand, destinationSecurityGroupRuleCallInstance )	
  #Add error handling to validate that init command succeeded.
  return destinationSecurityGroupRuleCallInstance

def destroyInstanceOfCallToModule(locationOfCallInstance, parentDirOfCallInstance):
  #remove the instance of the call to the module, including its directory and any contents of that directory.  
  if os.path.exists(locationOfCallInstance) and os.path.isdir(locationOfCallInstance):
    #if not os.listdir(destinationVirtualMachineCallInstance):
    print("Directory is empty")
    path = Path(locationOfCallInstance)
    shutil.rmtree(path)
    #else:    
    #  print("Instance directory is not empty, so we will keep it for now:  ", destinationVirtualMachineCallInstance)
  else:
    print("Given Directory doesn't exist: ", locationOfCallInstance)
  #If parent is empty, delete parent directory also.  Otherwise, if parent directory is NOT empty, leave parent directory as-is.
  if os.path.exists(parentDirOfCallInstance) and os.path.isdir(parentDirOfCallInstance):
    if not os.listdir(parentDirOfCallInstance):
      print("Directory is empty")
      path = Path(parentDirOfCallInstance)
      shutil.rmtree(path)
    else:    
      print("Parent directory is not empty, so we will keep it for now: ", parentDirOfCallInstance)
  else:
    print("Given Directory doesn't exist: ", parentDirOfCallInstance)

=======
>>>>>>> ac0a3b861b45a7306429e91c3896cc8010db9031
