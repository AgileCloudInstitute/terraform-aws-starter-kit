## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "aws-simple-vm" {
  source = "../../modules/aws-simple-vm"
  #source = "..\\..\\modules\\aws-simple-vm"

  _region = "${var.aws_region}"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  vpcId = "${var.vpcId}"
  systemName = "${var.systemName}"
  environmentName = "${var.environmentName}"
  ownerName = "${var.ownerName}"
  vmName = "${var.vmName}"
  amiId = "${var.amiId}"
  subnetId = "${var.subnetId}"
  sgId = "${var.sgId}"  

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcId" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }
variable "vmName" { }
variable "amiId" { }  
variable "subnetId" { }  
variable "sgId" { }

##Output variables
output "public_ip_of_ec2_instance" { value = "${module.aws-simple-vm.public_ip_of_ec2_instance}" }
output "ami_id" { value = "${module.aws-simple-vm.ami_id}" }
