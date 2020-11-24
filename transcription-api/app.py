from flask import Flask, render_template
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from helpers import *
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

app = Flask(__name__)
app.config.from_object("config")

s3 = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)


@app.route("/", methods=["POST"])
def upload_file():
    """
        These attributes are also available
        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype
    """
    # A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

    # B
    file = request.files["user_file"]
    if file:
        file.filename = secure_filename(file.filename)
    if file.filename == "":
        return "Please select a file"
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        return "{}{}".format(S3_LOCATION, file.filename)

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e


if __name__ == "__main__":
    app.run()
