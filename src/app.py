import boto3
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()  # Take environment variables from .env.
print(os.environ.get('ARTEFACT_VERSION'))

# TODO Make sure credentials are set
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY

max_mins = int(os.environ.get('EC2_MAX_MINS'))
print(f"Time EC2 allowed to run: {max_mins}")

# Key tag for checking
except_word = 'dont shoot'
print(f"Tag which allows to skip stopping: {except_word}")


# Get a list of all available AWS regions, use us-west-2 as default region
ec2_client = boto3.client('ec2', region_name='us-west-2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

for region in regions:
    ec2 = boto3.client('ec2', region_name=region)

    # Get a list of all instances in the current region
    response = ec2.describe_instances()
    instances = [instance for reservation in response['Reservations'] for instance in reservation['Instances']]

    for instance in instances:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        launch_time = instance['LaunchTime']
        current_time = datetime.now(launch_time.tzinfo)
        running_time = current_time - launch_time

        print(f"instance {instance_id} found in region {region}; last uptime: {running_time}; state: {state}")

        # Check if the super tag exists
        tags = instance['Tags']
        excepted = False
        for tag in tags:
            if tag['Key'] == except_word:
                print(f"Tag {except_word} found in {instance_id} in region {region}.")
                excepted = True
                break
        #else:
            #print(f"Super tag not found in {instance_id} in region {region}.")

        # Stop the instance
        if state == 'running' and not excepted and running_time > timedelta(minutes=max_mins):
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} stopped.")
