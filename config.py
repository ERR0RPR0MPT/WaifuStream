
import yaml
import sys


# 读取YAML文件
with open(sys.argv[1], 'r', encoding='utf-8') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        print("Please check your config file.")
        exit(1)

CONFIG_NAME = config['CONFIG_NAME']
CONFIG_MATCH_COMMAND = config['CONFIG_MATCH_COMMAND']
SHELL_TITLE = config['SHELL_TITLE']
SERVER_HOST = config['SERVER_HOST']
SERVER_PORT = config['SERVER_PORT']
SERVER_TRANSLATE_PROXY = config['SERVER_TRANSLATE_PROXY']
MODEL = config['MODEL']
BING_MAX_DIALOG_NUM = config['BING_MAX_DIALOG_NUM']
BING_CHAT_WS_URL = config['BING_CHAT_WS_URL']
AUTO_RESTART_ENABLE = config['AUTO_RESTART_ENABLE']
AUTO_RESTART_MINUTES = config['AUTO_RESTART_MINUTES']
BILI_ROOM_ID = config['BILI_ROOM_ID']
BILI_USER_UID = config['BILI_USER_UID']
BILI_ADMIN_USERS = config['BILI_ADMIN_USERS']
BILI_LIVE_AREA_ID = config['BILI_LIVE_AREA_ID']
BILI_KEEP_ALIVE_SECONDS = config['BILI_KEEP_ALIVE_SECONDS']
BILI_SESSDATA = config['BILI_SESSDATA']
BILI_JCT = config['BILI_JCT']
BILI_BUVID3 = config['BILI_BUVID3']
BILI_DEDEUSERID = config['BILI_DEDEUSERID']
OBS_ENABLE = config['OBS_ENABLE']
OBS_HOST = config['OBS_HOST']
OBS_PORT = config['OBS_PORT']
OBS_PASSWORD = config['OBS_PASSWORD']
STREAM_SCHEDULE = config['STREAM_SCHEDULE']
VTS_API_URL = config['VTS_API_URL']
AUTO_ANSWER_ENABLE = config['AUTO_ANSWER_ENABLE']
EMOTION_SIMULATION_ENABLE = config['EMOTION_SIMULATION_ENABLE']
EMOTION_SIMULATION_MODE = config['EMOTION_SIMULATION_MODE']
VITS_API_TYPE = config['VITS_API_TYPE']
TRANSLATE_LOG_STATE = config['TRANSLATE_LOG_STATE']
TRANSLATE_MODE = config['TRANSLATE_MODE']
TRANSLATE_TARGET_LANGUAGE = config['TRANSLATE_TARGET_LANGUAGE']
MAX_DANMAKU_QUEUE_LENGTH = config['MAX_DANMAKU_QUEUE_LENGTH']
MAX_INTERACT_MESSAGES_PER_MINUTE = config['MAX_INTERACT_MESSAGES_PER_MINUTE']
INTERACT_MESSAGES_RANDOM = config['INTERACT_MESSAGES_RANDOM']
MAX_WAIT_SECONDS = config['MAX_WAIT_SECONDS']
MAX_ANSWER_LENGTH = config['MAX_ANSWER_LENGTH']
MAX_CHAT_ANSWER_SECONDS = config['MAX_CHAT_ANSWER_SECONDS']
IGNORED_USERS = config['IGNORED_USERS']
EMOTION_IMAGE_URL = config['EMOTION_IMAGE_URL']
EMOTION_IMAGE_DEFAULT = config['EMOTION_IMAGE_DEFAULT']
TERMINAL_CHAT_NAME = config['TERMINAL_CHAT_NAME']
MULTI_MODE = config['MULTI_MODE']
MULTI_DIR = config['MULTI_DIR']
MULTI_ID = config['MULTI_ID']
MULTI_NAME = config['MULTI_NAME']
MULTI_MAX_STEPS = config['MULTI_MAX_STEPS']
MULTI_PROMPT = config['MULTI_PROMPT']
VITS_DOMAINS = config['VITS_DOMAINS']
OPENAI_API_KEY_LIST = config['OPENAI_API_KEY_LIST']
VITS_HEADER = config['VITS_HEADER']
VITS_PAYLOAD = config['VITS_PAYLOAD']
RANDOM_QUESTION = config['RANDOM_QUESTION']
USER = config['USER']
BOT = config['BOT']
SYSTEM_PROMPT = config['SYSTEM_PROMPT']
EMOTION_PROMPT = config['EMOTION_PROMPT']
WELCOME_PROMPT = config['WELCOME_PROMPT']
THANKS_FOR_GIFT_PROMPT = config['THANKS_FOR_GIFT_PROMPT']
TRANSLATE_PROMPT = config['TRANSLATE_PROMPT']
REQUEST_TOKEN_MSG = config['REQUEST_TOKEN_MSG']
SESSION_TOKEN_MSG = config['SESSION_TOKEN_MSG']
SEND_KEYS_MSG = config['SEND_KEYS_MSG']
TEXT_CHAT_RESET = config['TEXT_CHAT_RESET']
TEXT_MODEL_STYLE_CHANGED = config['TEXT_MODEL_STYLE_CHANGED']
TEXT_OPERATION_COMPLETED = config['TEXT_OPERATION_COMPLETED']
TEXT_DANMAKU_SAVED = config['TEXT_DANMAKU_SAVED']
TEXT_OPERATION_QUESTION = config['TEXT_OPERATION_QUESTION']
TEXT_OPERATION_RESET = config['TEXT_OPERATION_RESET']
TEXT_DANMAKU_SAVED_ALERT = config['TEXT_DANMAKU_SAVED_ALERT']
TEXT_THINKING = config['TEXT_THINKING']
TEXT_MAX_NUM_LIMITED = config['TEXT_MAX_NUM_LIMITED']
TEXT_RESTARTING = config['TEXT_RESTARTING']
TEXT_RESTARTING_FAILED = config['TEXT_RESTARTING_FAILED']
TEXT_IGNORE_DANMAKU = config['TEXT_IGNORE_DANMAKU']
TEXT_IGNORE_ROBOT = config['TEXT_IGNORE_ROBOT']
TEXT_IGNORE_USER = config['TEXT_IGNORE_USER']
TEXT_DELETE_EARLY_DANMAKU = config['TEXT_DELETE_EARLY_DANMAKU']
TEXT_QUEUE_LIMITED = config['TEXT_QUEUE_LIMITED']
TEXT_IS_NOT_MSG_ALERT = config['TEXT_IS_NOT_MSG_ALERT']
TEXT_QUEUE_SAME_MSG = config['TEXT_QUEUE_SAME_MSG']
TEXT_QUEUE_SAME_MSG_ALERT = config['TEXT_QUEUE_SAME_MSG_ALERT']
TEXT_RANDOM_QUESTION = config['TEXT_RANDOM_QUESTION']
TEXT_RESET_DIALOG = config['TEXT_RESET_DIALOG']
TEXT_RATE_LIMITED = config['TEXT_RATE_LIMITED']
TEXT_SYSTEM_TOKEN_LIMITED_ALERT = config['TEXT_SYSTEM_TOKEN_LIMITED_ALERT']
TEXT_RATE_LIMITED_ALERT = config['TEXT_RATE_LIMITED_ALERT']
TEXT_UNKNOWN_ERROR_ALERT = config['TEXT_UNKNOWN_ERROR_ALERT']
TEXT_SECOND = config['TEXT_SECOND']
TEXT_GPT_INFERENCE_TIME = config['TEXT_GPT_INFERENCE_TIME']
TEXT_VITS_INFERENCE_TIME = config['TEXT_VITS_INFERENCE_TIME']
TEXT_JAPANESE = config['TEXT_JAPANESE']
TEXT_CHINESE = config['TEXT_CHINESE']
EMOTION_KEYS_SHORTCUT_DICT = config['EMOTION_KEYS_SHORTCUT_DICT']
EMOTION_IMAGES_SHORTCUT_DICT = config['EMOTION_IMAGES_SHORTCUT_DICT']
FIX_TRANSLATE_ERROR_RULES = config['FIX_TRANSLATE_ERROR_RULES']
