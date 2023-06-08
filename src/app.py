import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()  # Take environment variables from .env.
print(os.environ.get('ARTEFACT_VERSION'))

max_hours = int(os.environ.get('EC2_MAX_HOURS'))
# Key tag for checking
excep_word = 'dont shoot'

# Make sure credentials are set
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

# Get a list of all available AWS regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

for region in regions:
    ec2 = boto3.client('ec2', region_name=region)

    # Get a list of all instances in the current region
    response = ec2.describe_instances()
    instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    for instance in instances:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']

        # Check if the super tag exists
        tags = instance['Tags']
        excepted = False
        for tag in tags:
            if tag['Key'] == excep_word:
                print(f"Tag {excep_word} found in {instance_id} in region {region}.")
                excepted = True
                break
        else:
            print(f"Super tag not found in {instance_id} in region {region}.")

        # Stop the instance
        if state == 'running' and not excepted:
            launch_time = instance['LaunchTime']
            current_time = datetime.now(launch_time.tzinfo)
            running_time = current_time - launch_time

            if running_time > timedelta(hours=max_hours):
                ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Instance {instance_id} in region {region} stopped.")
