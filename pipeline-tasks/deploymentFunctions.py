import subprocess
import yaml
import re

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

vpc_id = ''  
vpc_cidr = ''  
subnet_id = ''  
sg_id = ''  
sg_name = ''  

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
      else:
        break

def getVarsFragmentFoundation(yamlFileAndPath):  
  varsFragmentFoundation = ""  
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("aws_region", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("vpcName", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("systemName", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("environmentName", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("ownerName", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_public_access_key", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_secret_access_key", key):  
        varsFragmentFoundation = varsFragmentFoundation + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
  return varsFragmentFoundation

def getVarsFragmentVM(yamlFileAndPath, vpcId, subnetId, sgId):  
  varsFragmentVM = ""  
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("aws_region", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("systemName", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("environmentName", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("ownerName", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_public_access_key", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_secret_access_key", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("vmName", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("amiId", key):  
        varsFragmentVM = varsFragmentVM + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"vpcId="+ vpcId +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"subnetId="+ subnetId +"\""  
  varsFragmentVM = varsFragmentVM + " -var=\"sgId="+ sgId +"\""
  return varsFragmentVM

def getVarsFragmentSecurityGroup(yamlFileAndPath, vpcId, vpcCidr, sgId, sgName):  
  print("inside getVarsFragmentSecurityGroup(vpcId)")  
  varsFragmentSecurityGroup = ""  
  print("1: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)  
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("aws_region", key):  
        varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
        print("2: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)  
      if re.match("_public_access_key", key):  
        varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
        print("3: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)  
      if re.match("_secret_access_key", key):  
        varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
        print("4: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)  
      if re.match("vpcName", key):  
        varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcId="+ vpcId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"vpcCidr="+ vpcCidr +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgId="+ sgId +"\""  
  varsFragmentSecurityGroup = varsFragmentSecurityGroup + " -var=\"sgName="+ sgName +"\""  
  print("5: varsFragmentSecurityGroup is: ", varsFragmentSecurityGroup)
  return varsFragmentSecurityGroup  
  
def getVarsFragmentS3Backend(yamlFileAndPath, vpcId):  
  varsFragmentS3Backend = ""  
  with open(yamlFileAndPath) as f:  
    my_dict = yaml.safe_load(f)  
    for key, value in my_dict.items():  
      print(key, " is: ", value)  
      if re.match("aws_region", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("systemName", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("environmentName", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("ownerName", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_public_access_key", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("_secret_access_key", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("s3BucketNameTF", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
      if re.match("dynamoDbTableNameTF", key):  
        varsFragmentS3Backend = varsFragmentS3Backend + " -var=\""+ key + "=" + my_dict.get(key) +"\""  
  varsFragmentS3Backend = varsFragmentS3Backend + " -var=\"vpcId="+ vpcId +"\""  
  return varsFragmentS3Backend
