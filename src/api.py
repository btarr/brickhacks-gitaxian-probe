from flask import Flask, request, redirect, url_for, jsonify
import os
import detect_script
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './tmp'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['data']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save('{}.jpg'.format(os.path.join(UPLOAD_FOLDER, filename)))
            cards = detect_script.crop_image(cv2.imread('{}.jpg'.format(os.path.join(UPLOAD_FOLDER, filename))))
            print cards
            return jsonify(**cards)


app.run(debug=True)
