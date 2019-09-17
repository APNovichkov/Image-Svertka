import flask
from flask import Flask
from mongo_api import DataProvider
import json
from bson import ObjectId

app = Flask(__name__)
dp = DataProvider()


# Should return json with all of the images that are stored in mongoDB
@app.route("/imgs/list_images")
def list_all_images():
    output = []
    for row in dp.list_images({}):
        print(row)
        row['_id'] = str(row['_id'])
        row['fs_id'] = str(row['fs_id'])
        output.append(row)

    return json.dumps({'result': output})


@app.route("/")
def index():
    return "Hello"


if __name__ == '__main__':
    app.run(debug=True)


@app.route("/imgs/<string:id>")
def get_image(id):
    resp = flask.make_response(dp.get_image(id))
    resp.content_type = "image/jpg"
    return resp
