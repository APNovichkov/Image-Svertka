from flask import Flask, render_template
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import os


original_images_folder = os.path.join('static', 'original_images')
new_images_folder = os.path.join('static', 'edited_images')

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = original_images_folder
app.config['UPLOAD_FOLDER'] = new_images_folder

# Filters

f_outline = [
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
]

f_sharp = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
]

f_blur = (np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]) / 9).tolist()

f_custom = (np.array([
    [0, 0, 1],
    [0, -1, 0],
    [1, 0, 0]
])).tolist()


@app.route('/')
def index():
    original_img_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'waterfall.jpg')
    original_img = img.imread(original_img_path)

    # new_img_1 = apply_filter(orignal_img, f_blur)
    new_img = apply_filter(original_img, f_outline)
    new_img = new_img.astype('uint8')
    new_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'waterfall_outline.jpg')

    img.imsave(new_img_path, new_img)

    return render_template(
        "index.html",
        original_img_path=original_img_path,
        new_img_path=new_img_path)


def apply_filter(img, f):
    ROWS = img.shape[0]
    COLS = img.shape[1]

    d = np.zeros((ROWS, COLS, 3), dtype=int).tolist()
    for k in range(3):
        for i in range(ROWS - 2):
            for j in range(COLS - 2):
                s = 0
                for ii in range(3):
                    for jj in range(3):
                        s += img[i + ii][j + jj][k] * f[ii][jj]
                d[i + 1][j + 1][k] = int(s)
    d = np.array(d)
    return np.clip(d, 0, 255)


if __name__ == '__main__':
    app.run(debug=True)
