#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

# Update system and install prerequisites
echo "Updating system and installing prerequisites..."
yum update -y
yum install -y yum-utils device-mapper-persistent-data lvm2

# Enable and install Docker from Amazon Linux Extras
echo "Enabling and installing Docker..."
amazon-linux-extras enable docker
yum install -y docker

# Start and enable Docker service
echo "Starting and enabling Docker service..."
systemctl start docker
systemctl enable docker

# Add ec2-user to the docker group
echo "Adding 'ec2-user' to the Docker group..."
usermod -aG docker ec2-user

# Verify Docker installation
echo "Verifying Docker installation..."
docker --version
if [ $? -eq 0 ]; then
    echo "Docker has been successfully installed."
else
    echo "Failed to install Docker."
    exit 1
fi

# Install Docker Compose
echo "Installing Docker Compose..."
DOCKER_COMPOSE_VERSION="v2.26.0"
curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verify Docker Compose installation
docker-compose --version
if [ $? -eq 0 ]; then
    echo "Docker Compose has been successfully installed."
else
    echo "Failed to install Docker Compose."
    exit 1
fi

# Ensure required files are available
echo "Ensuring docker-compose.yml, init.sql, and .env are present..."
REQUIRED_FILES=(
    "/home/ec2-user/docker-compose.yml"
    "/home/ec2-user/db-scripts/init.sql"
    "/home/ec2-user/.env"
)
for FILE in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo "Required file $FILE not found. Please upload it and re-run this script."
        exit 1
    fi
done

# Run Docker Compose
echo "Starting application with Docker Compose..."
cd /home/ec2-user
docker-compose up -d

echo "Setup complete!"
