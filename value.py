import threading
from bilibili_api import live
from pygtrans import Translate
import config

sender_str = ""
trans_origin_str = ""
trans_target_str = ""
trans_emotion_data = ""
trans_image_url = ""
html_template = open(f"./assets/{config.CONFIG_NAME}/templates/index.html", "r", encoding="utf-8").read()
html_image_template = open(f"./assets/{config.CONFIG_NAME}/templates/image.html", "r", encoding="utf-8").read()
openai_api_current_key = ""
msg_queue = []
audio_queue = {}
audio_threads_queue = {}
vits_domain_index = 0
audio_threads_num = 99999999
interact_last_append_time = 0
interact_messages_appended = 0
audio_lock = threading.Lock()
chat_dict = {}
stop_event = False
is_play_audio_timeout = False
vts_ws = None
room = live.LiveDanmaku(config.BILI_ROOM_ID)
client = Translate(proxies=config.SERVER_TRANSLATE_PROXY)
