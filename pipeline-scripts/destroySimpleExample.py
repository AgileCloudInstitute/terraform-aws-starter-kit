print("Hello from inside destroySimpleExample.py ")

import sys  
    
awsPublicAccessKey=sys.argv[1] 
awsSecretAccessKey=sys.argv[2] 
storageAccountNameTerraformBackend=sys.argv[3] 
terraBackendKey=sys.argv[4] 
awsRegion=sys.argv[5] 
DefaultWorkingDirectory=sys.argv[6] 

print("awsPublicAccessKey is: ", awsPublicAccessKey)
print("awsSecretAccessKey is: ", awsSecretAccessKey)
print("storageAccountNameTerraformBackend is: ", storageAccountNameTerraformBackend)
print("terraBackendKey is: ", terraBackendKey)
print("awsRegion is: ", awsRegion)
print("DefaultWorkingDirectory is: ", DefaultWorkingDirectory)

print("Python version is: ", sys.version_info[0])  

