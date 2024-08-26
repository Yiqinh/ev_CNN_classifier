from flask import Flask, jsonify, request

import tensorflow as tf
import os
import cv2
import imghdr
import numpy as np
import math

from werkzeug.utils import secure_filename

here = os.path.dirname(os.path.abspath(__file__))    
model = tf.keras.models.load_model(os.path.join(os.path.dirname(here), 'pineapple_CNN.keras'))

cur_image = [None]

app = Flask(__name__)

@app.route("/cnn", methods=['POST'])
def upload():
    if cur_image[0]:
        os.remove(cur_image[0])
        cur_image[0] = None

    d = {}
    try:
        file = request.files['file_from_react']
        filename = file.filename
        print(f"Uploading file {filename}")
        d['status'] = 'OPEN SEASAME'

        filename=secure_filename(file.filename)
        image_path="./images/" + filename

        file.save(image_path)
        print(imghdr.what(image_path))
        cur_image[0] = image_path

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)

@app.route("/infer", methods=['POST'])
def infer():
    d = {}
    img = cv2.imread(cur_image[0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resize = tf.image.resize(img, (256,256))
    yhat = model.predict(np.expand_dims(resize/255, 0))
   
    if yhat > 0.5:
        y_pred = "Pineapple"
    else:
        y_pred = "No Pineapple"

    yhat = float(yhat[0][0])
    yhat = max(yhat, 1-yhat)
    yhat = math.floor(yhat * 100) / 100
    if yhat == 1.0:
        yhat = 0.99

    #clean up
    os.remove(cur_image[0])
    cur_image[0] = None
    #send results
    if y_pred == "Pineapple":
        d["pineapple"] = yhat
        d['no_pineapple'] = 1 - yhat
        d['pine_top'] = str(True)
        d['no_pine_top'] = str(False)
    else:
        d["no_pineapple"] = yhat
        d['pineapple'] = 1 - yhat
        d['pine_top'] = str(False)
        d['no_pine_top'] = str(True)

    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True, port=8000)