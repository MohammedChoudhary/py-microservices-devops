variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "key_pair_name" {
  description = "Name of AWS key pair for SSH access"
  type        = string
  default     = "devops-assignment-key"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "devops-microservices"
}

variable "dockerhub_username" {
  description = "DockerHub username for pulling images"
  type        = string
  default     = "mohxmd77"
}