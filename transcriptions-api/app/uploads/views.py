from flask_restful import Resource, reqparse
import werkzeug
from config import S3_LOCATION, S3_BUCKET
from botocore.exceptions import ClientError
from flask_cors import CORS
import boto3



s3 = boto3.client("s3", region_name='us-west-2') #  aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
dynamo = boto3.resource('dynamodb', region_name='us-west-2')  # , endpoint_url='http://localhost:8000')
table = dynamo.Table('UserUploads')


class UploadFile(Resource):
    def get(self):
        return "hello"

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        image_file = args['file']
        image_file.save("your_file_name.jpg")


def delete_user_upload_item(user, filename):
    """
    This function deletes a user upload file
    :param user: authenticated user (partition key of the UserUploads dynamo table)
    :param filename: filename to be deleted
    :return:
    """
    try:
        response = table.delete_item(
            Key={
                'user': user,
                'filename': filename
            },
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response


def user_upload_file(user, file):
    """
    This function uploads the uploaded file to s3 and creates an item in the database with the uploaded files url

    :param user: email address of authenticated user
    :param file: uploaded file
    :return:
    """
    user_directory = parse_email(user)
    filename = file.filename
    filepath = "{}{}/{}".format(S3_LOCATION, user_directory, filename)
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            '{}/{}'.format(user_directory, file.filename),
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        table.put_item(
            Item={
                'user': user,
                'filename': filename,
                'fileurl': filepath
            }
        )
        return filepath

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e


def parse_email(user_email):
    split = user_email.split("@")
    host = split[1].split('.')[0]
    return '{}_{}'.format(split[0], host)