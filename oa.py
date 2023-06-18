import json
import random
import re
import threading
import time
import traceback
import config
import danmaku
import multiprocess
import utils
import openai
import value
import vits


class ChatGPT:
    """
    GPT-3.5 Turbo 模型交互
    """

    def __init__(self, system_prompt):
        self.user = config.USER
        self.messages = [{"role": "system", "content": system_prompt}]

    def ask_gpt(self):
        """
        交互(流式输出)
        :return:
        """
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=True
        )
        return rsp

    def ask_gpt_get(self):
        """
        交互
        :return:
        """
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
        )
        return rsp.get("choices")[0]["message"]["content"]


def hide_openai_api_key(api_key):
    try:
        return api_key[:8] + "*" * (len(api_key) - len(api_key[:8]) - len(api_key[-6:])) + api_key[-6:]
    except:
        return ""


def set_available_openai_key():
    """
    随机获取一个 OpenAI API Key，并检查可用性
    :return:
    """
    i = 0
    while True:
        i += 1
        if len(config.OPENAI_API_KEY_LIST) == 0:
            raise Exception("You have set nothing for OpenAI API Key, Please set one key first.")
        if i >= 20:
            raise Exception("Sorry, no available OpenAI KEY.")
        new_key = random.choice(config.OPENAI_API_KEY_LIST)
        if new_key != openai.api_key or len(config.OPENAI_API_KEY_LIST) == 1:
            # 检查可用性
            origin_key = openai.api_key
            openai.api_key = new_key
            try:
                c = ChatGPT("test")
                c.messages.append({"role": "user", "content": "test"})
                c.ask_gpt_get()
            except:
                traceback.print_exc()
                openai.api_key = origin_key
                config.OPENAI_API_KEY_LIST.remove(new_key)
                print(
                    f"OpenAI API Key: {hide_openai_api_key(new_key)} is not available. Check for another one...")
                continue
            openai.api_key = new_key
            return


def on_msg(danmu):
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

    try:
        value.chat_dict[ide]
    except:
        value.chat_dict[ide] = ChatGPT(config.SYSTEM_PROMPT)

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
        value.chat_dict[ide].messages.append({"role": "user", "content": q})
        answer_rsp = value.chat_dict[ide].ask_gpt()
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

        for chunk in answer_rsp:
            try:
                now_token = chunk.choices[0].delta.to_dict()["content"]
                answer += now_token
                if len(answer) >= config.MAX_ANSWER_LENGTH:
                    print("Answer too long, shutdown...")
                    break
                value.trans_origin_str = answer
                # 检测是否成功输出一句话
                if any(char in now_token for char in '，。：？！、,.:?!~'):
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
                        if config.TRANSLATE_MODE == "gpt":
                            print(f"Using GPT to translate...{partial_answer}")
                            trans_chat = ChatGPT(config.TRANSLATE_PROMPT)
                            trans_chat.messages.append(
                                {"role": "user",
                                 "content": config.TRANSLATE_PROMPT.replace("{content}", partial_answer)})
                            trans_text = trans_chat.ask_gpt_get()
                            print(f"GPT translate done: {trans_text}")
                        elif config.TRANSLATE_MODE == "google":
                            k = 0
                            while True:
                                try:
                                    text = value.client.translate(partial_answer,
                                                                  target=config.TRANSLATE_TARGET_LANGUAGE)
                                    trans_text = text.translatedText
                                    break
                                except:
                                    # traceback.print_exc()
                                    k += 1
                                    print("Error: translation failed, try other ways.")
                                    if k < 3:
                                        time.sleep(0.2)
                                        continue
                                    print("Using original text...")
                                    trans_text = partial_answer
                                    break

                        # 翻译人工修正
                        trans_text = utils.fix_translate_error(trans_text)
                        # 更新UI
                        value.trans_target_str += trans_text
                        # 运行VITS推理
                        t = threading.Thread(target=vits.run_vits_and_play, args=(trans_text, i))
                        t.start()
                        value.audio_threads_queue[str(i)] = t
                        i += 1
                    except:
                        traceback.print_exc()
                        continue
            except:
                continue

        # 感情检测
        if not sentences_detect and config.EMOTION_SIMULATION_ENABLE:
            t_emo = threading.Thread(target=emotion_analysis_init, args=(answer,))
            t_emo.start()
        t_emo.join()

        print(f"GPT Original Output: {answer}")
        utils.save_dialog(f"GPT Original Output: {answer}")
        print(f"GPT Emotional Output: {value.trans_emotion_data}")
        utils.save_dialog(f"GPT Emotional Output: {value.trans_emotion_data}")
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
        value.chat_dict[ide].messages.append({"role": "assistant", "content": answer})
        value.sender_str = f"{name} -> Finished"
        return answer
    except:
        traceback.print_exc()
        print("Error: GPT chat failed.")
        value.stop_event = True
        value.audio_queue = {}
        value.audio_threads_queue = {}
        value.sender_str = f"{name} -> Error"
        return "Error: GPT chat failed."


def emotion_analysis(msg):
    """
    情感分析
    :param msg: 消息(string)
    :return: 情感分析结果(string)
    """
    emotion_temp = ChatGPT(config.EMOTION_PROMPT)
    emotion_temp.messages.append({"role": "user", "content": msg})
    emotion_data = emotion_temp.ask_gpt_get()
    return emotion_data


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


if config.MODEL == "openai":
    set_available_openai_key()
