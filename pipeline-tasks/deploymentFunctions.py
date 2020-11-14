## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess
import yaml
import re
import fileinput 
import os 
import platform
from distutils.dir_util import copy_tree
from pathlib import Path
import shutil
import sys


ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

vpc_id = ''  
vpc_cidr = ''  
subnet_id = ''  
sg_id = ''  
sg_name = ''  
vm_ip_pub = ''
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
        if "public_ip_of_ec2_instance" in decodedline:
          print("Found public_ip_of_ec2_instance!")
          global vm_ip_pub
          vm_ip_pub=decodedline[28:].replace('"', '')
          print("public_ip_of_ec2_instance in deploymentFunctions.py is: ", vm_ip_pub)
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

def createBackendConfigFileTerraform(dir_to_use_net, **params): 
  resource_group_name = params.get('resGroupName')
  storage_account_name_terraform_backend = params.get('storageAccountNameTerraformBackend')
  storage_container_name = params.get('storContainerName')
  terra_key_file_name = params.get('keyFileTF')
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
  print("About to read the file we just wrote.") 
  f = open(tfFileNameAndPath, "r") 
  print(f.read())  

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
  cidrBlocks = ''
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
            varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"aws_region="+netFoundationItems.get(networkItem) +"\""  
      if re.match("tags", key):
        tags = my_dict.get(key)
        for tag in tags:
          if re.match("networkName", tag):
            varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcName="+tags.get(tag) +"\""  
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
                      adminCidr2 =  (requests.get('http://ipv4.icanhazip.com').text).rstrip() + "/32"
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
    varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var-file=\"" + tfvarsFileAndPath +"\""
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcId="+ vpcId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcCidr="+ vpcCidr +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgId="+ sgId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgName="+ sgName +"\""  
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

def convertPathForOS(pathToApplicationRoot, relativePath):
  print("platform.system() is: ", platform.system())
  if platform.system() == 'Windows':
    if '/' in relativePath:
      relativePath = relativePath.replace("/", "\\\\")
    destinationCallParent = pathToApplicationRoot + relativePath
  else:
    if '\\' in relativePath:
      relativePath = relativePath.replace('\\', '/')
    destinationCallParent = pathToApplicationRoot + relativePath
  return destinationCallParent

def createCallDirectoryAndFile(sourceOfCallTemplate, destinationCallInstance, newPointerLineWindows, newPointerLineLinux):
    Path(destinationCallInstance).mkdir(parents=True, exist_ok=True)
    copy_tree(sourceOfCallTemplate, destinationCallInstance)
    fileName = destinationCallInstance + "main.tf"
    if platform.system() == 'Windows':
      print("Confirmed this is Windows.  Gonna remove linux syntax by removing line that includes /modules/ ")
      searchTerm = "/modules/"
      deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
      searchTerm = "\\modules\\"
      changePointerLineInCallToModule(fileName, searchTerm, newPointerLineWindows)
    else: 
      searchTerm = "\\modules\\"
      deleteWrongOSPointerLineInCallToNodule(fileName, searchTerm)
      searchTerm = "/modules/"
      changePointerLineInCallToModule(fileName, searchTerm, newPointerLineLinux)

def initializeTerraformBackend(keySource, keyFile, destinationCallInstance, demoStorageKey, **kw):
  if keySource == "keyVault":
    kw['keyFileTF']  =  keyFile 
    createBackendConfigFileTerraform(destinationCallInstance, **kw) 
    initCommand="terraform init -backend=true -backend-config=\"access_key="+demoStorageKey+"\""  	
  else:
    initCommand = 'terraform init '
  runTerraformCommand(initCommand, destinationCallInstance )	
  #Add error handling to validate that init command succeeded.


def instantiateFoundationCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, keySource, demoStorageKey, **kw):
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  relativePathTemplate = "\\calls-to-modules\\templates\\network-foundation\\"
  relativePathInstance = "\\calls-to-modules\\instances\\network-foundation\\"+foundationInstanceName+"-network-foundation\\"  
  sourceOfFoundationCallTemplate = convertPathForOS(pathToApplicationRoot, relativePathTemplate)
  destinationFoundationCallInstance = convertPathForOS(pathToApplicationRoot, relativePathInstance)
  p = Path(destinationFoundationCallInstance)
  if p.exists():
    print("The instance of the call to module already exists.  Make sure to run destroyFoundation.py to destroy the directory structure of all instances of calls to modules before you send this back to version control.")
  else:
    newPointerLineWindows="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-network-foundation\""
    newPointerLineLinux="  source = \"../../../../modules/aws-simple-network-foundation\""
    createCallDirectoryAndFile(sourceOfFoundationCallTemplate, destinationFoundationCallInstance, newPointerLineWindows, newPointerLineLinux)
  keyFile = foundationInstanceName + "-networkFoundation"
  initializeTerraformBackend(keySource, keyFile, destinationFoundationCallInstance, demoStorageKey, **kw)
  return destinationFoundationCallInstance

def instantiateBlobStorageCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, blobStorageInstance, keySource, demoStorageKey, **kw):
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  relativePathTemplate = "\\calls-to-modules\\templates\\s3-backend\\"
  relativePathInstance = "\\calls-to-modules\\instances\\s3-backends\\"+foundationInstanceName+"-"+blobStorageInstance+"-s3\\" 
  sourceOfBlobStorageCallTemplate = convertPathForOS(pathToApplicationRoot, relativePathTemplate)
  destinationBlobStorageCallInstance = convertPathForOS(pathToApplicationRoot, relativePathInstance)
  p = Path(destinationBlobStorageCallInstance)
  if p.exists():
    print("The instance of the call to module already exists.  Make sure to run destroyFoundation.py to destroy the directory structure of all instances of calls to modules before you send this back to version control.")
  else:
    newPointerLineWindows="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-S3-backend\""
    newPointerLineLinux="  source = \"../../../../modules/aws-simple-S3-backend\""
    createCallDirectoryAndFile(sourceOfBlobStorageCallTemplate, destinationBlobStorageCallInstance, newPointerLineWindows, newPointerLineLinux)
  keyFile = foundationInstanceName + "-" + blobStorageInstance + "-s3" 
  initializeTerraformBackend(keySource, keyFile, destinationBlobStorageCallInstance, demoStorageKey, **kw)
  return destinationBlobStorageCallInstance

def instantiateStandaloneVirtualMachineCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, vmInstance, keySource, demoStorageKey, **kw):
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  relativePathTemplate = "\\calls-to-modules\\templates\\vm\\"
  relativePathInstance = "\\calls-to-modules\\instances\\vm\\"+foundationInstanceName+"-"+vmInstance+"-vm\\"  
  sourceOfVirtualMachineCallTemplate = convertPathForOS(pathToApplicationRoot, relativePathTemplate)
  destinationVirtualMachineCallInstance = convertPathForOS(pathToApplicationRoot, relativePathInstance)
  p = Path(destinationVirtualMachineCallInstance)
  if p.exists():
    print("The instance of the call to module already exists.  Make sure to run destroyFoundation.py to destroy the directory structure of all instances of calls to modules before you send this back to version control.")
  else:
    newPointerLineWindows="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-vm\""
    newPointerLineLinux="  source = \"../../../../modules/aws-simple-vm\""
    createCallDirectoryAndFile(sourceOfVirtualMachineCallTemplate, destinationVirtualMachineCallInstance, newPointerLineWindows, newPointerLineLinux)
  keyFile = foundationInstanceName + "-" + vmInstance + "-vm" 
  initializeTerraformBackend(keySource, keyFile, destinationVirtualMachineCallInstance, demoStorageKey, **kw)
  return destinationVirtualMachineCallInstance

def instantiateSecurityGroupRuleCallInstance(pathToApplicationRoot, yamlConfigFileAndPath, sgr, keySource, demoStorageKey, **kw):
  foundationInstanceName = getFoundationInstanceName(yamlConfigFileAndPath)
  relativePathTemplate = "\\calls-to-modules\\templates\\security-group-rules\\"
  relativePathInstance = "\\calls-to-modules\\instances\\security-group-rules\\"+foundationInstanceName+"-"+sgr+"-sgr\\"  
  sourceOfSecurityGroupRuleCallTemplate = convertPathForOS(pathToApplicationRoot, relativePathTemplate)
  destinationSecurityGroupRuleCallInstance = convertPathForOS(pathToApplicationRoot, relativePathInstance)
  p = Path(destinationSecurityGroupRuleCallInstance)
  if p.exists():
    print("The instance of the call to module already exists.  Make sure to run destroyFoundation.py to destroy the directory structure of all instances of calls to modules before you send this back to version control.")
  else:
    newPointerLineWindows="  source = \"..\\\..\\\..\\\..\\\modules\\\\aws-simple-security-group-rules\""
    newPointerLineLinux="  source = \"../../../../modules/aws-simple-security-group-rules\""
    createCallDirectoryAndFile(sourceOfSecurityGroupRuleCallTemplate, destinationSecurityGroupRuleCallInstance, newPointerLineWindows, newPointerLineLinux)
  keyFile = foundationInstanceName + "-" + sgr + "-sgr"
  initializeTerraformBackend(keySource, keyFile, destinationSecurityGroupRuleCallInstance, demoStorageKey, **kw)
  return destinationSecurityGroupRuleCallInstance

def destroyInstanceOfCallToModule(locationOfCallInstance, parentDirOfCallInstance):
  if os.path.exists(locationOfCallInstance) and os.path.isdir(locationOfCallInstance):
    print("Directory is empty")
    path = Path(locationOfCallInstance)
    shutil.rmtree(path)
  else:
    print("Given Directory doesn't exist: ", locationOfCallInstance)
  if os.path.exists(parentDirOfCallInstance) and os.path.isdir(parentDirOfCallInstance):
    if not os.listdir(parentDirOfCallInstance):
      print("Directory is empty")
      path = Path(parentDirOfCallInstance)
      shutil.rmtree(path)
    else:    
      print("Parent directory is not empty, so we will keep it for now: ", parentDirOfCallInstance)
  else:
    print("Given Directory doesn't exist: ", parentDirOfCallInstance)
