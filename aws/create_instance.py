#!/usr/bin/python3

import boto3
import sys

# By: Douglas Almeida 
# Email: Douglas.alu.lmb@gmail.com
# The script must be invocated passing two parameters imageid and instacename
# ex: python3 create_instance.py ami-0c5204531f799e0c6 instance01

#validation of the image id
try:
    sys.argv[1] 
except:
    print("image id not found")
    sys.exit(1)

image_id_validation = sys.argv[1]

if image_id_validation[0:4] != "ami-":
        print("image_id incorrect")
        sys.exit(1)
else:
    image_id = sys.argv[1]

#validation of the instance name
try:
    sys.argv[2]
except:
    print("instance name not found!!")
    sys.exit(1)
else:
    instance_name = sys.argv[2]

#connection with client ec2 *-*
client = boto3.client('ec2', region_name='us-west-2')

#creating the instance with AMI base
def create_instance(imageID, instanceName):
    response = client.run_instances(
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
        ImageId=imageID,
        KeyName='KeyName',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        Monitoring={
            'Enabled': False
        },
        SecurityGroupIds=[
            'SecurityGroupName',
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instanceName
                    }
                ]
            },
        ],
        DisableApiTermination=True,
        IamInstanceProfile={
            'Name': 'IamName'
        },

    )

#getting instance id
def getting_instance_id():
    response = client.describe_instances()

    reservations = response["Reservations"]
    instances = [reservation['Instances'][0] for reservation in reservations]

    for instance in instances:
        for tag in instance['Tags']:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                id_ami_base = instance['InstanceId']
    return id_ami_base            

#waiting the instance running
def wait_until_instance_running(instanceid):
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instanceid)
    instance.wait_until_running()

create_instance(image_id, instance_name)
wait_until_instance_running(getting_instance_id())
