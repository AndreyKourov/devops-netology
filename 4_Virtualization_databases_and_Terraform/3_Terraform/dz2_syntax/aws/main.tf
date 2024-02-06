
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Create a VPC
#resource "aws_vpc" "example" {
#  cidr_block = "10.0.0.0/16"
#}

resource "aws_instance" "app_server" {
  ami           = "ami-08d70e59c07c61a3a"
  instance_type = "t2.micro"
  tags = {
    Name = var.instance_name
  }
}

variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "ExampleAppServerInstance"
}

data "aws_caller_identity" "current" {}
data "aws_availability_zones" "current" {}
data "aws_regions" "current" {}