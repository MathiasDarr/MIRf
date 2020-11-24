from flask import Flask, render_template
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from helpers import *
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

app = Flask(__name__)
app.config.from_object("config")

s3 = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
dynamo = boto3.resource('dynamodb')  # , endpoint_url='http://localhost:8000')
table = dynamo.Table('UserUploads')


def user_upload_file(user, file):
    """
    This function uploads the uploaded file to s3 and creates an item in the database with the uploaded files url

    :param user: email address of authenticated user
    :param file: uploaded file
    :return:
    """
    user_directory = parse_email(user)
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            '{}/{}'.format(user_directory, file.filename),
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        filepath = "{}{}/{}".format(S3_LOCATION,user_directory, file.filename)

        table.put_item(
            Item={
                'user': user,
                'fileurl': filepath,
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


@app.route("/upload/<user>", methods=["POST"])
def upload_file(user):
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file = request.files["user_file"]
    if file:
        file.filename = secure_filename(file.filename)
    if file.filename == "":
        return "Please select a file"

    return user_upload_file(user, file)


if __name__ == "__main__":
    app.run()
