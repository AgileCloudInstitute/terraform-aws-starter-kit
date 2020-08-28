import deploymentFunctions as depfunc
import re

pathToApplicationRoot = 'C:\\projects\\terraform\\sandbox\\terraform-aws-simple-example\\'  
dirOfYamlFile = "C:\\projects\\terraform\\tfvars\\terraform-aws-simple-example\\"
nameOfYamlFile = 'varsFromDevLaptop.yaml'
yamlFileAndPath = dirOfYamlFile + nameOfYamlFile

#############################################################################
### Create the network foundation
#############################################################################
varsFragmentNet = depfunc.getVarsFragmentFoundation(yamlFileAndPath)
print("varsFragmentNet is: ", varsFragmentNet)  
applyCommandNet = "terraform apply -auto-approve" + varsFragmentNet
print("applyCommandNet is: ", applyCommandNet)
dirToUseNet = pathToApplicationRoot + 'calls-to-modules\\aws-simple-network-foundation-call-to-module'  
commandToRun = 'dir'  
initCommand = 'terraform init '
depfunc.runTerraformCommand(initCommand, dirToUseNet)
depfunc.runTerraformCommand(applyCommandNet, dirToUseNet)
  
##############################################################################
### Create Virtual Machine and attach to the foundation
##############################################################################
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
print("depfunc.subnet_id is: ", depfunc.subnet_id) 
print("depfunc.sg_id is: ", depfunc.sg_id)
varsFragmentCompute = depfunc.getVarsFragmentVM(yamlFileAndPath, depfunc.vpc_id, depfunc.subnet_id, depfunc.sg_id)  
print("varsFragmentCompute for VM is: ", varsFragmentCompute)
applyCommandCompute = "terraform apply -auto-approve" + varsFragmentCompute
print("applyCommandCompute is: ", applyCommandCompute)
dirToUseVM = pathToApplicationRoot + "calls-to-modules\\aws-simple-vm-call-to-module\\"
depfunc.runTerraformCommand(initCommand, dirToUseVM)
depfunc.runTerraformCommand(applyCommandCompute, dirToUseVM)  
  
###############################################################################
### Create Security Group and attach to the foundation and VM.  
###############################################################################
#Get some input vars from output from the network foundation module.  
depfunc.runTerraformCommand('terraform output', dirToUseNet)
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
print("depfunc.vpc_cidr is: ", depfunc.vpc_cidr)
print("depfunc.sg_id is: ", depfunc.sg_id)
print("depfunc.sg_name is: ", depfunc.sg_name)
varsFragmentSG = depfunc.getVarsFragmentSecurityGroup(yamlFileAndPath, depfunc.vpc_id, depfunc.vpc_cidr, depfunc.sg_id, depfunc.sg_name)  
print("varsFragmentSG is: ", varsFragmentSG)
applyCommandSG = "terraform apply -auto-approve" + varsFragmentSG
print("applyCommandSG is: ", applyCommandSG)
dirToUseSG = pathToApplicationRoot + "calls-to-modules\\aws-simple-security-group-rules-call-to-module\\"
depfunc.runTerraformCommand(initCommand, dirToUseSG)
depfunc.runTerraformCommand(applyCommandSG, dirToUseSG)

################################################################################
### Create S3 Backend and attach to the foundation
################################################################################
#Get some input vars from output from the network foundation module.  
depfunc.runTerraformCommand('terraform output', dirToUseNet)
print("depfunc.vpc_id is: ", depfunc.vpc_id) 
varsFragmentS3Backend = depfunc.getVarsFragmentS3Backend(yamlFileAndPath, depfunc.vpc_id)
print("varsFragmentS3Backend is: ", varsFragmentS3Backend)
applyCommandS3Backend = "terraform apply -auto-approve" + varsFragmentS3Backend
print("applyCommandS3Backend is: ", applyCommandS3Backend)
dirToUseS3Backend = pathToApplicationRoot + "calls-to-modules\\aws-simple-s3-backend-call-to-module\\"
depfunc.runTerraformCommand(initCommand, dirToUseS3Backend)
depfunc.runTerraformCommand(applyCommandS3Backend, dirToUseS3Backend)
