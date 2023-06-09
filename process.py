import os
import random
import time
import traceback
import openai
import bing
import config
import oa
import utils
import value


def execute():
    """
    消息处理主线程
    :return:
    """
    while True:
        try:
            choice_flag = 0
            danmu = None
            while True:
                if choice_flag <= config.MAX_WAIT_SECONDS:
                    if len(value.msg_queue) <= 0:
                        choice_flag += 1
                        time.sleep(0.3)
                        continue
                    choice_flag = 0
                    danmu = value.msg_queue.pop(0)
                    msg = danmu["text"]
                    ide = danmu["id"]
                    name = danmu["name"]
                    timestamp = danmu["timestamp"]
                    delay_seconds = time.time() - float(timestamp)
                    if delay_seconds > 5.0 and danmu["type"] == "enter":
                        print(f"Message \"Enter\" timeout for {str(delay_seconds)}, select next message.")
                        continue
                    if delay_seconds > 18.0:
                        print(f"Message \"Normal\" timeout for {str(delay_seconds)}, select next message.")
                        continue
                else:
                    if config.AUTO_ANSWER_ENABLE:
                        choice_flag = 0
                        msg = random.choice(config.RANDOM_QUESTION)
                        ide = "0"
                        name = config.TEXT_RANDOM_QUESTION
                        
                        timestamp = str(time.time())
                    else:
                        choice_flag = 0
                        time.sleep(0.3)
                        continue
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
                    utils.save_dialog("ID=" + ide + " Name=" + name)
                    utils.save_dialog(f"Question: {msg}")
                    utils.save_short_dialog(f"Q: {msg}")
                    value.sender_str = f"{name} -> Inferencing..."
                    start_time = time.time()
                    print("Inferencing...")
                    retries = 0
                    while True:
                        retries += 1
                        try:
                            if config.MODEL == "openai":
                                oa.on_msg(danmu)
                            elif config.MODEL == "bing":
                                bing.sync_ask_stream(danmu)
                            break
                        except openai.error.AuthenticationError:
                            print("OpenAI AuthenticationError, Try to set a key...")
                            oa.set_available_openai_key()
                            continue
                        except openai.error.InvalidRequestError:
                            print("Token has been limited. Try to recovery...")
                            if not config.TEXT_RESET_DIALOG in value.sender_str:
                                value.sender_str = config.TEXT_RESET_DIALOG + " -> " + value.sender_str
                            if retries >= 2:
                                break
                            value.chat_dict[ide] = oa.ChatGPT(config.SYSTEM_PROMPT)
                            continue
                        except openai.error.RateLimitError:
                            print("Rate has been limited. Try to recovery...")
                            if not config.TEXT_RATE_LIMITED in value.sender_str:
                                value.sender_str = config.TEXT_RATE_LIMITED + " -> " + value.sender_str
                            # if retries >= 3:
                            #     time.sleep(10)
                            if retries >= 5:
                                break
                            oa.set_available_openai_key()
                            continue
                        except:
                            traceback.print_exc()
                            print("Error in Inferencing.")
                            break
                    end_time = time.time()
                    if config.MODEL == "openai":
                        op_key = openai.api_key
                        print(f"Used API Key：index={str(config.OPENAI_API_KEY_LIST.index(op_key) + 1)} -> {oa.hide_openai_api_key(op_key)}")
                    print(config.TEXT_GPT_INFERENCE_TIME + " {}".format(
                        round(end_time - start_time, 2)) + config.TEXT_SECOND)
                else:
                    print('Error: Empty Message.')
                print("Finished.\n----------------------------------")
        except:
            traceback.print_exc()
            print("Error")
            time.sleep(3)
            print("Retry...")
            continue
