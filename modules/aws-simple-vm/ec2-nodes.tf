## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

data "aws_ami" "amazon-linux-2" {  
  most_recent = true
  
  owners = ["amazon"]
 
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
  
  filter {
    name   = "architecture"
    values = ["x86_64*"]
  }

}  

resource "aws_instance" "example-host" {
  ami                         = data.aws_ami.amazon-linux-2.id
  associate_public_ip_address = true
  instance_type               = "t2.micro"
  user_data_base64 = base64encode(local.example-host-userdata)
  source_dest_check           = false
  subnet_id = var.subnetId 
  vpc_security_group_ids = [var.sgId]

  timeouts {
    create = "60m"
    update = "60m"
    delete = "60m"
  }
  
  tags = { 
    Name = var.vmName
    System = var.systemName
    Environment = var.environmentName
    Owner = var.ownerName
  }

}
