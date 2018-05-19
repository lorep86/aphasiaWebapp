import os
import random

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DEFAULT_STATIC_PATH = "/static"

IMG_PATH_TO_NAME = {
    "01foto.jpg": "OCCHIALI",
    "02foto.jpg": "SVEGLIA",
    "03foto.jpg": "CUCCHIAINO",
    "04foto.jpg": "BICCHIERE",
    "05foto.jpg": "PIATTO",
    "06foto.jpg": "MELA",
    "07foto.jpg": "BOTTIGLIA",
    "08foto.jpg": "TAZZA",
}

current_img_data = {
    "path": "",
    "name": "",
}


@app.route("/")
def root_handler():
    return render_template("index.html", **_get_random_img())


@app.route("/reload")
def reload_handler():
    return jsonify(_get_random_img())


@app.route("/upload")
def upload_handler():
    return render_template("upload.html")


@app.route("/name", methods=["POST"])
def name_handler():
    if request.form["inputName"].upper() == current_img_data["name"]:
        return render_template("index.html", **_get_random_img())
    else:
        return render_template("index.html", **current_img_data)


def _get_random_img():
    images = [f for f in os.listdir("static") if f.endswith(".jpg")]
    img = images[random.randint(0, len(images) - 1)]
    current_img_data["path"] = os.path.join(DEFAULT_STATIC_PATH, img)
    current_img_data["name"] = IMG_PATH_TO_NAME[img]
    return current_img_data


if __name__ == '__main__':
    app.run()
