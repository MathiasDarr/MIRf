import boto3
import json


def create_security_group(vpcID, sgname):
    ec2 = boto3.client('ec2')
    try:
        response = ec2.create_security_group(GroupName=sgname,
                                             Description='DESCRIPTION',
                                             VpcId=vpcID)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpcID))
        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 8080,
                 'ToPort': 8080,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            ])
        print('Ingress Successfully Set %s' % data)
        return response['GroupId']
    except  Exception as e:
        print(e)


def create_network_load_balancer(load_balancer_name, publicsubnet1):
    client = boto3.client('elbv2')
    nlb_response = client.create_load_balancer(
        Name=load_balancer_name,
        Subnets=[
            publicsubnet1
        ],
        Scheme='internet-facing',
        Type='network',
        IpAddressType='ipv4'
    )
    return nlb_response


def create_application_load_balancer(load_balancer_name, publicsubnet1):
    client = boto3.client('elbv2')
    nlb_response = client.create_load_balancer(
        Name=load_balancer_name,
        Subnets=[
            publicsubnet1
        ],
        Scheme='internet-facing',
        Type='network',
        IpAddressType='ipv4'
    )
    return nlb_response


def create_target_group(target_group_name, vpcID):
    client = boto3.client('elbv2')
    target_group_response = client.create_target_group(
        Name=target_group_name,
        Port=8080,
        Protocol='TCP',
        VpcId=vpcID,
        TargetType='ip'
    )
    return target_group_response['TargetGroups'][0]['TargetGroupArn']


def create_network_load_balancer_listener(load_balancer_arn, target_group_arn):
    client = boto3.client('elbv2')
    # target_group_arn = target_group_response['TargetGroups'][0]['TargetGroupArn']
    listener_response = client.create_listener(
        DefaultActions=[
            {
                'TargetGroupArn': target_group_arn,
                'Type': 'forward',
            },
        ],
        LoadBalancerArn=load_balancer_arn,
        Port=80,
        Protocol='TCP',
    )
    return listener_response


def create_application_load_balancer_listener(application_load_balancer_arn, target_group_arn):
    client = boto3.client('elbv2')
    # target_group_arn = target_group_response['TargetGroups'][0]['TargetGroupArn']
    listener_response = client.create_listener(
        DefaultActions=[
            {
                'TargetGroupArn': target_group_arn,
                'Type': 'forward',
            },
        ],
        LoadBalancerArn=application_load_balancer_arn,
        Port=80,
        Protocol='TCP',
    )
    return listener_response


def delete_load_balancer(load_balancer_arn):
    client = boto3.client('elbv2')
    response = client.delete_load_balancer(
        LoadBalancerArn=load_balancer_arn)


def delete_target_group(target_group_arn):
    client = boto3.client('elbv2')
    response = client.delete_target_group(
        TargetGroupArn=target_group_arn
    )


def delete_ecs_service(service_name):
    client = boto3.client('ecs')
    client.update_service(cluster='DakobedCluster', service=service_name, desiredCount=0)
    client.delete_service(cluster='DakobedCluster', service=service_name)


def register_ecs_task(task_name):
    client = boto3.client('ecs')
    instance_list = client.list_container_instances(cluster='DakobedCluster')['containerInstanceArns']
    response = client.register_task_definition(
        family=task_name,
        networkMode='awsvpc',
        taskRoleArn='arn:aws:iam::710339184759:role/dakobed-ecs-dynamo-role',
        executionRoleArn='arn:aws:iam::710339184759:role/ecsTaskExecutionRole',
        requiresCompatibilities=['FARGATE'],
        cpu='256',
        memory='512',
        containerDefinitions=[
            {
                'name': 'dakobedcontainer',
                'image': '710339184759.dkr.ecr.us-west-2.amazonaws.com/dakobed/services:latest',
                'cpu': 256,
                'memory': 512,
                'memoryReservation': 123,
                'logConfiguration': {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "dakobedservice-logs",
                        "awslogs-region": "us-west-2",
                        "awslogs-stream-prefix": "awslogs-dakobedservice-logs"
                    }
                },
                'portMappings': [
                    {
                        'containerPort': 8080,
                        'hostPort': 8080,
                        'protocol': 'http'
                    },
                ],
                'essential': True,
            },
        ],
    )


def create_ecs_service(service_name, task_name, subnets, security_group_id, target_group_arn):
    client = boto3.client('ecs')
    response = client.create_service(cluster='DakobedCluster',
                                     serviceName=service_name,
                                     launchType='FARGATE',
                                     taskDefinition=task_name,
                                     desiredCount=1,
                                     networkConfiguration={
                                         "awsvpcConfiguration": {
                                             "assignPublicIp": "ENABLED",
                                             "securityGroups": [security_group_id],
                                             "subnets": [subnets['public1'], subnets['public2'], subnets['private1'],
                                                         subnets['private2']]
                                         },
                                     },
                                     deploymentConfiguration={
                                         'maximumPercent': 100,
                                         'minimumHealthyPercent': 50},
                                     loadBalancers=[
                                         {"containerName": "dakobedcontainer",
                                          "containerPort": 8080,
                                          "targetGroupArn": target_group_arn
                                          }
                                     ]),
    return response
