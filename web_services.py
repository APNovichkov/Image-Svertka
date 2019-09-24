import flask
from flask import Flask
from mongo_api import DataProvider
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
dp = DataProvider()

PROPS_TO_STR = ['_id', 'fs_id', 'image_id']

# app configurations for uploading files
app.config['UPLOAD_FOLDER'] = "/Users/andreynovichkov/Desktop/Make-School/Personal-projects/Image-editing/static/uploaded_images"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# Return json with all of the images that are stored in mongoDB
@app.route("/imgs")
def list_all_images():
    output = []
    for row in dp.list_images({}):
        print('Before', row)
        _to_str(row, PROPS_TO_STR)
        print('After', row)
        output.append(row)

    return json.dumps({'result': output})


def _to_str(row, props):
    for prop in props:
        if prop in row:
            row[prop] = str(row[prop])


@app.route("/")
def index():
    return "Hello"


# Returns an image given an fs_id
@app.route("/imgs/<string:id>")
def get_image(id):
    resp = flask.make_response(dp.get_image(id))
    resp.content_type = "image/jpg"
    return resp


if __name__ == '__main__':
    app.run(debug=True)
