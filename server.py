
from flask import Flask, jsonify, make_response, send_file
from urllib.parse import unquote
import os
import utils
import value
import config
import logging


app = Flask(__name__)
app.debug = False


@app.route("/")
def home():
    html_template = utils.get_html_template().replace("{z}", value.sender_str).replace("{a}", value.trans_origin_str).replace("{b}",value.trans_target_str)
    return make_response(html_template, 200)

@app.route("/update_data/")
def update_data():
    data = {
        "z": value.sender_str,
        "a": value.trans_origin_str,
        "b": value.trans_target_str
    }
    return make_response(jsonify(data), 200)

@app.route("/image/")
def image():
    html_image_template = utils.get_html_image_template().replace("{image_url}", value.trans_image_url)
    return make_response(html_image_template, 200)

@app.route("/update_image_data/")
def update_image_data():
    if value.trans_image_url == "":
        utils.set_trans_image_url(config.EMOTION_IMAGE_URL + config.EMOTION_IMAGE_DEFAULT)
    data = {"image_url": value.trans_image_url}
    return make_response(jsonify(data), 200)

@app.route("/assets/<path:path>")
def assets(path):
    if path.startswith(f"{config.CONFIG_NAME}/images/"):
        if path == f"{config.CONFIG_NAME}/images/":
            file_path = os.path.join(os.getcwd(), "assets", path.split("/")[0:-1], config.EMOTION_IMAGE_DEFAULT)
            print(file_path)
            return send_file(file_path, mimetype="image/png")
        p = unquote(path)
        file_path = os.path.join(os.getcwd(), "assets", *p.split("/"))
        if os.path.isfile(file_path):
            print(file_path)
            return send_file(file_path, mimetype="image/png")
        else:
            file_path = os.path.join(os.getcwd(), *p.split("/")[0:-1], config.EMOTION_IMAGE_DEFAULT)
            print(file_path)
            return send_file(file_path, mimetype="image/png")
    else:
        return make_response("Not Found", 404)


def start_http_server():
    logging.getLogger('flask').setLevel(logging.FATAL)
    logging.getLogger('werkzeug').setLevel(logging.FATAL)
    utils.async_run(app.run(host=config.SERVER_HOST, port=config.SERVER_PORT))
