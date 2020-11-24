import json
import boto3
import base64
import uuid
# import requests

def lambda_handler(event, context):
    title = "first"
    user = "mddarr"
    # file_path = '{}/{}.wav'.format(user, title.lower().replace(' ', '-'))
    # file_content = base64.b64decode(event['content'])
    #
    # s3 = boto3.client('s3')
    # s3_response = ''
    # try:
    #     s3_response = s3.put_object(Bucket='dakobed-transcriptions', Key=file_path, Body=file_content)
    #
    # except Exception as e:
    #     s3_response = str(e)
    #     print(e)

    return {
        'statusCode': 200,
        'body': user
    }
