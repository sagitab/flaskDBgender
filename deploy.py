import boto3
import os
import time
import subprocess

def stop_ec2(public_ip, private_key_path, instance_id):
    # Command to stop the EC2 instance using AWS CLI
    ssh_command = [
        "ssh",
        "-i", private_key_path,
        "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
        f"ec2-user@{public_ip}",
        f"aws ec2 stop-instances --instance-ids {instance_id} --output text"
    ]

    print(f"Stopping EC2 instance with ID: {instance_id}...")

    # Execute the command
    result = subprocess.run(ssh_command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"EC2 instance {instance_id} stopped successfully.")
    else:
        print(f"Failed to stop EC2 instance. Error:\n{result.stderr}")


def delete_file_on_ec2(public_ip, private_key_path, file_path):
    # Command to delete the file on EC2
    ssh_command = [
        "ssh",
        "-i", private_key_path,
        "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
        f"ec2-user@{public_ip}",
        f"rm -f {file_path}"  # Remove the file if it exists
    ]

    print(f"Deleting file {file_path} on EC2...")

    # Execute the command
    result = subprocess.run(ssh_command, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"Failed to delete file. Error:\n{result.stderr}")


def run_script_on_ec2(public_ip, private_key_path):
    # Command to run as root using sudo
    ssh_command = [
        "ssh",
        "-i", private_key_path,
        f"ec2-user@{public_ip}",
        "sudo bash -c 'chmod +x /home/ec2-user/setup.sh && /home/ec2-user/setup.sh'"
    ]
    print("Running setup script on EC2 as root...")

    # Run the command via subprocess
    result = subprocess.run(ssh_command, capture_output=True, text=True)

    # Check if the command ran successfully
    if result.returncode == 0:
        print(f"Setup script executed successfully:\n{result.stdout}")
    else:
        print(f"Failed to execute script. Error:\n{result.stderr}")


def file_exists_on_ec2(public_ip, private_key_path, filename):
    # Check if file exists on the EC2 instance
    check_command = [
        "ssh",
        "-i", private_key_path,
        "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
        f"ec2-user@{public_ip}",
        f"test -f /home/ec2-user/{filename} && echo 'exists' || echo 'not exists'"
    ]
    result = subprocess.run(check_command, capture_output=True, text=True)
    return 'exists' in result.stdout


def create_directory_on_ec2(public_ip, private_key_path, directory):
    # Create directory on EC2 if it doesn't already exist
    check_directory_command = [
        "ssh",
        "-i", private_key_path,
        "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
        f"ec2-user@{public_ip}",
        f"mkdir -p /home/ec2-user/{directory}"  # Create directory if it doesn't exist
    ]
    print(f"Creating directory {directory} on EC2...")
    result = subprocess.run(check_directory_command, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Directory {directory} created or already exists.")
    else:
        print(f"Failed to create directory {directory}. Error:\n{result.stderr}")


def upload_files(public_ip, private_key_path):
    # Files to upload
    files_to_upload = [
        "setup.sh",
        "docker-compose.yml",
    ]
    
    # First, create the db-scripts directory
    create_directory_on_ec2(public_ip, private_key_path, "db-scripts")

    # Upload files
    for file in files_to_upload:
        # Check if the file already exists on EC2
        if file_exists_on_ec2(public_ip, private_key_path, file):
            if file == "setup.sh":
                delete_file_on_ec2(public_ip, private_key_path, "/home/ec2-user/setup.sh")
            else:
                print(f"{file} already exists on EC2. Skipping upload.")
                continue

        # Upload file if it doesn't exist
        upload_command = [
            "scp",
            "-i", private_key_path,
            "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
            file,
            f"ec2-user@{public_ip}:/home/ec2-user/"
        ]
        print(f"Uploading {file}...")
        result = subprocess.run(upload_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to upload {file}. Error:\n{result.stderr}")
            return
        print(f"{file} uploaded successfully.")
    
    # Now upload init.sql to the db-scripts directory
    init_sql_path = "db-scripts/init.sql"
    if not file_exists_on_ec2(public_ip, private_key_path, "db-scripts/init.sql"):
        upload_command = [
            "scp",
            "-i", private_key_path,
            "-o", "StrictHostKeyChecking=no",  # Automatically accept new hosts
            init_sql_path,
            f"ec2-user@{public_ip}:/home/ec2-user/db-scripts/"
        ]
        print(f"Uploading init.sql to db-scripts...")
        result = subprocess.run(upload_command, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to upload init.sql. Error:\n{result.stderr}")
            return
        print("init.sql uploaded successfully.")


def run_app(public_ip, private_key_path):
    # Upload files first
    upload_files(public_ip, private_key_path)

    # Run the setup script on EC2 after uploading
    run_script_on_ec2(public_ip, private_key_path)


# Specify your AWS credentials (for automatic login)
private_key_path = os.getenv("SSH_KEY_PATH")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
region = 'us-east-1'

# Create a session with the credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

# Now you can create a client/resource using this session
ec2_client = session.client('ec2')

# Tag name to identify your running EC2 instance
desired_instance_name = 'FlaskAppInstance'

# Check if the instance already exists and is running
def check_instance_exists():
    response = ec2_client.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': [desired_instance_name]},  # Filter by tag name
        ]
    )
    instances = response['Reservations']

    if instances:
        instance_state = instances[0]['Instances'][0]['State']['Name']
        instance_id = instances[0]['Instances'][0]['InstanceId']
        public_ip = instances[0]['Instances'][0].get('PublicIpAddress', 'N/A')

        if instance_state == 'running':
            return instance_id, public_ip, 'running'
        elif instance_state == 'stopped':
            return instance_id, public_ip, 'stopped'

    return None, None, None

# Try to find an existing instance first
instance_id, public_ip, state = check_instance_exists()

if instance_id:
    if state == 'running':
        print(f"Instance already running. ID: {instance_id}, Public IP: {public_ip}")
    elif state == 'stopped':
        print(f"Instance is stopped. Starting it now...")

        # Start the stopped instance
        ec2_client.start_instances(InstanceIds=[instance_id])
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        # Get the public IP of the EC2 instance (after starting it)
        instance = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')
        print(f"EC2 instance is running at: {public_ip}")
else:
    # If no instance exists, create a new one
    instance_params = {
        'ImageId': 'ami-0453ec754f44f9a4a',  # Replace with your desired AMI ID
        'InstanceType': 't2.micro',          # Choose instance type (e.g., 't2.micro' for the free tier)
        'MinCount': 1,
        'MaxCount': 1,
        'KeyName': 'aws_cli_key',                # Replace with your EC2 key pair name
        'SecurityGroupIds': ['sg-033cc57f4bddfbd55'],  # Replace with your security group ID
        'SubnetId': 'subnet-0459486efaab02d08',  # Replace with your VPC subnet ID
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': desired_instance_name  # Tag your instance with a name
                    }
                ]
            }
        ]
    }

    # Launch the EC2 instance
    response = ec2_client.run_instances(**instance_params)

    # Get the instance ID
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance {instance_id} is being created...")

    # Wait until the instance is running
    ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])

    # Get the public IP of the EC2 instance
    instance = ec2_client.describe_instances(InstanceIds=[instance_id])
    public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(f"EC2 instance is running at: {public_ip}")

time.sleep(20)
try:
    run_app(public_ip, private_key_path)
except Exception as e:
    print(f"Error running app: {e}")
