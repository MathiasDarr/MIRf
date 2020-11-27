from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
from uploads.views import UploadFile
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)

CORS(app)
#
app.config.from_object("config")


api.add_resource(UploadFile, '/upload')
# api.add_resource(upload, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)





