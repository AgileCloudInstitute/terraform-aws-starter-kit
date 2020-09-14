import subprocess
import re
import os
import sys

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')	

print("Hello from inside setEnvironmentVarsFromPipeline.py ")  	

def runShellCommand(commandToRun):
    print("Inside runShellCommand(..., ...) function. ")
    print("commandToRun is: " +commandToRun)

    proc = subprocess.Popen( commandToRun,cwd=None, stdout=subprocess.PIPE, shell=True)
    while True:
      line = proc.stdout.readline()
      if line:
        thetext=line.decode('utf-8').rstrip('\r|\n')
        decodedline=ansi_escape.sub('', thetext)
        print(decodedline)
      else:
        break

demoStorageKey=sys.argv[1]

exportString = 'export ARM_ACCESS_KEY=' +demoStorageKey +"\n"
with open(os.path.expanduser("/home/azureuser/.bashrc"), "a") as outfile:
    # 'a' stands for "append"  
    outfile.write(exportString)
#"export MYVAR=MYVALUE"
print("About to read the /home/azureuser/.bashrc file we just wrote to.")	
#open and read the file after the appending: 
f = open("/home/azureuser/.bashrc", "r") 
print(f.read()) 

print("about to whoami: ")
runShellCommand("whoami")
 
print("about to echo ARM_ACCESS_KEY : ")
runShellCommand("echo $ARM_ACCESS_KEY")
#print(os.environ)
#print("ARM_ACCESS_KEY environment variable is: ", os.environ['ARM_ACCESS_KEY'])
print("Python version is: ", sys.version_info[0])  	
