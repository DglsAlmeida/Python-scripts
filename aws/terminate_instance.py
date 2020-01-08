#!/usr/bin/python3

import boto3
import sys

# By: Douglas Almeida 
# Email: Douglas.alu.lmb@gmail.com
# The script must be invocated passing instacename
# ex: python3 create_instance.py instance01

#connection with client ec2
client = boto3.client('ec2', region_name='us-west-2')

#validation of the instance name
try:
    sys.argv[1]
except:
    print("instance name not found!!")
    sys.exit(1)
else:
    instance_name = sys.argv[1]

#getting api id
def getting_instance_id():
    response = client.describe_instances()

    reservations = response["Reservations"]
    instances = [reservation['Instances'][0] for reservation in reservations]

    for instance in instances:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                id_ami_base = instance['InstanceId']
    return id_ami_base

#disabling APiTermination
def DisableAPiTermination(instanceid):
    response = client.modify_instance_attribute(
        InstanceId=instanceid,
        DisableApiTermination={
        'Value': False
        }
    )

#killing the instance
def terminateInstances(instanceid):
    response = client.terminate_instances(
        InstanceIds=[
          instanceid,
        ]
    )

DisableAPiTermination(getting_instance_id())
terminateInstances(getting_instance_id())
