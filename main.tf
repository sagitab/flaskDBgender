provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

variable "mysql_password" {
  description = "The MySQL root password"
  type        = string
  sensitive   = true
}

resource "random_id" "sg_suffix" {
  byte_length = 4
}

resource "aws_instance" "apache_server" {
  ami           = "ami-0453ec754f44f9a4a" # Replace with an Amazon Linux 2 AMI ID for your region
  instance_type = "t2.micro"              # Free tier eligible instance type

  key_name = "aws_cli_key"                   # Replace with your existing key pair name

  # Add a Security Group
  vpc_security_group_ids = [aws_security_group.flask_app_sg.id]

  # User Data Script to Install Apache
  user_data = <<-EOF
#!/bin/bash
sudo yum update -y
# Install libxcrypt-compat
sudo yum install -y libxcrypt-compat
sudo yum install -y docker
systemctl start docker
systemctl enable docker

curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo yum install git-all -y
git clone https://github.com/sagitab/flaskDBgender.git /home/ec2-user/flask-app
              
cd /home/ec2-user/flask-app
# Create .env file
cat <<EOT > .env
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=${var.mysql_password}
MYSQL_DB=mydb
PORT=5002
EOT
sudo docker-compose up -d
EOF

  tags = {
    Name = "Apache-Server"
  }
}

# Fetch the default VPC
data "aws_vpc" "default" {
  default = true
}

# Create the security group with a random suffix
resource "aws_security_group" "flask_app_sg" {
  name        = "flask-app-sg-tf-${random_id.sg_suffix.hex}"
  description = "Security group for Flask app"
  vpc_id      = data.aws_vpc.default.id

  # Allow HTTP traffic to the Flask application (port 5002)
  ingress {
    from_port   = 5002
    to_port     = 5002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow SSH traffic (port 22)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Output the Public IP
output "public_ip" {
  value       = aws_instance.apache_server.public_ip
  description = "Public IP of the Apache server"
}
