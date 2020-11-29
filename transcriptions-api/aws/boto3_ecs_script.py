import boto3
import json
from aws_utils import create_application_load_balancer_listener, create_network_load_balancer, create_ecs_service, \
    create_target_group, create_security_group, create_application_load_balancer, create_network_load_balancer_listener, \
    register_ecs_task, delete_ecs_service, delete_target_group, delete_load_balancer


with open('output/stack_output.json') as f:
  data = json.load(f)

outputs = data['Stacks'][0]['Outputs']

stack = {}
stack['accountID'] = outputs[0]['OutputValue']
stack['securitygroupID'] = outputs[1]['OutputValue']
stack['publicsubnet1'] = outputs[2]['OutputValue']
stack['ecstaskrole'] = outputs[3]['OutputValue']
stack['region'] = outputs[4]['OutputValue']
stack['vpcID'] = outputs[5]['OutputValue']
stack['ecsservicerole'] = outputs[6]['OutputValue']
stack['privatesubnet1'] = outputs[7]['OutputValue']


security_group_id = create_security_group(stack['vpcID'], 'dakobed-sg')

task_name = 'dbardtask'
service_name ='dakobedservice'

register_ecs_task(task_name)

subnets = {'public1':stack['publicsubnet1'], 'private1':stack['privatesubnet1']}
application_load_balancer_name = 'dakobedapplicationlb'


application_load_balancer_response = create_application_load_balancer(application_load_balancer_name, stack['publicsubnet1'])
application_load_balancer_arn = application_load_balancer_response['LoadBalancers'][0]['LoadBalancerArn']
load_balancer_dns = application_load_balancer_response['LoadBalancers'][0]['DNSName']

target_group_arn = create_target_group('dakobed-target-group',stack['vpcID'])

create_application_load_balancer_listener(application_load_balancer_arn, target_group_arn)

service_response =  create_ecs_service(service_name, task_name, subnets, security_group_id, target_group_arn)


# delete_load_balancer(application_load_balancer_arn)
# delete_target_group(target_group_arn)
# delete_ecs_service(service_name)

