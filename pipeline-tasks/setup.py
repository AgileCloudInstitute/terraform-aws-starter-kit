import os
import deploymentFunctions as depfunc
from distutils.dir_util import copy_tree
from pathlib import Path

print("Inside setup.py")

app_parent_path = os.path.dirname(os.path.realpath("..\\"))
print("app_parent_path is: ", app_parent_path)
from_path = app_parent_path+"\\terraform-aws-starter-kit"+"\\"+"Move-This-Directory-Outside-Of-Application-Path\\"
print("from_path is: ", from_path)
dest_path = app_parent_path+"\\config-and-secrets-outside-app-path\\"
print("dest_path is: ", dest_path)


#Create destination directory if it does not already exist 
Path(dest_path).mkdir(parents=True, exist_ok=True)
#Copy config and secret templates outside app path before they can be safely populated
copy_tree(from_path, dest_path)
print("Contents of app parent directory are: ")
depfunc.runShellCommandInWorkingDir("dir", app_parent_path)
