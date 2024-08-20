from flask import Blueprint, render_template, request
import tensorflow as tf
import os
import cv2
import imghdr
import numpy as np
import math

here = os.path.dirname(os.path.abspath(__file__))    

model = tf.keras.models.load_model(os.path.join(os.path.dirname(here), 'pineapple_CNN.keras'))
views = Blueprint(__name__, "views")

@views.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@views.route("/", methods=['POST'])
def predict():
    imagefile=request.files['imagefile']
    image_path="./images/" + imagefile.filename

    if image_path=="./images/":
        return render_template("index.html")

    imagefile.save(image_path)
    img = cv2.imread(image_path)
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

    return render_template("index.html", prediction=y_pred, prob=yhat)


view2 = Blueprint(__name__, "bocci")
@view2.route("/bocci")
def home2():
    return "bocci the rock"


