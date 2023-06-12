from config import *
from blive.msg import DanMuMsg
from googletrans import Translator
from collections import defaultdict
from datetime import datetime, timedelta
from blive import BLiver, Events, BLiverCtx
import concurrent.futures
import os
import re
import json
import time
import base64
import openai
import random
import string
import logging
import requests
import tempfile
import playsound
import pyautogui
import traceback
import threading
import websocket
import http.server
import socketserver

sender_str = ""
trans_origin_str = ""
trans_target_str = ""
trans_emotion_data = ""
html_template = ""
openai_api_current_key = ""
msg_queue = []
audio_queue = {}
audio_threads_queue = {}
audio_threads_num = 99999999
audio_lock = threading.Lock()
chat_dict = {}
stop_event = False
vts_ws = None
app = BLiver(ROOM_ID)
translator = Translator(service_urls=['translate.google.com', ])
dialog_today = datetime.today().strftime('%Y%m%d') + '.txt'
dialog_short_today = datetime.today().strftime('%Y%m%d') + '_short.txt'
with open(os.path.join(os.getcwd(), "templates", "index.html"), "r", encoding="utf-8") as file:
    html_template = file.read()


def is_valid_msg(msg):
    # 队列中同一用户id的消息数目不超过1条
    # if any(m["id"] == msg["id"] for m in msg_queue):
    # return False
    # 队列中含有相同的文字内容就不加入队列中
    # if any(m["text"] == msg["text"] for m in msg_queue):
    #     return False
    # 如果队列中已经存在同一用户ID和相同消息内容的消息，则返回False。如果不存在，则返回True
    if any(m["id"] == msg["id"] and m["text"] == msg["text"] for m in msg_queue):
        return False
    return True


def save_short_dialog(msg):
    if not os.path.exists('dialog'):
        os.makedirs('dialog')
    with open(os.path.join(os.getcwd(), "dialog", dialog_short_today), "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def save_dialog(msg):
    if not os.path.exists('dialog'):
        os.makedirs('dialog')
    with open(os.path.join(os.getcwd(), "dialog", dialog_today), "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def send_danmaku_origin(msg):
    bili_danmaku_send_data_temp = bili_danmaku_send_data
    bili_danmaku_send_data_temp["msg"] = msg
    r = requests.post(url=bili_danmaku_send_url, data=bili_danmaku_send_data_temp,
                      headers=bili_danmaku_send_header)
    if r.status_code != 200:
        print("发送弹幕失败，错误码：" + str(r.status_code) + "，错误信息：" + r.text)


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
            TEXT_IGNORE_DANMAKU in danmu_dict["text"] or TEXT_DANMAKU_SAVED in danmu_dict["text"] or TEXT_THINKING in
            danmu_dict["text"]):
        print(TEXT_IGNORE_DANMAKU + "(" + TEXT_IGNORE_ROBOT + "): text=" + danmu_dict["text"] + " id=" + danmu_dict[
            "id"] + " name=" + danmu_dict["name"])
        return

    # 指定忽略的用户
    if danmu_dict["id"] in IGNORED_USERS:
        print(TEXT_IGNORE_DANMAKU + "(" + TEXT_IGNORE_USER + "): text=" + danmu_dict["text"] + " id=" + danmu_dict[
            "id"] + " name=" + danmu_dict["name"])
        return

    # 弹幕是否合法
    if is_valid_msg(danmu_dict):
        while len(msg_queue) >= MAX_DANMAKU_QUEUE_LENGTH and time.time() - msg_queue[0] > 60:
            msg_temp = msg_queue.pop(0)
            print(TEXT_IGNORE_DANMAKU + "(" + TEXT_DELETE_EARLY_DANMAKU + "): text=" + msg_temp["text"] + " id=" +
                  msg_temp["id"] + " name=" + msg_temp["name"])
            send_danmaku(f"{TEXT_IGNORE_DANMAKU}: {TEXT_QUEUE_LIMITED}")

        # 检测是否为聊天信息或指令
        if not is_cmd_or_msg(danmu_dict):
            print(TEXT_IGNORE_DANMAKU + "(" + TEXT_IS_NOT_MSG_ALERT + "): text=" + danmu_dict["text"] + " id=" +
                  danmu_dict["id"] + " name=" + danmu_dict["name"])
            return
        msg_queue.append(danmu_dict)
        print(TEXT_DANMAKU_SAVED + ": text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict[
            "name"])
        send_danmaku(TEXT_DANMAKU_SAVED_ALERT)
    else:
        print(TEXT_IGNORE_DANMAKU + "(" + TEXT_QUEUE_SAME_MSG + "): text=" + danmu_dict["text"] + " id=" + danmu_dict[
            "id"] + " name=" + danmu_dict[
                  "name"])
        send_danmaku(TEXT_QUEUE_SAME_MSG_ALERT)


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
            messages=self.messages,
            stream=True
        )
        # return rsp.get("choices")[0]["message"]["content"]
        # 流式输出
        return rsp

    def ask_gpt_get(self):
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        return rsp.get("choices")[0]["message"]["content"]


openai_api_current_key = get_random_key()
openai.api_key = openai_api_current_key


def on_gpt_msg(q, ide, name):
    try:
        chat_dict[ide]
    except:
        chat_dict[ide] = ChatGPT()

    if q == "+reset":
        chat_dict[ide] = ChatGPT()
        send_danmaku(f"@{name} {TEXT_OPERATION_RESET}")
        return TEXT_RESET_CHAT

    # if q[0] == "+":
    #     # 切换模型样式
    #     model_style = q.replace("+", "")
    #     set_model_style(model_style)
    #     q = TEXT_OPERATION_QUESTION.replace("{style}", model_style)

    q = q.replace("#", "", 1)

    # # 限制对话次数
    # if len(chat.messages) > 15:
    #     chat = ChatGPT()##

    # 发送弹幕
    if ide != "0":
        send_danmaku(f"@{name} {TEXT_THINKING}")

    global sender_str
    global stop_event
    sender_str = f"{name}: {q} -> Inferencing..."
    stop_event = False

    # 提问-回答-记录
    chat_dict[ide].messages.append({"role": "user", "content": q})
    answer_rsp = chat_dict[ide].ask_gpt()
    answer = ""
    # 流式输出
    global trans_origin_str
    global trans_target_str
    global trans_emotion_data
    global audio_queue
    global audio_threads_queue
    global audio_threads_num
    trans_origin_str = ""
    trans_target_str = ""
    trans_emotion_data = ""
    audio_queue = {}
    audio_threads_queue = {}
    audio_threads_num = 99999999
    i = 0
    sentences_num = 0
    sentences_detect = False
    t1 = threading.Thread(target=play_audio_queue)
    t1.start()
    t_emo = None

    for chunk in answer_rsp:
        try:
            now_token = chunk.choices[0].delta.to_dict()["content"]
            answer += now_token
            trans_origin_str = answer
            # 检测是否成功输出一句话
            if any(char in now_token for char in '，。：？！,.:?!~'):
                try:
                    sentences_num += 1
                    # if sentences_num == 3:
                    #     # 识别感情
                    #     sentences_detect = True
                    #     t_emo = threading.Thread(target=emotion_analysis_init, args=(answer,))
                    #     t_emo.start()
                    # 提取最后一句话
                    tokens = re.split('(?<=[，。：？！,.:?!~])', answer)
                    tokens = [token.strip() for token in tokens if token.strip()]
                    partial_answer = tokens[-1]
                    # 调用翻译
                    k = 0
                    while True:
                        try:
                            trans = translator.translate(partial_answer, src='auto', dest='ja')
                            trans_text = trans.text
                            break
                        except:
                            traceback.print_exc()
                            k += 1
                            print("Error: translation failed, try other ways.")
                            if k < 3:
                                time.sleep(0.2)
                                continue
                            print("Using original text...")
                            trans_text = partial_answer
                            break
                    # 翻译人工修正
                    trans_text = fix_translate_error(trans_text)
                    # 更新UI
                    trans_target_str += trans_text
                    # 运行VITS推理
                    t = threading.Thread(target=run_vits_and_play, args=(trans_text, i))
                    t.start()
                    audio_threads_queue[str(i)] = t
                    i += 1
                except:
                    traceback.print_exc()
                    continue
        except:
            continue

    # 感情检测
    # if not sentences_detect:
    #     t_emo = threading.Thread(target=emotion_analysis_init, args=(answer,))
    #     t_emo.start()
    # t_emo.join()

    print(f"GPT Original Output: {answer}")
    save_dialog(f"GPT Original Output: {answer}")
    print(f"GPT Emotional Output: {trans_emotion_data}")
    save_dialog(f"GPT Emotional Output: {trans_emotion_data}")
    print(f"Original = {trans_origin_str}\nTarget = {trans_target_str}")
    save_dialog(f"Original = {trans_origin_str}\nTarget = {trans_target_str}\n")
    save_short_dialog(f"A: {trans_origin_str}\n\n")
    sender_str = f"{name}: {q} -> Playing"

    # 等待模型音频完毕
    for _, v in audio_threads_queue.items():
        v.join()
    audio_threads_num = len(audio_threads_queue)
    t1.join()

    stop_event = True
    audio_queue = {}
    audio_threads_queue = {}
    chat_dict[ide].messages.append({"role": "assistant", "content": answer})

    sender_str = f"{name}: {q} -> Finished"
    return answer


def run_vits_and_play(trans_text, flag):
    payload_copy = vits_payload
    payload_copy["data"][0] = trans_text
    response = requests.post(vits_url, headers=vits_headers, data=json.dumps(payload_copy))
    i = 0
    while i <= 3:
        i += 1
        if response.status_code == 200:
            # vits_json = json.loads(response.content)
            # vits_data = vits_json["data"][1].split(",")[1]
            # vits_decoded_data = base64.b64decode(vits_data)
            # vits_dir = os.path.join(tempfile.gettempdir(),
            #                         ''.join(random.choice(string.ascii_lowercase) for
            #                                 _ in range(8)) + ".wav")
            # with open(vits_dir, "wb") as f:
            #     f.write(vits_decoded_data)
            vits_json = json.loads(response.content)
            vits_web_dir = vits_json["data"][1]["name"]
            vits_name = os.path.basename(vits_web_dir)
            vits_urla = vits_download_url + vits_web_dir
            vits_dir = os.path.join(tempfile.gettempdir(), vits_name)
            r = requests.get(vits_urla)
            with open(vits_dir, 'wb') as f:
                f.write(r.content)
            global audio_queue
            audio_queue[str(flag)] = vits_dir
            break
        else:
            print(response.status_code)
            print("Error while playing the audio")
            continue


def play_audio_queue():
    i = 0
    global audio_threads_num
    while True:
        try:
            if i == audio_threads_num:
                audio_threads_num = 99999999
                break
            playsound.playsound(audio_queue[str(i)])
            i += 1
            time.sleep(0.2)
        except:
            time.sleep(0.2)
            continue


def emotion_analysis(msg):
    emotion_temp = ChatGPT()
    emotion_temp.messages.append({"role": "user", "content": emotion_prompt.replace("{emotion_phrase}", msg)})
    emotion_data = emotion_temp.ask_gpt_get()
    return emotion_data


def emotion_analysis_init(answer):
    emotion_data = emotion_analysis(answer)
    global trans_emotion_data
    trans_emotion_data = emotion_data
    emotion_keys = fix_emotion_keys(emotion_data)
    threading.Thread(target=send_keys, args=(emotion_keys,)).start()


def set_model_style(model_style):
    i = 0
    while i <= 5:
        i += 1
        try:
            vts_ws.send(session_vaild_msg)
            vts_ws.recv()
            vts_ws.send(send_keys_msg.replace("{hotkey}", model_style))
            break
        except:
            print("Failed to connect VTube Studio API. Retry...")
            init_ws()


def send_keys(lista):
    global stop_event
    while True:
        for i in lista:
            if stop_event:
                return
            try:
                print("Send Keys: " + i)
                i = i.split("+")
                vts_ws.send(session_vaild_msg)
                vts_ws.recv()
                vts_ws.send(send_keys_msg.replace("{hotkey}", i[0]))
                time.sleep(int(i[1]))
            except:
                print("Failed to connect VTube Studio API. Retry...")
                init_ws()


def init_ws():
    while True:
        try:
            global vts_ws
            vts_ws = websocket.create_connection(VTS_API_URL)
            print("Connected to VTube Studio API.")
            break
        except:
            print("Failed to connect VTube Studio API.")
            time.sleep(5)
            print("Retry...")


# def play_audio():
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), AUDIO_DIR_NAME)
#     for filename in os.listdir(path):
#         file_path = os.path.join(path, filename)
#         if os.path.isfile(file_path):
#             print(f"Playing {os.path.basename(file_path)}")
#             playsound.playsound(file_path)


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
                    name = TEXT_RANDOM_QUESTION
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
                    save_dialog("ID=" + ide + " Name=" + name)
                    save_dialog(f"Question: {msg}")
                    save_short_dialog(f"Q: {msg}")
                    global sender_str
                    sender_str = f"{name}: {msg} -> Inferencing..."
                    start_time = time.time()
                    print("Inferencing...")
                    retries = 0
                    is_failed = False
                    emotion_data = ""
                    global openai_api_current_key
                    while True:
                        retries += 1
                        try:
                            data = on_gpt_msg(msg, ide, name)
                            break
                        except openai.error.AuthenticationError as e:
                            print("OpenAI AuthenticationError, Try to set a key...")
                            openai_api_current_key = get_random_key()
                            openai.api_key = openai_api_current_key
                            continue
                        except openai.error.InvalidRequestError as e:
                            print("Token has been limited. Try to recovery...")
                            if not TEXT_RESET_DIALOG in sender_str:
                                sender_str = TEXT_RESET_DIALOG + " -> " + sender_str
                            if retries >= 2:
                                data = TEXT_SYSTEM_TOKEN_LIMITED_ALERT
                                emotion_data = ""
                                break
                            chat_dict[ide] = ChatGPT()
                            continue
                        except openai.error.RateLimitError as e:
                            print("Rate has been limited. Try to recovery...")
                            if not TEXT_RATE_LIMITED in sender_str:
                                sender_str = TEXT_RATE_LIMITED + " -> " + sender_str
                            if retries >= 3:
                                time.sleep(10)
                            if retries >= 5:
                                data = TEXT_RATE_LIMITED_ALERT
                                emotion_data = ""
                                break
                            openai_api_current_key = get_random_key()
                            openai.api_key = openai_api_current_key
                            continue
                        except:
                            traceback.print_exc()
                            print("Error")
                            data = TEXT_UNKNOWN_ERROR_ALERT
                            emotion_data = ""
                            break
                    end_time = time.time()
                    print(
                        f"Used API Key：index={str(OPENAI_API_KEY_LIST.index(openai_api_current_key) + 1)} -> " + openai_api_current_key[
                                                                                                                 :8] + "*" * (
                                len(openai_api_current_key) - len(openai_api_current_key[:8]) - len(
                            openai_api_current_key[-6:])) + openai_api_current_key[-6:])
                    print(TEXT_GPT_INFERENCE_TIME + " {}".format(round(end_time - start_time, 2)) + TEXT_SECOND)
                else:
                    print('Error: Empty Message.')
                print("Finished.\n----------------------------------")
        except:
            traceback.print_exc()
            print("Error")
            time.sleep(3)
            print("Retry...")
            continue


if __name__ == '__main__':
    # init_ws()
    threading.Thread(target=execute).start()
    threading.Thread(target=start_http_server).start()
    # threading.Thread(target=play_audio).start()
    app.run()
