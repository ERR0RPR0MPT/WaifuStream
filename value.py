
from bilibili_api import live
from bilibili_api import Credential
from pygtrans import Translate
import obsws_python as obs
import config

sender_str = ""
trans_origin_str = ""
trans_target_str = ""
trans_emotion_data = ""
trans_image_url = ""
msg_queue = []
audio_queue = {}
audio_threads_queue = {}
vits_domain_index = 0
audio_threads_num = 99999999
interact_last_append_time = 0
interact_messages_appended = 0
chat_dict = {}
stop_event = False
is_play_audio_timeout = False
vts_ws = None
client = Translate(proxies=config.SERVER_TRANSLATE_PROXY)
obswscl = obs.ReqClient(host=config.OBS_HOST, port=config.OBS_PORT, password=config.OBS_PASSWORD)
credential = Credential(sessdata=config.BILI_SESSDATA, bili_jct=config.BILI_JCT, buvid3=config.BILI_BUVID3, dedeuserid=config.BILI_DEDEUSERID)
roomOp = live.LiveRoom(config.BILI_ROOM_ID, credential=credential)
room = live.LiveDanmaku(config.BILI_ROOM_ID, credential=credential, max_retry=999999999)
