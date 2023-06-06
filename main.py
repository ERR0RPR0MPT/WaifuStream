from config import *
from blive.msg import DanMuMsg
from googletrans import Translator
from collections import defaultdict
from datetime import datetime, timedelta
from blive import BLiver, Events, BLiverCtx
import os
import json
import time
import openai
import random
import logging
import requests
import tempfile
import playsound
import traceback
import threading
import http.server
import socketserver

sender_str = ""
trans_origin_str = ""
trans_target_str = ""
html_template = ""
openai_api_current_key = ""
msg_queue = []
app = BLiver(ROOM_ID)
translator = Translator(service_urls=['translate.google.com', ])
dialog_today = datetime.today().strftime('%Y%m%d') + '.txt'
with open(os.path.join(os.getcwd(), "templates", "index.html"), "r", encoding="utf-8") as file:
    html_template = file.read()


def is_valid_msg(msg):
    # 队列中同一用户id的消息数目不超过1条
    if any(m["id"] == msg["id"] for m in msg_queue):
        return False
    # 队列中含有相同的文字内容就不加入队列中
    if any(m["text"] == msg["text"] for m in msg_queue):
        return False
    return True


def save_dialog(msg):
    with open(os.path.join(os.getcwd(), "dialog", dialog_today), "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def send_danmaku_origin(msg):
    bili_danmaku_send_data_temp = bili_danmaku_send_data
    bili_danmaku_send_data_temp["msg"] = msg
    requests.post(url=bili_danmaku_send_url, data=bili_danmaku_send_data_temp,
                  headers=bili_danmaku_send_header)


def send_danmaku(msg):
    threading.Thread(target=send_danmaku_origin, args=(msg,)).start()


@app.on(Events.DANMU_MSG)
async def listen_danmu(ctx: BLiverCtx):
    danmu = DanMuMsg(ctx.body)

    danmu_dict = {
        "text": danmu.content,
        "id": str(danmu.sender.id),
        "name": danmu.sender.name,
        "timestamp": str(time.time()),
    }

    # 避免机器人发送的弹幕被检测到
    if danmu_dict["id"] == str(BILI_UID) and (
            "弹幕被丢弃" in danmu_dict["text"] or "弹幕已保存" in danmu_dict["text"] or "思考中~" in danmu_dict["text"]):
        print("弹幕被丢弃(忽略机器人弹幕): text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict["name"])
        return

    # 指定忽略的用户
    if danmu_dict["id"] in IGNORED_USERS:
        print("弹幕被丢弃(用户被忽略): text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict["name"])
        return

    if is_valid_msg(danmu_dict):
        while len(msg_queue) >= MAX_DANMAKU_QUEUE_LENGTH and time.time() - msg_queue[0] > 60:
            msg_temp = msg_queue.pop(0)
            print("弹幕被丢弃(删除最早的弹幕): text=" + msg_temp["text"] + " id=" + msg_temp["id"] + " name=" + msg_temp["name"])
            send_danmaku("弹幕被丢弃：队列超限，请尝试重新发送")
        msg_queue.append(danmu_dict)
        print("弹幕已保存: text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict[
            "name"])
        send_danmaku("弹幕已保存，请在直播中等待亚托莉的回复~")
    else:
        print("弹幕被丢弃(队列中已存在相同的用户id或消息): text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict[
            "name"])
        send_danmaku("弹幕被丢弃：队列中已存在相同的ID/消息")


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(html_template.replace("{z}", sender_str).replace("{a}", trans_origin_str).replace("{b}",
                                                                                                               trans_target_str).encode(
                encoding="utf-8"))
        elif self.path == "/update_data/":
            data = {
                "z": sender_str,
                "a": trans_origin_str,
                "b": trans_target_str
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_error(404)


def start_http_server():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    with socketserver.TCPServer(("", TRANSLATE_PORT), MyRequestHandler) as server:
        if not TRANSLATE_LOG_STATE:
            server.RequestHandlerClass.log_request = lambda *args, **kwargs: None
        server.serve_forever()


def get_random_key():
    while True:
        new_key = random.choice(OPENAI_API_KEY_LIST)
        if new_key != openai_api_current_key or len(OPENAI_API_KEY_LIST) == 1:
            return new_key


class ChatGPT:
    def __init__(self):
        self.user = user
        self.messages = [{"role": "system", "content": system_prompt}]

    def ask_gpt(self):
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]


openai_api_current_key = get_random_key()
openai.api_key = openai_api_current_key
chat = ChatGPT()


def on_gpt_msg(q):
    global chat

    if q == "+reset":
        chat = ChatGPT()
        return "Chat Reset."

    # # 限制对话次数
    # if len(chat.messages) > 15:
    #     chat = ChatGPT()

    # 提问-回答-记录
    chat.messages.append({"role": "user", "content": q})
    answer = chat.ask_gpt()
    chat.messages.append({"role": "assistant", "content": answer})
    return answer


def execute():
    is_first_run = True
    while True:
        try:
            if is_first_run:
                is_first_run = False
                print("----------------------------------")
                print("Translate Server started at http://localhost:8004")
                print(f"Listening danmaku on room id: {ROOM_ID}")
            choice_flag = 0
            while True:
                if choice_flag <= MAX_WAIT_SECONDS:
                    if len(msg_queue) <= 0:
                        choice_flag += 1
                        time.sleep(1)
                        continue
                    choice_flag = 0
                    danmu = msg_queue.pop(0)
                    msg = danmu["text"]
                    ide = danmu["id"]
                    name = danmu["name"]
                    timestamp = danmu["timestamp"]
                else:
                    choice_flag = 0
                    msg = random.choice(random_question)
                    ide = "0"
                    name = "随机问答"
                    timestamp = str(time.time())

                if len(msg.strip()) > 0:
                    log = f"Received: id={ide},name={name},content={msg},time={timestamp}"
                    try:
                        if not os.path.isfile("logs.txt"):
                            with open("logs.txt", "w") as f:
                                f.write(log + "\n")
                        else:
                            with open("logs.txt", "a+") as f:
                                f.write(log + "\n")
                        print(log)
                    except:
                        print("Failed to write log.")

                    print(f"Input: {msg}")
                    save_dialog(f"Question: {msg}")
                    global sender_str
                    sender_str = f"{name}: {msg} -> Inferencing..."
                    start_time = time.time()
                    print("Inferencing...")
                    retries = 0
                    is_failed = False
                    global openai_api_current_key
                    global chat
                    while True:
                        retries += 1
                        try:
                            data = on_gpt_msg(msg)
                            break
                        except openai.error.AuthenticationError as e:
                            print("Try to set a key...")
                            openai_api_current_key = get_random_key()
                            openai.api_key = openai_api_current_key
                            chat = ChatGPT()
                            continue
                        except openai.error.InvalidRequestError as e:
                            traceback.print_exc()
                            print("Token has been limited. Try to recovery...")
                            sender_str = "重置对话 -> " + sender_str
                            chat = ChatGPT()
                            continue
                        except openai.error.RateLimitError as e:
                            print("Rate has been limited. Try to recovery...")
                            sender_str = "速率限制，请稍等 -> " + sender_str
                            if retries >= 3:
                                time.sleep(10)
                            openai_api_current_key = get_random_key()
                            openai.api_key = openai_api_current_key
                            continue
                        except:
                            traceback.print_exc()
                            print("Error")
                            is_failed = True
                            break
                    if is_failed:
                        break
                    end_time = time.time()
                    print(
                        f"Used API Key：index={str(OPENAI_API_KEY_LIST.index(openai_api_current_key) + 1)} -> " + openai_api_current_key[
                                                                                                                 :8] + "*" * (
                                len(openai_api_current_key) - len(openai_api_current_key[:8]) - len(openai_api_current_key[-6:])) + openai_api_current_key[-6:])
                    print("LLM 推理时间为：{}秒".format(round(end_time - start_time, 2)))
                    time_sticker_str = f" LLM推理:{str(round(end_time - start_time, 2))}秒 "

                    payload_copy = vits_payload
                    i = 0
                    while True:
                        try:
                            sender_str = f"{name}: {msg} -> Translating..."
                            print(f"GPT Original Output: {data}")
                            save_dialog(f"GPT Original Output: {data}")
                            trans = translator.translate(data, src='auto', dest='ja')
                            trans_origin = trans.origin
                            trans_text = trans.text
                            payload_copy["data"][2] = "日本語"
                            break
                        except:
                            traceback.print_exc()
                            i += 1
                            print("Error: translation failed, try other ways.")
                            if i < 3:
                                time.sleep(1)
                                continue
                            print("Using original text...")
                            trans_origin = data
                            trans_text = data
                            payload_copy["data"][2] = "简体中文"
                            break

                    # 翻译人工修正
                    trans_text = fix_translate_error(trans_text)

                    global trans_origin_str
                    global trans_target_str
                    trans_origin_str = trans_origin
                    trans_target_str = trans_text

                    print(f"Original = {trans_origin_str}\nTarget = {trans_target_str}")
                    save_dialog(f"Original = {trans_origin_str}\nTarget = {trans_target_str}\n")

                    # 发送弹幕
                    if ide != "0":
                        send_danmaku(f"@{name} 思考中~")

                    print("VITS Running...")
                    sender_str = sender_str.replace("Translating...", "VITS Running...")
                    start_time = time.time()
                    payload_copy["data"][0] = trans_text
                    response = requests.post(vits_url, headers=vits_headers, data=json.dumps(payload_copy))
                    if response.status_code == 200:
                        vits_json = json.loads(response.content)
                        vits_dir = vits_json["data"][1]["name"]
                        if not os.path.exists(vits_dir):
                            try:
                                # 检测到文件下载
                                print("Downloading...")
                                temp_path = os.path.join(tempfile.gettempdir(), os.path.basename(vits_dir))
                                response = requests.get(f"{vits_download_url}{vits_dir}")
                                with open(temp_path, 'wb') as f:
                                    f.write(response.content)
                                vits_dir = temp_path
                                print("OK.")
                            except:
                                traceback.print_exc()
                                print("Error: Download failed.")
                                continue
                        end_time = time.time()
                        print("VITS 推理时间为：{}秒".format(round(end_time - start_time, 2)))
                        time_sticker_str += f"VITS推理:{str(round(end_time - start_time, 2))}秒"
                        print("Start Play...")
                        sender_str = sender_str.replace(" -> VITS Running...", "") + time_sticker_str
                        playsound.playsound(vits_dir)
                        print("Finished.")
                    else:
                        print("Error while playing the audio")
                        continue
                    print("\n----------------------------------")
                else:
                    print('Error: Empty Message.')
        except:
            traceback.print_exc()
            print("Error")
            time.sleep(3)
            print("Retry...")
            continue


if __name__ == '__main__':
    threading.Thread(target=execute).start()
    threading.Thread(target=start_http_server).start()
    app.run()
