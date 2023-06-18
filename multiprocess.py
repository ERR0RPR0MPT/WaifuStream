
import json
import os.path
import random
import time
import traceback
import config
import value


def calculate_files():
    """
    统计目录下所有文件（不包含子目录）并返回列表
    :return: 文件列表
    """
    files = []
    for file in os.listdir(config.MULTI_DIR):
        if os.path.isfile(os.path.join(config.MULTI_DIR, file)):
            files.append(file)
    return files


def calculate_changed_files(old_list, new_list):
    """
    计算两个列表之间新增的元素并返回这些元素为一个列表
    :param old_list: 旧列表
    :param new_list: 新列表
    :return: 新增元素列表
    """
    return list(set(new_list) - set(old_list))


def write_file(file_name, msg):
    while True:
        try:
            with open(os.path.join(os.getcwd(), config.MULTI_DIR, file_name), 'w', encoding='utf-8') as f:
                f.write(msg)
            break
        except:
            time.sleep(0.1)
            continue


def multiprocess():
    """
    多模型间消息传递
    :return:
    """
    if not os.path.exists(config.MULTI_DIR):
        os.makedirs(config.MULTI_DIR)
    files_prev = calculate_files()
    while True:
        if not config.MULTI_MODE:
            time.sleep(1)
            continue
        try:
            files_current = calculate_files()
            if len(files_current) == len(files_prev):
                time.sleep(1)
                continue
            print("Find multi msg, start to process...")
            new_files = calculate_changed_files(files_prev, files_current)
            files_prev = files_current
            for fl in reversed(new_files):
                print(f"Open file to read json: {fl}")
                with open(os.path.join(os.getcwd(), config.MULTI_DIR, fl), 'r') as f:
                    data_str = f.read()
                multi_data = json.loads(data_str)
                if multi_data["multi"] == "true" and multi_data["type"] == "msg" and multi_data[
                    "modelId"] != config.MULTI_ID and int(
                        multi_data["steps"]) <= config.MULTI_MAX_STEPS:
                    print(f"Find multi msg: modelId={multi_data['modelId']}, steps={multi_data['steps']}")
                    # 写入read消息到multifile
                    ra = random.randint(10000000, 99999999)
                    read_data = {
                        "multi": "true",
                        "type": "read",
                        "modelId": config.MULTI_ID,
                        "modelName": config.MULTI_NAME,
                        "multi_user": multi_data["multi_user"],
                        "multi_user_text": multi_data["multi_user_text"],
                        "multi_model": multi_data["multi_model"],
                        "multi_model_text": multi_data["multi_model_text"],
                        "multi_random_num": str(ra),
                        "id": multi_data["id"],
                        "name": multi_data["name"],
                        "msgId": multi_data["msgId"],
                        "text": multi_data["text"],
                        "timestamp": str(time.time()),
                        "steps": multi_data["steps"]
                    }
                    time.sleep(random.random())
                    # file_name : {timestamp}_{random_str8}_{model}.txt
                    write_file(multi_data["timestamp"] + "_" + str(ra) + "_read_" + config.MULTI_NAME + ".txt",
                               json.dumps(read_data))
                    print("参加消息竞争")
                    time.sleep(3)
                    # 不只检查最后一个，而是检查所有的read消息
                    files_current = calculate_files()
                    new_files = calculate_changed_files(files_prev, files_current)
                    newest_bigger_random_num = -1
                    newest_select_file = ""
                    for kp in new_files:
                        if not "_read_" in kp:
                            continue
                        with open(os.path.join(os.getcwd(), config.MULTI_DIR, kp), 'r') as f:
                            data_str = f.read()
                        last_data = json.loads(data_str)
                        if last_data["multi"] == "true" and last_data["type"] == "read" and int(last_data["multi_random_num"]) > newest_bigger_random_num:
                            newest_bigger_random_num = int(last_data["multi_random_num"])
                            newest_select_file = kp
                    print(f"选择最新的文件：{newest_select_file}")
                    with open(os.path.join(os.getcwd(), config.MULTI_DIR, newest_select_file), 'r') as f:
                        data_str = f.read()
                    last_data = json.loads(data_str)
                    multi_text = config.MULTI_PROMPT.replace("{user}", last_data["multi_user"]) \
                        .replace("{user_text}", last_data["multi_user_text"]) \
                        .replace("{model}", last_data["multi_model"]) \
                        .replace("{model_text}", last_data["multi_model_text"])
                    if last_data["multi"] == "true" and last_data["modelId"] == config.MULTI_ID and last_data["msgId"] == multi_data["msgId"]:
                        print("该模型取得了竞争条件")
                        # 竞争条件指定该模型回答问题
                        msg_dict = {
                            "multi": "true",
                            "type": "msg",
                            "modelId": config.MULTI_ID,
                            "modelName": config.MULTI_NAME,
                            "multi_user": multi_data["multi_user"],
                            "multi_user_text": multi_data["multi_user_text"],
                            "multi_model": multi_data["multi_model"],
                            "multi_model_text": multi_data["multi_model_text"],
                            "steps": multi_data["steps"],
                            "text": multi_text,
                            "msgId": multi_data["msgId"],
                            "id": multi_data["id"],
                            "name": multi_data["name"],
                            "timestamp": multi_data["timestamp"],
                        }
                        value.msg_queue.append(msg_dict)
                        break
                    else:
                        # 竞争失败，等待下一次消息
                        print("竞争失败，等待下一次消息")
                        time.sleep(1)
                        break
                else:
                    # 消息不符合要求，等待下一次消息
                    time.sleep(1)
                    continue
        except:
            traceback.print_exc()
            print("Error when run multiprocess. Retry...")
            time.sleep(1)
            continue
