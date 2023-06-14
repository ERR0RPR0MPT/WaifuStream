import base64
import json
import os
import random
import string
import tempfile
import time
import traceback
import playsound
import requests
import config
import utils
import value


def run_vits_and_play(trans_text, flag):
    payload_copy = config.VITS_PAYLOAD
    payload_copy["data"][0] = trans_text
    i = 0
    while i <= 3:
        i += 1
        try:
            vits_domain, vits_url, vits_download_url = utils.get_vits_link()
            # print(f"VITS Domain: {vits_domain}")
            response = requests.post(vits_url, headers=config.VITS_HEADER, data=json.dumps(payload_copy))
            if response.status_code == 200:
                vits_dir = ""
                if config.VITS_API_TYPE == 0:
                    # use vits-fast-fine-tuning-inference
                    vits_json = json.loads(response.content)
                    vits_web_dir = vits_json["data"][1]["name"]
                    vits_name = os.path.basename(vits_web_dir)
                    vits_urla = vits_download_url + vits_web_dir
                    vits_dir = os.path.join(tempfile.gettempdir(), vits_name)
                    r = requests.get(vits_urla)
                    with open(vits_dir, 'wb') as f:
                        f.write(r.content)
                elif config.VITS_API_TYPE == 1:
                    # use moetts-inference
                    vits_json = json.loads(response.content)
                    vits_data = vits_json["data"][1].split(",")[1]
                    vits_decoded_data = base64.b64decode(vits_data)
                    vits_dir = os.path.join(tempfile.gettempdir(),
                                            ''.join(random.choice(string.ascii_lowercase) for
                                                    _ in range(8)) + ".wav")
                    with open(vits_dir, "wb") as f:
                        f.write(vits_decoded_data)
                value.audio_queue[str(flag)] = vits_dir
                break
            else:
                print(f"Error while playing the audio: code={str(response.status_code)} content={response.content}")
                continue
        except:
            traceback.print_exc()
            print(f"Error while playing the audio")
            continue


def play_audio_queue():
    i = 0
    while True:
        try:
            if i == value.audio_threads_num or value.is_play_audio_timeout:
                value.audio_threads_num = 99999999
                break
            playsound.playsound(value.audio_queue[str(i)])
            i += 1
            time.sleep(0.2)
        except:
            time.sleep(0.2)
            continue
