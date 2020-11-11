import os
import shutil
import deploymentFunctions as depfunc

print("Inside undoSetup.py")

app_parent_path = os.path.dirname(os.path.realpath("..\\"))
print("app_parent_path is: ", app_parent_path)
dest_path = app_parent_path+"\\config-and-secrets-outside-app-path\\"
print("dest_path is: ", dest_path)


try:
  shutil.rmtree(dest_path, ignore_errors=True)
except FileNotFoundError:
  print("The config-and-secrets-outside-app-path directory does not exist.  It may have already been deleted.")

print("Contents of app parent directory are: ")
depfunc.runShellCommandInWorkingDir("dir", app_parent_path)
