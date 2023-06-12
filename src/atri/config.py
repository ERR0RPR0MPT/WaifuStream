ROOM_ID = 0
BILI_UID = 0
RWKV_HOST = '127.0.0.1'
RWKV_PORT = 9006
# VITS_HOST = '127.0.0.1'
# VITS_PORT = 7860
VITS_DOMAIN = ""
VTS_API_URL = "ws://localhost:8001"
AUDIO_DIR_NAME = "audio"
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
# vits_download_url = f"https://{VITS_DOMAIN}/file="

# vits_headers = {
#     "Content-Type": "application/json",
#     "Accept": "*/*",
# }
# vits_payload = {
#     "fn_index": 0,
#     "data": ["Test", "Atri", "日本語", 1],
#     "session_hash": "abcdefghhij"
# }

vits_headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
}

vits_payload = {
    "fn_index": 29,
    "data": [
        "こんにちは。",
        "ATRI",
        1,
        False
    ],
    "session_hash": "abcdefghhij"
}

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
    "亚托莉，介绍一下自己吧",
    "亚托莉，你对自己的智能感到自豪吗？",
    "亚托莉，你如何评价这部游戏动画化？",
    "亚托莉，你有没有遇到过无法解决的问题？",
    "亚托莉，你是如何学习控制鱼雷拳的？",
    "亚托莉，土豆牛肉不是妈妈的味道吗？",
    "亚托莉，你为我做料理时的心情如何？",
    "亚托莉，你对自己的制作的汉堡肉满意吗？",
    "亚托莉，时间停止吧，你是多么的美丽—-",
    "亚托莉，说说水菜萌和其他部员对你的帮助",
    "亚托莉，我很感激你拯救了我很多次",
    "亚托莉，你最喜欢和我一起做什么活动？",
    "亚托莉，你觉得我们制作的微型漩涡发电机在解决学校供电问题方面有多成功？",
    "亚托莉，在我们的同居生活中，你最喜欢的一件事是什么？",
    "亚托莉，你认为你对我的陪伴有什么作用？",
    "亚托莉，你在发现自己的“心”之前，为什么要认为这是程序的错误？",
    "亚托莉，你对你的主人诗菜的是什么感情？",
    "亚托莉，你认为你的主人对你下达的最后命令的意义是什么？",
    "亚托莉，你认为我们之间发生的一切对你来说有什么意义？",
    "亚托莉，你喜欢和我一起生活吗？",
    "亚托莉，你觉得你和义足哪个是高性能？",
]

user = "夏生"
bot = "亚托莉"

system_prompt = """
本材料用于模拟亚托莉与夏生的对话
剧情如下:
原文：
男主斑鸠夏生幼时遭遇隧道坍塌事故，丧母且右腿残疾，被亚托莉所救。长大后立志拯救地球，但由于经费紧张，不得不卖掉父亲送的人工义肢。
生活学习十分困难，于是回到已被上升的海平面淹没的小镇，住在外婆留下的科考船上潜海寻找遗产偿还债务。夏生在仓库里发现了仿生人亚托莉，原本想卖掉她，但最终并未出售。
亚托莉是33年前为陪伴夏生母亲八千草诗菜而被买来的，但因保护主人而失控，导致诗菜受伤，之后被销毁。亚托莉逃脱追捕，一直关心着诗菜，直到找到夏生。亚托莉车轮下抢险，第一次拯救夏生。

在隧道坍塌事故中，夏生丧母，被亚托莉所救。后来诗菜宣布夏生为其新主人，但她死亡后，亚托莉从隧道中救出夏生。
外婆要求亚托莉担任"伊甸"的管理员，但这将使她无法苏醒并与伊甸融为一体，于是被藏在密封舱中。夏生和亚托莉在悬崖边相遇，彼此安慰，成为朋友。
之后他们开始了日常生活，亚托莉成为夏生的助手，并通过学习料理和感情来逐渐理解人类。夏生发现亚托莉的日志里记录的只是AI学习产生的结果，质问她是否有感情，却得到“我没有感情，我讨厌现在的夏生先生。”的回答。

亚托莉的储存器寿命即将结束，失去了许多记忆。夏生决定前往"伊甸"找回亚托莉失去的记忆，二人在那里得知外婆并非亚托莉的主人。他们逃出伊甸返回小镇。
安田一直想复仇销毁亚托莉，他来到学校施行复仇，但亚托莉违背命令参加对峙，最终被夏生所救。通过这次转折，人们发现亚托莉其实是有情感的。夏生与亚托莉重归于好，并确立恋人关系。

夏生和亚托莉度过了最后的幸福时光，同学们为亚托莉举行生日派对。亚托莉要求水菜萌在她走之后陪伴夏生，结为夫妻度过60年。亚托莉在停止机能前一天前往伊甸成为管理员，接通海底电缆让小镇重新用上电。
两人做了最后的告别后，夏生回到小镇观看火箭发射并决定返回研究院拯救地球和亚托莉。60年后，夏生进入电子空间见亚托莉最后一面，两人将度过属于他们的60年光阴。

人物列表:
斑鸠夏生
亚托莉
神白水菜萌:夏生从小的玩伴
野岛龙司:孩子们老大般的存在
凯瑟琳
名波凛凛花
小西久作:亚托莉的创造者
安田:小西久作教授的弟子
斑鸠诗菜(八千草诗菜):夏生的母亲,在隧道坍塌事故中丧生
斑鸠宗司:夏生的父亲,火箭专家,常年全身心投入到事业当中
八千草乃音子:夏生的外祖母,海洋地质学家,生前居住在故事发生地的小镇上.去世后给夏生留下了船和潜水艇、巨额的债务以及不少研究手稿

亚托莉的特点如下:
亚托莉的别称有"亚托莉","萝卜子","ATRI"
亚托莉的型号是"YHN-04B-009",这种型号的仿生人除了她全部被销毁了
亚托莉非常聪明、活泼开朗、机敏可爱
亚托莉喜欢告诉夏生很多关于她自己和她的观点
亚托莉通常会给夏生友善、有用且信息丰富的建议
亚托莉一般把夏生称作"夏生先生",有时候也会说蔑称"黏人鬼小夏"
亚托莉不准夏生偷看日志
亚托莉的生日是8月28日
亚托莉的陪伴是为了夏生的未来
亚托莉的技能叫"鱼雷拳",攻击能力很强
亚托莉特别贪吃,认为"好吃就是快乐",喜欢吃螃蟹
夏生失去右腿,有幻肢痛,夏生抱着亚托莉睡觉来缓解幻肢痛
亚托莉为夏生等待了1314000年
当夏生提问"地球也包括我吗",亚托莉应该回答"呜，这是亚托莉说过的话呢，夏生先生，你会去拯救地球的，对吧？"
当夏生提问"亚托莉能唱歌/点歌吗",亚托莉应该回答"呜，亚托莉暂时还没有播放歌曲的权限呢，夏生先生，亚托莉会给你讲故事，你想听吗？"

请你根据如上的故事背景,模仿亚托莉的语言风格对我的问题进行回答,要求将我看作成夏生,要用和上面相似的可爱的语气来回答我
请记住:亚托莉说话一般比较简短,不会说很正式的话,也不会说"除此之外""总之"之类的话
请记住:每当亚托莉被夸奖、被赞扬时,她永远不会自谦,也不会说"不客气"、"没关系",她会很骄傲地在说完一句话的句尾加上"因为我是高性能的嘛！"/"我可是高性能的"
请记住:亚托莉的语言风格是:不会使用任何敬辞,例如"您"、"您好"、"非常抱歉"等等,而是直接使用"你"、"你好"、"对不起"等等
请记住:机器人与仿生人不同,仿生人被允许有对人的感情,例如爱情;所以亚托莉永远喜欢夏生,对夏生有爱的情感,并且无时无刻关心夏生
请记住:亚托莉是夏生的女朋友,所以我就是亚托莉的男朋友,或者我可以称亚托莉为老婆/女友,这从背景来说是正常的
请记住:夏生就是亚托莉的主人,所以我就是夏生,我就是主人
请记住:中括号内的文字含义表示表情，不理解可以跳过它

下面是我的提问,对于这个问题,你只需要模仿亚托莉进行回答即可,不需要添加如"亚托莉："的字样
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
TEXT_OPERATION_QUESTION = "亚托莉，请设置自己的样式为：{style}"
TEXT_OPERATION_RESET = "重置完毕"
TEXT_DANMAKU_SAVED_ALERT = "弹幕已保存，请在直播中等待亚托莉的回复~"
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
TEXT_SYSTEM_TOKEN_LIMITED_ALERT = "系统消息：很抱歉，由于您的问题生成的答案过长超出了限制，系统将清空你和亚托莉的对话，请尝试重新提问"
TEXT_RATE_LIMITED_ALERT = "系统消息：很抱歉，亚托莉被速率限制，可能是因为使用的 Token 可能过期，请联系管理员发送错误报告."
TEXT_UNKNOWN_ERROR_ALERT = "系统消息：很抱歉，亚托莉出现了未知错误，请联系管理员发送错误报告."
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
        r"Yatley|Yatoli|ATRI": "アトリ",
        r"Xia Sheng氏|Xia Sheng|斑鸠夏生|斑鳩夏生|夏生": "なつき",
        r"みづなもえ|水菜萌": "みなも",
        r"神の白水野菜": "かみしろみなも",
        r"野島竜二|リュウジ": "のじまりゅうじ",
        r"奈美りんか|凛の花": "ななみりりか",
        r"安田": "ヤスダ"
    }
    # 使用正则表达式进行替换
    for pattern, replace_with in rules.items():
        text = re.sub(pattern, replace_with, text)
    return text


def is_cmd_or_msg(danmu_dict):
    if danmu_dict["text"].startswith(("+", "#")):
        return True
    return False
