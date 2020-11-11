## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

#Note: Enable encryption of storage by uncommenting below.
#resource "aws_kms_key" "mykey" {
#  description             = "This key is used to encrypt bucket objects"
#  deletion_window_in_days = 10
#}


resource "aws_s3_bucket" "tf" {

  bucket = var.s3BucketNameTF
  #TOTALLY WRONG TO LEAVE THE acl AS public-read-write BUT WE ARE SETTING THE WRONG VALUE HERE DURING DEVELOPMENT.
  #acl    = "public-read-write"

  versioning {
    enabled = true
  }
  #Also add replication and encryption
}


resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.selected.id 
  service_name = "com.amazonaws.us-west-2.s3"
  
  tags = {  
    Environment = var.environmentName  
	System = var.systemName  
	Owner = var.ownerName  
  }  

}

resource "aws_dynamodb_table" "terraform-lock" {
    name           = var.dynamoDbTableNameTF
    read_capacity  = 5
    write_capacity = 5
    hash_key       = "LockID"
    attribute {
        name = "LockID"
        type = "S"
    }
    tags = {
        "Name" = "DynamoDB Terraform State Lock Table"
    }
}
