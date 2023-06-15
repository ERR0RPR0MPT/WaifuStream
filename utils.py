from datetime import datetime
import os
import random
import sys
import time
import config
import danmaku
import nlp
import value
import re
import websocket


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
    if danmu_dict["text"].startswith(("+", "#")):
        return True
    return False


def restart():
    # 检查权限
    python = sys.executable
    os.execl(python, python, *sys.argv)


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
        value.chat_dict[msg["id"]] = nlp.ChatGPT(config.SYSTEM_PROMPT)
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


def hide_openai_api_key(api_key):
    try:
        return api_key[:8] + "*" * (len(api_key) - len(api_key[:8]) - len(api_key[-6:])) + api_key[-6:]
    except:
        return ""


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
    while True:
        for i in lista:
            if value.stop_event:
                set_trans_image_url(config.EMOTION_IMAGE_URL + config.EMOTION_IMAGE_DEFAULT)
                return
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


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
