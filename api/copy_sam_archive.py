"""
This script is a hack to download the archive file from cloud s3 and upload it to


"""
# !/usr/bin/env python3

import boto3
import os


BUCKET = 'dakobed-serverless-apis'


s3_client = boto3.client('s3')
objs = s3_client.list_objects_v2(Bucket=BUCKET)['Contents']


## Download the object in the bucket that was most recently modified.
get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
sorted_objects = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)]
archive_file = sorted_objects[0]

local_archive_file = './tmp/{}'.format(archive_file)

## Download from cloud S3
with open(local_archive_file, 'wb') as f:
    s3_client.download_fileobj(BUCKET, archive_file, f)

## Upload to local S3
s3_local_client = boto3.client('s3', endpoint_url='http://localhost:4566')


s3_local_client.create_bucket(Bucket=BUCKET)


with open(local_archive_file, "rb") as f:
    s3_local_client.upload_fileobj(f, BUCKET, archive_file)

## Delete the file from temp
for f in os.listdir('tmp'):
    os.remove(os.path.join('tmp', f))


