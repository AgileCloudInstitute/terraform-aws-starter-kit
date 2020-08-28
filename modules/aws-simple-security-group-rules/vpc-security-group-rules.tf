## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# Security group and rule to allow the node to communicate with the outside world.  

data "aws_security_group" "example-hosts" {
  id = var.sgId
  vpc_id = data.aws_vpc.example-vpc.id  
  name = var.sgName
}

resource "aws_security_group_rule" "example-admin-ssh" {
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks       = ["${local.admin-external-cidr}"]
  security_group_id        = data.aws_security_group.example-hosts.id
}
