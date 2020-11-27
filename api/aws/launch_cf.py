"""
This script launches a cloudformation stack with a VPC, a public and a private subnet.

"""
# !/usr/bin/env python3
import boto3
import json

stack_name ='DakobedLibrosaServicesStack'

cloud_formation_client = boto3.client('cloudformation')
with open('stack/cloudformation_stack.yaml', 'r') as cf_file:
    cft_template = cf_file.read()
    cloud_formation_client.create_stack(StackName=stack_name, TemplateBody=cft_template, Capabilities=['CAPABILITY_NAMED_IAM'])
waiter =cloud_formation_client.get_waiter('stack_create_complete')
print("...waiting for stack to be ready...")
waiter.wait(StackName=stack_name)

stack_json = cloud_formation_client.describe_stacks(StackName=stack_name)
with open('output/stack_output.json', 'w') as fp:
    json.dump(stack_json, fp, default=str)