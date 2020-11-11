## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "aws-simple-network-foundation" {
  #source = "../../modules/aws-simple-network-foundation"
  source = "..\\..\\modules\\aws-simple-network-foundation"

  _region = "${var.aws_region}"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  vpcName = "${var.vpcName}"
  systemName = "${var.systemName}"
  environmentName = "${var.environmentName}"
  ownerName = "${var.ownerName}"

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcName" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }

##Output variables
output "vpc_id" { value = "${module.aws-simple-network-foundation.vpc_id}" }
output "vpc_cidr" { value = "${module.aws-simple-network-foundation.vpc_cidr}" }
output "subnet_id" { value = "${module.aws-simple-network-foundation.subnet_id}" }
output "sg_id" { value = "${module.aws-simple-network-foundation.sg_id}" }
output "sg_name" { value = "${module.aws-simple-network-foundation.sg_name}" }