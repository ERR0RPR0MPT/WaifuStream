import json
import random
import re
import threading
import time
import traceback
import danmaku
import multiprocess
import utils
import value
import vits
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import config


class BingAI:
    """
    BingAI 模型交互
    """

    def __init__(self, system_prompt=""):
        while True:
            try:
                self.bing = utils.async_run(Chatbot.create())
                break
            except:
                continue
        self.user = config.USER
        self.bot = config.BOT
        self.system_prompt = system_prompt
        self.user_prompt = ""
        self.num = 0

    def generate_prompt(self):
        return f"{self.system_prompt}\n{self.user_prompt}"

    def ask(self, msg):
        i = 0
        while True:
            try:
                i += 1
                if i > 3:
                    return "Someone tell LWSD there's some problems with my AI"
                if config.BING_CHAT_WS_URL == "":
                    rsp = utils.async_run(self.bing.ask(prompt=msg, conversation_style=ConversationStyle.creative))
                else:
                    rsp = utils.async_run(self.bing.ask(prompt=msg, conversation_style=ConversationStyle.creative,
                                                        wss_link=config.BING_CHAT_WS_URL))
                return rsp["item"]["messages"][1]["text"]
            except:
                continue


def generate_prompt(system_prompt="", user_prompt=""):
    return f"{system_prompt}\n{user_prompt}"


def ask_once(p):
    errors = 0
    while True:
        try:
            return utils.async_run(utils.async_run(Chatbot.create()).ask(prompt=p, conversation_style=ConversationStyle.creative))["item"]["messages"][1]["text"]
        except:
            errors += 1
            print("Ask_once Error.")
            if errors > 4:
                return "Someone tell LWSD there's some problems with my AI"


async def ask_stream(danmu, bot):
    """
    消息事件循环
    :param danmu: 消息
    :return:
    """

    q = danmu["text"]
    ide = danmu["id"]
    name = danmu["name"]
    timestamp = danmu["timestamp"]
    typer = "danmu"
    multi = "false"
    steps = "-1"
    if "{model_myself}" in q:
        q = q.replace("{model_myself}", config.MULTI_NAME)
        danmu["text"] = q
    try:
        typer = danmu["type"]
        if config.MULTI_MODE:
            multi = danmu["multi"]
            steps = danmu["steps"]
    except:
        pass

    if q[0] == "+" and config.EMOTION_SIMULATION_ENABLE and config.EMOTION_SIMULATION_MODE == "vts":
        # 切换模型样式
        model_style = q.replace("+", "")
        utils.set_model_style(model_style)
        q = config.TEXT_OPERATION_QUESTION.replace("{style}", model_style)

    # q = q.replace("#", "", 1)

    # # 限制对话次数
    # if len(chat.messages) > 15:
    #     chat = ChatGPT(config.SYSTEM_PROMPT)

    try:
        # 发送弹幕
        if ide != "0" or ide != "-10000":
            danmaku.send_danmaku(f"@{name} {config.TEXT_THINKING}")

        value.sender_str = f"{name} -> Inferencing..."
        value.stop_event = False

        # 提问-回答-记录
        value.chat_dict[ide].user_prompt = q
        answer = ""
        # 流式输出
        value.trans_origin_str = ""
        value.trans_target_str = ""
        value.trans_emotion_data = ""
        value.audio_queue = {}
        value.audio_threads_queue = {}
        value.audio_threads_num = 99999999
        value.is_play_audio_timeout = False
        i = 0
        sentences_num = 0
        sentences_detect = False
        t1 = threading.Thread(target=vits.play_audio_queue)
        t1.start()
        t_emo = None

        # 构造对话内容
        says = f"{value.chat_dict[ide].system_prompt}\n{value.chat_dict[ide].user_prompt}"

        last_symbol = ""
        # ts = value.chat_dict[ide].ask(says)
        async for final, ts in bot.bing.ask_stream(
                prompt=says,
                conversation_style=ConversationStyle.creative
        ):
            try:
                if type(ts) == str:
                    answer = ts
                if len(answer) >= config.MAX_ANSWER_LENGTH:
                    print("Answer is too long, shutdown...")
                    break
                value.trans_origin_str = answer
                if len(answer) == 0:
                    continue
                if answer[-1] in '，。：？！、,.:?!~' and last_symbol != answer[-1]:
                    try:
                        sentences_num += 1
                        if sentences_num == 3 and config.EMOTION_SIMULATION_ENABLE:
                            # 识别感情
                            sentences_detect = True
                            t_emo = threading.Thread(target=emotion_analysis_init, args=(answer,))
                            t_emo.start()
                        # 提取最后一句话
                        tokens = re.split('(?<=[，。：？！、,.:?!~])', answer)
                        tokens = [token.strip() for token in tokens if token.strip()]
                        partial_answer = tokens[-1]
                        # 调用翻译
                        trans_text = ""
                        if config.TRANSLATE_MODE == "bing":
                            print(f"Using BingAI to translate...")
                            trans_text = ask_once(generate_prompt(user_prompt=config.TRANSLATE_PROMPT.replace("{content}", partial_answer)))
                            print(f"BingAI translate done: {trans_text}")
                        elif config.TRANSLATE_MODE == "google":
                            k = 0
                            while True:
                                try:
                                    text = value.client.translate(partial_answer,
                                                                  target=config.TRANSLATE_TARGET_LANGUAGE)
                                    trans_text = text.translatedText
                                    break
                                except:
                                    traceback.print_exc()
                                    k += 1
                                    print("Error: translation failed, try other ways.")
                                    if k < 3:
                                        time.sleep(0.2)
                                        continue
                                    print("Using original text...")
                                    trans_text = answer
                                    break
                        # 翻译人工修正
                        trans_text = utils.fix_translate_error(trans_text)
                        # 更新UI
                        value.trans_target_str += trans_text
                        # 运行VITS推理
                        t = threading.Thread(target=vits.run_vits_and_play, args=(trans_text, i))
                        t.start()
                        value.audio_threads_queue[str(i)] = t
                        last_symbol = answer[-1]
                        i += 1
                    except:
                        traceback.print_exc()
                else:
                    continue
            except:
                traceback.print_exc()

        # 感情检测
        if not sentences_detect and config.EMOTION_SIMULATION_ENABLE:
            t_emo = threading.Thread(target=emotion_analysis_init, args=(answer,))
            t_emo.start()
        t_emo.join()

        print(f"BingAI Original Output: {answer}")
        utils.save_dialog(f"BingAI Original Output: {answer}")
        print(f"BingAI Emotional Output: {value.trans_emotion_data}")
        utils.save_dialog(f"BingAI Emotional Output: {value.trans_emotion_data}")
        print(f"Original = {value.trans_origin_str}\nTarget = {value.trans_target_str}")
        utils.save_dialog(f"Original = {value.trans_origin_str}\nTarget = {value.trans_target_str}\n")
        utils.save_short_dialog(f"A: {value.trans_origin_str}\n\n")
        value.sender_str = f"{name} -> Playing"

        # 等待模型音频完毕
        try:
            for _, v in value.audio_threads_queue.items():
                v.join()
            value.audio_threads_num = len(value.audio_threads_queue)
            t1.join(config.MAX_CHAT_ANSWER_SECONDS)
            if t1.is_alive():
                value.is_play_audio_timeout = True
                print("Play Audio Thread execution timed out. Stop the audio thread...")
        except:
            print("Error: May be shutdown by long tokens.")

        # 如果开启模型间交流，就发msg消息到multifile
        try:
            try:
                mut = danmu["multi_user_text"]
            except:
                mut = q
                pass
            if config.MULTI_MODE and typer != "enter" and typer != "gift":
                ts = str(time.time())
                msg_dict = {
                    "multi": "true",
                    "type": "msg",
                    "modelId": config.MULTI_ID,
                    "modelName": config.MULTI_NAME,
                    "multi_user": name,
                    "multi_user_text": mut,
                    "multi_model": config.MULTI_NAME,
                    "multi_model_text": answer,
                    "name": "模型间问答",
                    "id": "-5000",
                    "msgId": ''.join(random.choice("123456789") for _ in range(8)),
                    "text": answer,
                    "timestamp": ts,
                    "steps": "0" if steps == "-1" else str(int(steps) + 1),
                }
                multiprocess.write_file(ts + "_" + ''.join(
                    random.choice("123456789") for _ in range(8)) + "_msg_" + config.MULTI_NAME + ".txt",
                                        json.dumps(msg_dict))
        except:
            traceback.print_exc()
            print("Error when run multi sender.")

        value.stop_event = True
        value.audio_queue = {}
        value.audio_threads_queue = {}
        value.sender_str = f"{name} -> Finished"
        return answer
    except:
        traceback.print_exc()
        print("Error: BingAI chat failed.")
        value.stop_event = True
        value.audio_queue = {}
        value.audio_threads_queue = {}
        value.sender_str = f"{name} -> Error"
        return "Error: BingAI chat failed."


def sync_ask_stream(danmu):
    ide = danmu["id"]
    name = danmu["name"]
    try:
        value.chat_dict[ide]
    except:
        value.chat_dict[ide] = BingAI(config.SYSTEM_PROMPT)
    if value.chat_dict[ide].num > config.BING_MAX_DIALOG_NUM:
        value.chat_dict[ide] = BingAI(config.SYSTEM_PROMPT)
        danmaku.send_danmaku(f"@{name} {config.TEXT_MAX_NUM_LIMITED}")
    bot = value.chat_dict[ide]
    utils.async_run(ask_stream(danmu, bot))


def emotion_analysis(msg):
    """
    情感分析
    :param msg: 消息(string)
    :return: 情感分析结果(string)
    """
    return ask_once(generate_prompt(system_prompt=config.EMOTION_PROMPT, user_prompt=msg))


def emotion_analysis_init(answer):
    """
    情感分析初始化
    :param answer: 消息(string)
    :return: None
    """
    emotion_data = emotion_analysis(answer)
    value.trans_emotion_data = emotion_data

    # 判断使用vts还是Web
    if config.EMOTION_SIMULATION_MODE == "vts":
        emotion_keys = utils.fix_emotion_keys(emotion_data)
        threading.Thread(target=utils.send_keys, args=(emotion_keys,)).start()
    elif config.EMOTION_SIMULATION_MODE == "web":
        emotion_images = utils.fix_emotion_images(emotion_data)
        threading.Thread(target=utils.send_images, args=(emotion_images,)).start()
