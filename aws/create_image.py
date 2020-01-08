#!/usr/bin/python3

import boto3
import sys

# By: Douglas Almeida 
# Email: Douglas.alu.lmb@gmail.com
# The script must be invocated passing parameter instacename
# ex: python3 create_instance.py instance01

#Validation instance name
try:
    sys.argv[1]
except:
    print("instance name not found!!")
    sys.exit(1)
else:
    instance_name = sys.argv[1]

#connection with client ec2
client = boto3.client('ec2', region_name='us-west-2')

#creating the AMI base
def create_image(instanceID, instanceName):
    response = client.create_image(
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'VolumeSize': 8,
                    'VolumeType': 'gp2'
                },
            },
        ],
        InstanceId=instanceID,
        Name=instanceName,
    )

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

create_image(getting_instance_id(), instance_name)
