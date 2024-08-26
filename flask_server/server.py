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

cur_image = None

app = Flask(__name__)

@app.route("/cnn", methods=['POST'])
def upload():
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
        cur_image = image_path

    except Exception as e:
        print(f"Couldn't upload file {e}")
        d['status'] = 0

    return jsonify(d)

@app.route("/infer", methods=['POST'])
def infer():
    d = {}
    img = cv2.imread(cur_image)
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
    
    #clean up
    os.remove(cur_image)

    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True, port=8000)