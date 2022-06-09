# availability zones in the region
data "aws_availability_zones" "azs" {}

# create a VPC (Virtual Private Cloud)
resource "aws_vpc" "vpc" {
  cidr_block            = var.vpc_cidr
  enable_dns_hostnames  = true
  enable_dns_support    = true

  tags = {
    Name = "flask-docker-vpc"
  }
}
