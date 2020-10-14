# terraform-aws-starter-kit
Working example of creating basic aws instrustructure including EC2 VM in VPC  
    
##  This repo can either be:  
A.  consumed into a pipeline system as we will do with some of our examples  
B.  or cloned manually as a simple hands-on experience of using Terraform with AWS  
  
#  To use this manually:  
1.  Clone onto a machine on which Terraform has already been installed.  
2.  Run [pipeline-tasks/setup.py](https://github.com/AgileCloudInstitute/terraform-aws-starter-kit/blob/master/pipeline-tasks/setup.py) to copy the contents of the `Move-This-Directory-Outside-Of-Application-Path` directory to a different location so that any sensitive information like keys that you will put into it will NOT be transported around with the application code.    
3.  In the `vars/yamlInputs/varsFromDevLaptop.yaml` file, place the values for input variables that you will be using to instantiate this example.    
4.  Then in the `vars/yamlInputs/keys.yaml` file, make sure that the `name` property of a key pair record is a combination of a name of a foundationInstance and the term KeyPair as shown in the example given `demoKeyPair` which combines a reference of the foundation instance named `demo` and the term KeyPair.  This naming convension is essential in order for automation in the rest of this starter kit to work.  (Note that pibeline key managemne will be done with a secrets vault, so that this example with `keys.yaml` is just for demonstration.)      
5.  Open a terminal and navigate to the root directory into which you cloned this repository, then continue navigating to the `pipeline-tasks` subdirectory.  
6.  Type `python3 createFoundation.py` to create infrastructure on AWS using this example.    
7.  Note the IP address that is printed in the console as an output variable.  You may have to scroll up for this.  
8.  If on windows, open a Putty instance.  Putty to the IP address of the newly created EC2 instance, which was given as an output variable.  Then login with the username and password that you put in the `userdata.tf` file.  
9.  If on Linux, `ssh` to the IP address of the instance using the username you specified in the USERDATA.  
10.  Change your password immediately upon logging in by typing the commands given below.  Write down your replacement password somewhere safe so that you remember it.  Again note that putting a password in USERDATA is bad practice.  We are only doing it here to keep this example very simple.  
    
        $ passwd  
        Changing password for user agile-cloud.  
        Changing password for agile-cloud.  
        (current) UNIX password:  
        New password:  
        Retype new password:  
        passwd: all authentication tokens updated successfully.  
        $  
      
#  Destroy the infrastructure you created above in order to avoid paying for what you do not use:  
1.  Return to the console window in which you typed the `python3 createFoundation.py` command above.  Make sure it is pointed to the same directory in which you ran the `python3 createFoundation.py` command.  
2.  Type `python3 destroyFoundation.py` to destroy the infrastructure and read the console output to confirm that everything was actually destroyed as intended.        
  
