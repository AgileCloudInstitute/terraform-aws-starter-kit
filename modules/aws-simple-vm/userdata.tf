## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    
  
####################################################  
# Below we create the USERDATA to get the instance ready to run.
# The Terraform local simplifies Base64 encoding.  
locals {

  example-host-userdata = <<USERDATA
#!/bin/bash -xe

#SECURITY HOLE: Just for easy demonstration, the following enables password login and creates an agile-cloud with a password exposed in version control. 
#Replace the following 4 lines with something more secure when you establish a secrets management system.
/usr/sbin/useradd agile-cloud
echo agile-cloud:just-for-demo123 | chpasswd
echo 'agile-cloud ALL=(ALL:ALL) ALL' | sudo EDITOR='tee -a' visudo
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd

mkdir /home/agile-cloud/cloned-repos
mkdir /home/agile-cloud/vars
mkdir /home/agile-cloud/staging

chown -R agile-cloud:agile-cloud /home/agile-cloud/vars
chown -R agile-cloud:agile-cloud /home/agile-cloud/cloned-repos
chown -R agile-cloud:agile-cloud /home/agile-cloud/staging

### Install software
yum -y update
sudo yum install git -y

echo "About to install python3"
sudo yum install -y python3
sudo yum install -y python3-setuptools
sudo easy_install-3.7 pip

##Put any other startup commands you want to put here.
##Remember there are other approaches such as configuration tools like Ansible, Chef, Puppet, etc.

USERDATA

}