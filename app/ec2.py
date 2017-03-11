import boto3
from datetime import datetime, timedelta
from operator import itemgetter


class EC2:
    ec2 = boto3.resource('ec2')
    cloudwatch = boto3.client('cloudwatch')     
    imageId = "ami-baf632ac"

    def create_ec2_instances(self,minCount, maxCount):
        imageId = self.imageId
        ec2 = self.ec2
        ec2.create_instances(ImageId=imageId, MinCount=minCount,MaxCount=maxCount,InstanceType='t2.small')


    def stop_ec2_instances(self,ids):
        print("stop")
        ec2 = self.ec2
        ec2.instances.filter(InstanceIds=ids).stop()
        ec2.instances.filter(InstanceIds=ids).terminate()

    def get_cpu_utilization(self,instance_id):
        print(instance_id)
        now = datetime.utcnow()
        past = now - timedelta(minutes=1440)
        results = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=past,
            EndTime=now,
            Period=300,
            Statistics=['Average'])
        datapoints = results['Datapoints']
        last_datapoint = sorted(datapoints, key=itemgetter('Timestamp'))[-1]
        utilization = last_datapoint['Average']
        load = round((utilization/100.0), 2)
        print("***LOAD***")
        print(load)
        return load


    def is_above_threshold(self,threshold):
        if self.get_cpu_utilization("i-01e26623dacc9c5b2") > threshold:
            self.resize_instance('GROW',2)
            print("greater")
        else:
            self.resize_instance('SHRINK',2)
            print("less")
            #use the AWS EC2 API to resize its worker pool


    def resize_instance(self,type,ratio):
        #find no of instances running
        state = 'pending'
        numInstance = self.findNoInstances(state)
        if type == 'GROW':
            if numInstance == 0:
                state = 'running'
                numInstance = self.findNoInstances(state)
                print("**NO OF INSTANCES**")
                print(numInstance)
                #create more instances
                self.create_ec2_instances(numInstance*ratio,numInstance*ratio)
        else:
            state = 'running'
            numInstance = self.findNoInstances(state)
            if numInstance > 1:
                self.stopInstances('running', (numInstance/ratio))

    # Use the filter() method of the instances collection to retrieve all running EC2 instances
    # and the count
    def findNoInstances(self,state):  
        ec2 = self.ec2
        instances = ec2.instances.filter(
            Filters = [{'Name': 'instance-state-name', 'Values': [state]}])
        count = 0
        for instance in instances:
            #print(instance.id, instance.instance_type)
            count = count +1
        return count

    def stopInstances(self,state,num_to_stop):  
        ec2 = self.ec2
        instances = ec2.instances.filter(
            Filters = [{'Name': 'instance-state-name', 'Values': [state]}])
        count = 0
        instance_list = []
        for instance in instances:
            if count < num_to_stop:
                print("stop "+instance.id)
                instance_list.append(instance.id)
            count = count +1
        self.stop_ec2_instances(instance_list)

    def listInstance(self, state):  
        ec2 = self.ec2
        instances = ec2.instances.filter(
            Filters = [{'Name': 'instance-state-name', 'Values': [state]}])
        count = 0
        instance_list = []
        for instance in instances:
            instance_list.append(instance.id)
        return instance_list

if __name__== "__main__":
    #list_ec2_instances()
    #get_cpu_utilization("i-01e26623dacc9c5b2")
    e = EC2()
    e.is_above_threshold(0.9)#10%

'''def resize_instance(numInstance):
    #create more instances
    create_ec2_instances(numInstance)
    # Stop the instance
    cloudwatch.stop_instances(InstanceIds=[instance_id])
    waiter = cloudwatch.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    # Change the instance type
    cloudwatch.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value='t2.medium')

    # Start the instance
    cloudwatch.start_instances(InstanceIds=[instance_id])
    '''
