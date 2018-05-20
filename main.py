import os
import random

from threading import Lock

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
mutex = Lock()


DEFAULT_STATIC_PATH = "/static"

IMG_PATH_TO_TAG = {
    "01foto.jpg": "OCCHIALI",
    "02foto.jpg": "SVEGLIA",
    "03foto.jpg": "CUCCHIAINO",
    "04foto.jpg": "BICCHIERE",
    "05foto.jpg": "PIATTO",
    "06foto.jpg": "MELA",
    "07foto.jpg": "BOTTIGLIA",
    "08foto.jpg": "TAZZA",
}


@app.route("/")
def root_handler():
    img_data = _get_random_img()
    session["tag"] = img_data["tag"]
    session["path"] = img_data["path"]
    return render_template("index.html", **img_data)


@app.route("/reload")
def reload_handler():
    img_data = _get_random_img()
    session["tag"] = img_data["tag"]
    session["path"] = img_data["path"]
    return jsonify(img_data)


@app.route("/upload", methods=["GET", "POST"])
def upload_handler():
    if request.method == "GET":
        return render_template("upload.html")
    if request.method == "POST":
        if "file" not in request.files:
            flash("Selezionare un file")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("upload.html")


@app.route("/name", methods=["GET"])
def name_handler():
    if request.args.get("tag").upper() == session["tag"]:
        img_data = _get_random_img()
        session["tag"] = img_data["tag"]
        session["path"] = img_data["path"]
        return jsonify(img_data)
    else:
        return jsonify({"tag": session["tag"], "path": session["path"]})


def _get_random_img():
    images = [f for f in os.listdir("static") if f.endswith(".jpg")]
    img = images[random.randint(0, len(images) - 1)]
    path = os.path.join(DEFAULT_STATIC_PATH, img)
    mutex.acquire()
    tag = IMG_PATH_TO_TAG[img]
    mutex.release()

    return {
        "path": path,
        "tag": tag,
    }


if __name__ == '__main__':
    app.secret_key = "my secret key"
    app.config["SESSION_TYPE"] = "filesystem"
    app.run()
