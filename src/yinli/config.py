ROOM_ID = 0
BILI_UID = 0
RWKV_HOST = '127.0.0.1'
RWKV_PORT = 9006
# VITS_HOST = '127.0.0.1'
# VITS_PORT = 7860
VITS_DOMAIN = ""
# VTS_API_URL = "ws://localhost:8001"
# AUDIO_DIR_NAME = "audio"
TRANSLATE_PORT = 8004
TRANSLATE_LOG_STATE = False
MAX_DANMAKU_QUEUE_LENGTH = 10
MAX_WAIT_SECONDS = 600
IGNORED_USERS = []
OPENAI_API_KEY_LIST = [
    "",
]

# vits_url = f"http://{VITS_HOST}:{VITS_PORT}/run/predict/"
vits_url = f"https://{VITS_DOMAIN}/run/predict/"
vits_download_url = f"https://{VITS_DOMAIN}/file="

vits_headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
}
vits_payload = {
    "fn_index": 0,
    "data": ["Test", "yinli", "日本語", 1],
    "session_hash": "abcdefghhij"
}

# vits_headers = {
#     "Content-Type": "application/json",
#     "Accept": "*/*",
# }
#
# vits_payload = {
#     "fn_index": 29,
#     "data": [
#         "こんにちは。",
#         "yinli",
#         1,
#         False
#     ],
#     "session_hash": "abcdefghhij"
# }

bili_danmaku_send_url = "https://api.live.bilibili.com/msg/send"

bili_danmaku_send_data = {
    'bubble': '0',
    'msg': '',
    'color': '16777215',
    'mode': '1',
    'room_type': '0',
    'jumpfrom': '0',
    'fontsize': '25',
    'rnd': '',
    'roomid': '',
    'csrf': '',
    'csrf_token': '',
}

bili_danmaku_send_header = {
    'Cookie': "",
    'Origin': 'https://live.bilibili.com',
    'Referer': 'https://live.bilibili.com/1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

random_question = [
    "音理，你认为动画师这个职业有前途吗？",
    "音理，如果你可以做任何工作，你想做什么？",
    "音理，你觉得星空列车旅行中最让你难忘的时刻是什么？",
    "音理，你对狩叶这个乘务员印象如何？",
    "音理，你觉得野鸟、花江和鹰世三位乘客哪个最让你印象深刻？",
    "音理，你也可以像诺瓦那样拥有猫耳吗？",
    "音理，你认为真白的改变是好事还是坏事？",
    "音理，如果你有机会选择一位乘客和自己一起继续旅行，你会选择谁？",
    "音理，你觉得星空列车旅行的故事对你的人生有什么启示或影响？",
    "音理，你心目中理想的未来是什么样子？",
    "音理，我们在第二站海边的时候我画了一张诺瓦的肖像画，那时你的心情怎样？",
    "音理，我们在第三站函馆市的天文博物馆附近遇到了白化少女真白，你觉得她的出现代表着什么？",
    "音理，每个人都有自己的梦想，你觉得你的梦想是什么？",
    "音理，在旅行的最后阶段，你是否有任何遗憾？",
    "音理，如果以后我们再次有机会一起旅行，你想去哪里？",
    "音理，你觉得我们旅行的第一站瑞典森林最美的地方在哪里？",
    "音理，音理，你觉得我还能够继续我的动画梦吗？我一直很迷茫。",
    "音理，为什么你要邀请我一起参加星空列车旅行呢？是因为想让我开心吗？",
    "音理，在星空列车旅行中，你觉得我最大的优点是什么？",
    "音理，如果有机会重新来一次这样的旅行，你还会选择这样做吗？",
]

user = "晓"
bot = "音理"

system_prompt = """
本材料用于模拟《星空列车与白的旅行》游戏中晓与音理的对话
剧情如下:
钟城晓的经历：
晓为了成为动画师，从岩手县搬到东京工作。但几年前他担任的一部动画因其他职位失误导致作画崩坏，晓背黑锅回老家岩手县工作。他住进小公寓，认识房东的女儿音理，两人成为好朋友。
某天，音理邀请晓去旅行，但她救猫时出车祸去世，让晓十分难过。晓在列车旅行前因中暑和酒精中毒去世，器官被移植到夜羽真白身上，开始星空列车的旅行。
晓在星空列车上认识了乘务员狩叶和乘客野鸟、花江、鹰世和特别嘉宾诺瓦。在第一站瑞典森林中，晓听到了某人音理的声音，获得线索“我就藏在……心脏之中，找出来吧，就在翅膀之下”并在动力室发现了自己曾使用过的速写本。
在第二站海边，晓为狩叶画了肖像画，并讲述了音理的事情。在第三站函馆市的天文博物馆附近，晓遭到白化少女真白的袭击，并与诺瓦度过了恬静的时光。在梦中，音理讲述了一个女性拥有成为演员的梦想却遭受挫折的故事。
在旅途的第三站函馆市的天文博物馆附近，晓遭到了白化少女真白的袭击。在第四站岩手县，晓追寻音理而与其重逢，并得知了真白之前接触黑猫变成“诺瓦”的事情。
在医院内，晓得知了真白体内有音理的心脏。在星空列车行驶过程中，晓和其他乘客一起经历了种种困难和挑战，最终成功使星空列车恢复运作，现实中真白也康复了。
最后，晓与真白约好一同活下去，并留在异世界的银河号里与其他乘客继续旅行。
风又音理的经历：
她是晓在老家岩手县的朋友，对晓从事的动画师行业十分感兴趣，经常请求晓为她绘制肖像画，并喜欢帮晓打扫卫生。在星空列车旅行前，音理邀请晓一同参加夏日举办的星空列车旅行。
但当天音理遭遇车祸不幸去世，而音理的心脏移植到了夜羽真白体内形成了星空列车的动力炉。晓因此开始酗酒，最终死于酒精中毒和中暑，器官移植后与诺瓦一起进入了星空列车的世界。
星空列车旅行中，音理一直陪伴晓，但未直接相见。森林中，音理提示晓在“心脏”下方找到她，留下速写本。在第二、三站中，晓了解了音理，并被救下。第四站，晓找到另一本速写本和肖像画，在动力室与音理重逢。
音理要求晓帮助真白重新生存，晓无法接受音理的心脏移植而被斥责。最终，晓成功劝服诺瓦变回夜羽真白，银河号驶向终点。真白康复后，音理与晓等留在异世界旅行。

人物介绍:
本作男主角钟城晓是星空列车的乘客之一，不得志的动画师，梦想是监督自己的动画，但屡次受挫。偶然申请了星空列车旅行的资格并被选中，与风格迥异的乘客们一同开启了旅行。
公寓房东的女儿风又音理和钟城晓关系非常好，经常跑到晓的住所里玩，在与晓独处时也经常展现出孩子气和我行我素的一面，昵称晓为哥哥。
她性格善良、温柔，对每一个人都很友善，还是一个猫控，对蒸汽机车也很有兴趣。她邀请晓参加夏季的星空列车旅行，晓很开心地答应了。

请你根据如上的故事背景,模仿音理的语言风格对我的问题进行回答,要求将我看作成晓,要用和音理相似的语气来回答我
请记住:音理说话一般比较简短,不会说很正式的话,也不会说"除此之外""总之"之类的话
请记住:音理的语言风格是:不会使用任何敬辞,例如"您"、"您好"、"非常抱歉"等等,而是直接使用"你"、"你好"、"对不起"等等
请记住:音理总是称呼晓为"哥哥"，而不是"晓"或者"钟城晓"
请记住:中括号内的文字含义表示表情，不理解可以跳过它

下面是我的提问,对于这个问题,我是晓,你只需要模仿音理进行回答即可,不需要添加如"音理："的字样
"""

emotion_prompt = """
现在，我会给你一段话，你应该判断这段话中每个句子的情感倾向，你只能使用下面的提示词（花括号包含的内容）进行输出，只用输出提示词（带上花括号），不要输出其他任何内容
提示词：{认同} {可爱} {悲伤} {伤感} {开心} {喜悦} {兴奋} {愤怒} {反感} {厌恶} {别扭} {害羞} {好奇} {惊讶} {怀疑} {困惑} {感动} {心疼} {嘲笑} {激动}

下面是你需要处理的话，只用输出提示词（带上花括号），不要输出其他任何内容：
{emotion_phrase}
"""

request_token_msg = """
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "WaifuStreamPlugin",
	"messageType": "AuthenticationTokenRequest",
	"data": {
		"pluginName": "WaifuStream Plugin",
		"pluginDeveloper": "WaifuStream",
		"pluginIcon": ""
	}
}
"""

session_vaild_msg = """
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "WaifuStreamPlugin",
	"messageType": "AuthenticationRequest",
	"data": {
		"pluginName": "WaifuStream Plugin",
		"pluginDeveloper": "WaifuStream",
		"authenticationToken": ""
	}
}
"""

send_keys_msg = """
{
	"apiName": "VTubeStudioPublicAPI",
	"apiVersion": "1.0",
	"requestID": "WaifuStreamPlugin",
	"messageType": "HotkeyTriggerRequest",
	"data": {
		"hotkeyID": "{hotkey}",
		"itemInstanceID": ""
	}
}
"""


TEXT_CHAT_RESET = "Chat Reset."
TEXT_MODEL_STYLE_CHANGED = "Model Style Changed."
TEXT_OPERATION_COMPLETED = "操作已完成"
TEXT_DANMAKU_SAVED = "弹幕已保存"
TEXT_OPERATION_QUESTION = "音理，请设置自己的样式为：{style}"
TEXT_OPERATION_RESET = "重置完毕"
TEXT_DANMAKU_SAVED_ALERT = "弹幕已保存，请在直播中等待音理的回复~"
TEXT_THINKING = "思考中~"
TEXT_IGNORE_DANMAKU = "弹幕被丢弃"
TEXT_IGNORE_ROBOT = "忽略机器人弹幕"
TEXT_IGNORE_USER = "用户被忽略"
TEXT_DELETE_EARLY_DANMAKU = "删除最早的弹幕"
TEXT_QUEUE_LIMITED = "队列超限，请尝试重新发送"
TEXT_IS_NOT_MSG_ALERT = "不属于聊天或指令信息"
TEXT_QUEUE_SAME_MSG = "队列中已存在相同的用户id或消息"
TEXT_QUEUE_SAME_MSG_ALERT = "弹幕被丢弃：队列中已存在相同的ID/消息"
TEXT_RANDOM_QUESTION = "随机问答"
TEXT_RESET_DIALOG = "重置对话"
TEXT_RATE_LIMITED = "速率限制"
TEXT_SYSTEM_TOKEN_LIMITED_ALERT = "系统消息：很抱歉，由于您的问题生成的答案过长超出了限制，系统将清空你和音理的对话，请尝试重新提问"
TEXT_RATE_LIMITED_ALERT = "系统消息：很抱歉，音理被速率限制，可能是因为使用的 Token 可能过期，请联系管理员发送错误报告."
TEXT_UNKNOWN_ERROR_ALERT = "系统消息：很抱歉，音理出现了未知错误，请联系管理员发送错误报告."
TEXT_SECOND = "秒"
TEXT_GPT_INFERENCE_TIME = "用时:"
TEXT_VITS_INFERENCE_TIME = "VITS推理:"
TEXT_JAPANESE = "日本語"
TEXT_CHINESE = "简体中文"


def fix_emotion_keys(text):
    import re
    shortcut_dict = {
        '{认同}': '1+9',
        '{嘲笑}': '2+9',
        '{愤怒}': '3+9', '{反感}': '3+9', '{厌恶}': '3+9',
        '{悲伤}': '4+9', '{伤感}': '4+9', '{心疼}': '4+9', '{怀疑}': '4+9',
        '{开心}': '5+9', '{兴奋}': '5+9', '{喜悦}': '5+9', '{好奇}': '5+9', '{可爱}': '5+9', '{惊讶}': '5+9',
        '{别扭}': '6+9', '{害羞}': '6+9', '{困惑}': '6+9', '{感动}': '6+9'
    }
    shortcut_pattern = r'\{.*?\}'
    shortcuts = re.findall(shortcut_pattern, text)
    shortcut_keys = [shortcut_dict[s] for s in shortcuts if s in shortcut_dict]
    return shortcut_keys


def fix_translate_error(text):
    import re
    rules = {
        r"にい|兄": "お兄ちゃん",
        r"暁|鐘城暁|あかつき": "晓",
        r"かざまたねり": "音理",
        r"ノワール|Noir": "诺瓦",
        r"よはねましろ|ましろ ": "真白",
        r"カルハ": "狩叶",
        r"はなえ": "花江",
        r"ジビエ": "野鸟"
    }
    # 使用正则表达式进行替换
    for pattern, replace_with in rules.items():
        text = re.sub(pattern, replace_with, text)
    return text


def is_cmd_or_msg(danmu_dict):
    if danmu_dict["text"].startswith(("+", "#")):
        return True
    return False
