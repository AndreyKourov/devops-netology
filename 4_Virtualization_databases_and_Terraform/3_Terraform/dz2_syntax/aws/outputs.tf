output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "AZ_names" {
  value = data.aws_availability_zones.current.names
}

output "subnet_id" {
  value       = aws_instance.app_server.subnet_id
}