# Mongo API
# The functions to implement:
# List Images Metadata - Returns a list of the stuff located in FS
# Get Image - Returns the img.read() and
# Add images - Takes as parameters a bunch of stuff

from pymongo import MongoClient
import gridfs
import os
from bson import ObjectId


class DataProvider:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['images']
        self.img_cl = self.db['image_paths']
        self.fs = gridfs.GridFS(self.db)

    # Adds image to FS as a file, and adds metadata about that image to the image paths collection -> img_cl
    def add_image(self, name, category, location_by_country, path):
        imageID = self.fs.put(open(path, "rb"))

        input = {
            "fs_id": imageID,
            "name": name,
            "category": category,
            "location_by_country": location_by_country,
            "file_size": os.path.getsize(path),
            "path": path
        }

        self.img_cl.insert_one(input)

    # Returns a list of all documents in the img_cl collection
    def list_images(self, query={}):
        return self.img_cl.find(query)

    # Removes image or images, depending on how many query matches we get
    def remove_image(self, query):
        if len(query) != 0:
            for row in self.img_cl.find(query):
                fs_id = row['fs_id']
                print("Removing image from fs with id: " + str(fs_id))
                self.fs.delete(fs_id)

            self.img_cl.delete_many(query)
        else:
            print("query is empty :(")

    def get_image(self, imageID):
        return self.fs.get(ObjectId(imageID)).read()


if __name__ == "__main__":
    add_image('San Francisco', 'City', 'United States', '/Users/andreynovichkov/Desktop/to-post-in-august/_DSC0569.jpg')

    # remove_image({'name': 'San Francisco'})

    fout = open("/Users/andreynovichkov/Desktop/sf_test.jpg", "wb")
    fout.write(get_image(img_cl.find_one({'name': 'San Francisco'})['fs_id']))

    for row in list_images():
        print(row)
