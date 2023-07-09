import asyncio
import threading
from datetime import datetime
import os
import random
import sys
import time
from typing import Any
from bilibili_api import sync
import config
import danmaku
import multiprocess
import oa
import process
import schedule
import server
import value
import re
import websocket


def __ensure_event_loop() -> None:
    try:
        asyncio.get_event_loop()
    except:
        asyncio.set_event_loop(asyncio.new_event_loop())


def async_run(coroutine) -> Any:
    __ensure_event_loop()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)


def fix_emotion_keys(text):
    shortcut_pattern = r'\{.*?\}'
    shortcuts = re.findall(shortcut_pattern, text)
    shortcut_keys = [config.EMOTION_KEYS_SHORTCUT_DICT[s] for s in shortcuts if s in config.EMOTION_KEYS_SHORTCUT_DICT]
    return shortcut_keys


def fix_emotion_images(text):
    shortcut_pattern = r'\{.*?\}'
    shortcuts = re.findall(shortcut_pattern, text)
    shortcut_keys = [config.EMOTION_IMAGES_SHORTCUT_DICT[s] for s in shortcuts if
                     s in config.EMOTION_IMAGES_SHORTCUT_DICT]
    return shortcut_keys


def fix_translate_error(text):
    for pattern, replace_with in config.FIX_TRANSLATE_ERROR_RULES.items():
        text = re.sub(pattern, replace_with, text)
    return text


def is_cmd_or_msg(danmu_dict):
    if danmu_dict["text"].startswith(config.CONFIG_MATCH_COMMAND):
        return True
    return False


def get_dialog_today():
    return f"{config.CONFIG_NAME}_" + datetime.today().strftime('%Y%m%d') + '.txt'


def get_dialog_short_today():
    return f"{config.CONFIG_NAME}_" + datetime.today().strftime('%Y%m%d') + '_short.txt'


def get_vits_link():
    if value.vits_domain_index >= len(config.VITS_DOMAINS):
        value.vits_domain_index = 0
    vd = config.VITS_DOMAINS[value.vits_domain_index]
    value.vits_domain_index += 1
    return vd, f"https://{vd}/run/predict/", f"https://{vd}/file="


def is_valid_msg(msg):
    # 队列中同一用户id的消息数目不超过1条
    # if any(m["id"] == msg["id"] for m in msg_queue):
    # return False
    # 队列中含有相同的文字内容就不加入队列中
    # if any(m["text"] == msg["text"] for m in msg_queue):
    #     return False
    # 去除前缀进行检查
    msg_del_starts = msg["text"].replace(config.CONFIG_MATCH_COMMAND, "", 1)
    # 重启指令的管理员检测
    if msg["text"] == "+restart" or msg_del_starts == "+restart":
        if msg["id"] in config.BILI_ADMIN_USERS:
            danmaku.send_danmaku(config.TEXT_RESTARTING)
            restart()
            return False
        else:
            danmaku.send_danmaku(config.TEXT_RESTARTING_FAILED)
            return False
    # 检查是否为重置对话指令
    if msg["text"] == "+reset" or msg_del_starts == "+reset":
        value.chat_dict[msg["id"]] = oa.ChatGPT(config.SYSTEM_PROMPT)
        danmaku.send_danmaku("@" + msg["name"] + f" {config.TEXT_OPERATION_RESET}")
        return False
    # 检查对话开头是否匹配
    if not msg["text"].startswith(config.CONFIG_MATCH_COMMAND):
        return False
    # 如果队列中已经存在同一用户ID和相同消息内容的消息，则返回False。如果不存在，则返回True
    if any(m["id"] == msg["id"] and m["text"] == msg["text"] for m in value.msg_queue):
        return False
    return True


def save_short_dialog(msg):
    if not os.path.exists(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog")):
        os.makedirs(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog"))
    with open(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog", get_dialog_short_today()), "a",
              encoding="utf-8") as f:
        f.write(msg + "\n")


def save_dialog(msg):
    if not os.path.exists(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog")):
        os.makedirs(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog"))
    with open(os.path.join(os.getcwd(), "assets", config.CONFIG_NAME, "dialog", get_dialog_today()), "a",
              encoding="utf-8") as f:
        f.write(msg + "\n")


def set_model_style(model_style):
    i = 0
    while i <= 5:
        i += 1
        try:
            value.vts_ws.send(config.SESSION_TOKEN_MSG)
            value.vts_ws.recv()
            value.vts_ws.send(config.SEND_KEYS_MSG.replace("{hotkey}", model_style))
            break
        except:
            print("Failed to connect VTube Studio API. Retry...")
            init_ws()


def set_trans_image_url(url):
    value.trans_image_url = url
    print(f"Set emotion: {url.split('/')[-1]}")


def get_html_template():
    with open(f"./assets/{config.CONFIG_NAME}/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


def get_html_image_template():
    with open(f"./assets/{config.CONFIG_NAME}/templates/image.html", "r", encoding="utf-8") as f:
        return f.read()


def send_keys(lista):
    while True:
        for i in lista:
            if value.stop_event:
                return
            try:
                # print("Send Keys: " + i)
                i = i.split("+")
                value.vts_ws.send(config.SESSION_TOKEN_MSG)
                value.vts_ws.recv()
                value.vts_ws.send(config.SEND_KEYS_MSG.replace("{hotkey}", i[0]))
                time.sleep(int(i[1]))
            except:
                print("Failed to connect VTube Studio API. Retry...")
                init_ws()


def send_images(lista):
    j = 0
    while True:
        j += 1
        if j >= 4:
            return
        if value.stop_event:
            set_trans_image_url(config.EMOTION_IMAGE_URL + config.EMOTION_IMAGE_DEFAULT)
            return
        i = random.choice(lista)
        # print("Send Images: " + i)
        set_trans_image_url(config.EMOTION_IMAGE_URL + i)
        time.sleep(random.randint(6000, 10000) / 1000)


def init_ws():
    if config.EMOTION_SIMULATION_ENABLE and config.EMOTION_SIMULATION_MODE == "vts":
        while True:
            try:
                value.vts_ws = websocket.create_connection(config.VTS_API_URL)
                print("Connected to VTube Studio API.")
                break
            except:
                print("Failed to connect VTube Studio API.")
                time.sleep(5)
                print("Retry...")


def start_stream():
    print("Starting live...")
    sync(value.roomOp.start(config.BILI_LIVE_AREA_ID))
    if config.OBS_ENABLE:
        value.obswscl.start_stream()
    print("Success.")


def stop_stream():
    print("Stop live...")
    sync(value.roomOp.stop())
    if config.OBS_ENABLE:
        value.obswscl.stop_stream()
    print("Success.")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def restart():
    while True:
        try:
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except:
            print("重启失败，正在重试")
            continue


def auto_restart():
    if config.AUTO_RESTART_ENABLE:
        time.sleep(config.AUTO_RESTART_MINUTES * 60)
        print("Auto restart...")
        threading.Thread(target=restart).start()


def main_init():
    init_ws()
    threading.Thread(target=process.execute).start()
    threading.Thread(target=multiprocess.multiprocess).start()
    threading.Thread(target=server.start_http_server).start()
    threading.Thread(target=danmaku.init_danmaku).start()
    threading.Thread(target=auto_restart).start()
    threading.Thread(target=schedule.schedule).start()
