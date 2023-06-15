from urllib.parse import unquote
import json
import logging
import os
import socketserver

import utils
import value
import config
import http.server


class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, formats, *args):
        return

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                value.html_template.replace("{z}", value.sender_str).replace("{a}", value.trans_origin_str).replace(
                    "{b}",
                    value.trans_target_str).encode(
                    encoding="utf-8"))
        elif self.path == "/update_data/":
            data = {
                "z": value.sender_str,
                "a": value.trans_origin_str,
                "b": value.trans_target_str
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/image/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(value.html_image_template.replace("{image_url}", value.trans_image_url).encode(encoding="utf-8"))
        elif self.path == "/update_image_data/":
            if value.trans_image_url == "":
                utils.set_trans_image_url(config.EMOTION_IMAGE_URL + config.EMOTION_IMAGE_DEFAULT)
            data = {"image_url": value.trans_image_url}
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path.startswith(f"/assets/{config.CONFIG_NAME}/images/"):
            if self.path == f"/assets/{config.CONFIG_NAME}/images/":
                file_path = os.path.join(os.getcwd(), *self.path.split("/")[0:-1], config.EMOTION_IMAGE_DEFAULT)
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            p = unquote(self.path)
            file_path = os.path.join(os.getcwd(), *p.split("/"))
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                file_path = os.path.join(os.getcwd(), *p.split("/")[0:-1], config.EMOTION_IMAGE_DEFAULT)
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
        else:
            self.send_error(404)

class ThreadHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def start_http_server():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    with ThreadHTTPServer(("", config.SERVER_PORT), MyRequestHandler) as server:
        if not config.TRANSLATE_LOG_STATE:
            server.RequestHandlerClass.log_request = lambda *args, **kwargs: None
        server.serve_forever()
