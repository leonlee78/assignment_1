import boto3
from datetime import datetime, timedelta

ec2 = boto3.resource('ec2')
cloudwatch = boto3.client('cloudwatch')
imageId = "ami-baf632ac"


def create_ec2_instances():
    ec2.create_instances(ImageId=imageId, MinCount=1,MaxCount=2)


def stop_ec2_instances(ids):
    ec2.instances.filter(InstanceIds=ids).stop()
    ec2.instances.filter(InstanceIds=ids).terminate()

# Use the filter() method of the instances collection to retrieve all running EC2 instances
def list_ec2_instances():
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        print(instance.id, instance.instance_type)

def get_cpu_utilization(instance_id):
    print(instance_id)
    now = datetime.utcnow()
    past = now - timedelta(minutes=1440)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=past,
        EndTime=now,
        Period=3600,
        Statistics=['Average'])
    print(response)
    #TODO: get the sum of all average


def is_above_threshold(threshold):
    if get_cpu_utilization("i-01e26623dacc9c5b2") > threshold:
        print("greater")
        #use the AWS EC2 API to resize its worker pool

def resize_instance(instance_id):
    # Stop the instance
    cloudwatch.stop_instances(InstanceIds=[instance_id])
    waiter = cloudwatch.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    # Change the instance type
    cloudwatch.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value='t2.medium')

    # Start the instance
    cloudwatch.start_instances(InstanceIds=[instance_id])

'''
def delete_image_s3():
    #TODO:

def delete_db_value():
    #TODO
'''

if __name__== "__main__":
    #list_ec2_instances()
    #get_cpu_utilization("i-01e26623dacc9c5b2")
