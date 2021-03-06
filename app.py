from flask import Flask, request
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img,img_to_array

app= Flask(__name__)
model=tf.keras.models.load_model("vgg16_b32_f.h5")

def predict_class(file_path):
    img=Image.open(file_path)
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array2 = tf.keras.applications.vgg16.preprocess_input(img_array)
    img_array2 = tf.expand_dims(img_array2, 0)
    result = model.predict(img_array2)
    class_subset = ['cardboard', 'ewaste', 'glass', 'metal', 'organic', 'paper', 'plastic']
    predicted_class = class_subset[np.argmax(result[0])]
    return predicted_class

@app.route("/")
def main():
    return "It is working"

@app.route("/process", methods=["POST"])
def processReq():
    data = request.files["img"]
    resp = predict_class(data)
    return resp

if __name__=='__main__':
    app.run(debug=True)