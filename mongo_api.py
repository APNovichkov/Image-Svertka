# Mongo API
# The functions to implement:
# List Images Metadata - Returns a list of the stuff located in FS
# Get Image - Returns the img.read() and
# Add images - Takes as parameters a bunch of stuff

from pymongo import MongoClient
import gridfs
import os
from bson import ObjectId
import matplotlib.image as img


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

    def get_image_with_filter(self, imageId, filter):
        original_img = None
        for currant_image in self.img_cl.find({'fs_id': imageId}):
            original_img = img.imread(currant_image['path'])

        ROWS = original_img.shape[0]
        COLS = original_img.shape[1]

        filtered_image = np.zeros((ROWS, COLS, 3), dtype=int).tolist()
        for k in range(3):
            for i in range(ROWS - 2):
                for j in range(COLS - 2):
                    sum = 0
                    for ii in range(3):
                        for jj in range(3):
                            sum += original_img[i + ii][j + jj][k] * filter[ii][jj]
                    filtered_image[i + 1][j + 1][k] = int(sum)
        filtered_image = np.array(filtered_image)
        return np.clip(filtered_image, 0, 255)


if __name__ == "__main__":
    dp = DataProvider()
    print(dp.get_image_with_filter('5d89b79a771bb11d8b28c91c', ""))

    # base_dir = "/Users/andreynovichkov/Desktop/Make-School/Personal-projects/Image-editing/static/original_images"
    # dp = DataProvider()
    # dp.add_image('Oregon Waterfall', 'Nature', 'United States', base_dir + '/waterfall.jpg')

    # remove_image({'name': 'San Francisco'})

    # fout = open("/Users/andreynovichkov/Desktop/sf_test.jpg", "wb")
    # fout.write(get_image(img_cl.find_one({'name': 'San Francisco'})['fs_id']))

    # for row in dp.list_images():
    #    print(row)
