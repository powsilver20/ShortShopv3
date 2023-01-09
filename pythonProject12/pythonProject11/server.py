from flask import Flask, request, render_template, redirect, make_response, url_for, flash
from werkzeug.utils import secure_filename
import sqlite3
import os
app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        path = r"static/images/text.txt"
        assert os.path.isfile(path)
        with open(path, "r") as f:
            pass
        pic = request.files['file']
        pic.save(os.path.join(app.config['UPLOAD_FOLDER']),"name")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)