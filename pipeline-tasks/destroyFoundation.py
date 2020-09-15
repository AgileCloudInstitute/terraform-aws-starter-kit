## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import deploymentFunctions as depfunc
import re

dirOfYamlFile = "C:\\projects\\terraform\\tfvars\\terraform-aws-simple-example\\"
nameOfYamlFile = 'varsFromDevLaptop.yaml'
yamlFileAndPath = dirOfYamlFile + nameOfYamlFile
pathToApplicationRoot = "C:\\projects\\terraform\\sandbox\\terraform-aws-simple-example\\"
dirToUseNet = pathToApplicationRoot + 'calls-to-modules\\aws-simple-network-foundation-call-to-module'  
dirToUseVM = pathToApplicationRoot + "calls-to-modules\\aws-simple-vm-call-to-module\\"
dirToUseSG = pathToApplicationRoot + "calls-to-modules\\aws-simple-security-group-rules-call-to-module\\"
dirToUseS3Backend = pathToApplicationRoot + "calls-to-modules\\aws-simple-s3-backend-call-to-module\\"
initCommand = 'terraform init '

################################################################################
### Destroy the S3 Backend 
################################################################################
#Get some input vars from output from the network foundation module.  
depfunc.runTerraformCommand('terraform output', dirToUseNet)
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
varsFragmentS3Backend = depfunc.getVarsFragmentS3Backend(yamlFileAndPath, depfunc.vpc_id)
print("varsFragmentS3Backend is: ", varsFragmentS3Backend)
destroyCommandS3Backend = "terraform destroy -auto-approve" + varsFragmentS3Backend
print("destroyCommandS3Backend is: ", destroyCommandS3Backend)
depfunc.runTerraformCommand(initCommand, dirToUseS3Backend)
depfunc.runTerraformCommand(destroyCommandS3Backend, dirToUseS3Backend)

#############################################################################
### Destroy the security group rule
#############################################################################
#Get some input vars from output from the network foundation module.  
depfunc.runTerraformCommand('terraform output', dirToUseNet)
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
print("depfunc.vpc_cidr is: ", depfunc.vpc_cidr)
print("depfunc.sg_id is: ", depfunc.sg_id)
print("depfunc.sg_name is: ", depfunc.sg_name)
varsFragmentSG = depfunc.getVarsFragmentSecurityGroup(yamlFileAndPath, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name)  
print("varsFragmentSG is: ", varsFragmentSG)
destroyCommandSG = "terraform destroy -auto-approve" + varsFragmentSG
print("destroyCommandSG is: ", destroyCommandSG)
depfunc.runTerraformCommand(initCommand, dirToUseSG)
depfunc.runTerraformCommand(destroyCommandSG, dirToUseSG)

###############################################################################
### Destroy the virtual machine
###############################################################################
#Get some input vars from output from the network foundation module.  
depfunc.runTerraformCommand('terraform output', dirToUseNet)
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
print("depfunc.subnet_id is: ", depfunc.subnet_id) 
print("depfunc.sg_id is: ", depfunc.sg_id)
varsFragmentCompute = depfunc.getVarsFragmentVM(yamlFileAndPath, depfunc.vpc_id, depfunc.subnet_id, depfunc.sg_id)  
print("varsFragmentCompute for VM is: ", varsFragmentCompute)
destroyCommandCompute = "terraform destroy -auto-approve" + varsFragmentCompute
print("destroyCommandCompute is: ", destroyCommandCompute)
depfunc.runTerraformCommand(initCommand, dirToUseVM)
depfunc.runTerraformCommand(destroyCommandCompute, dirToUseVM)  

###############################################################################
### Destroy the foundation 
###############################################################################
varsFragmentNet = depfunc.getVarsFragmentFoundation(yamlFileAndPath)
print("varsFragmentNet is: ", varsFragmentNet)  
destroyCommandNet = "terraform destroy -auto-approve" + varsFragmentNet
print("destroyCommandNet is: ", destroyCommandNet)
depfunc.runTerraformCommand(initCommand, dirToUseNet)
depfunc.runTerraformCommand(destroyCommandNet, dirToUseNet)
