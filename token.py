import boto3

# client = boto3.client('cognito-idp')
UserPoolId = 'us-west-2_pjwRbMQJ1',
ClientId = 'g2lpoe0m73vmgipkrj2f85jrr',

from pycognito import Cognito

u = Cognito(UserPoolId,ClientId, username='mddarr@gmail.com')
u.authenticate(password='1!Iksarmanssss')