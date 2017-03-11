import boto3

class LoadBalancer:
	client = boto3.client('elb')
	loadbalance_name ='ece1779LB'

	def register_instance(self, instance_id):
		response = self.client.register_instances_with_load_balancer(
		    LoadBalancerName=self.loadbalance_name,
		    Instances=[
		        {
		            'InstanceId': instance_id
		        },
		    ]
		)
		print(response)

	def deregister_instance(self, instance_id):
		response = self.client.deregister_instances_from_load_balancer(
		    LoadBalancerName=self.loadbalance_name,
		    Instances=[
		        {
		            'InstanceId': instance_id
		        },
		    ]
		)


if __name__== "__main__":
	lb = LoadBalancer()
	#lb.register_instance('i-04fa8ff8a9c5d8927')
	lb.deregister_instance('i-04fa8ff8a9c5d8927')
