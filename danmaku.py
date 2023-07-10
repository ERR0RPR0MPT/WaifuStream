import random
import threading
import time
import traceback
from bilibili_api import sync, Danmaku
import blivedm
import utils
import value
import config


def send_danmaku_origin(msg):
    """
    发送弹幕(原始)
    :param msg: 弹幕内容
    :return:
    """
    try:
        if msg == "":
            print("Empty danmaku msg, ignore.")
            return
        sync(value.roomOp.send_danmaku(Danmaku(msg)))
        print("成功发送弹幕")
    except:
        print("Failed to send danmaku.")


def send_danmaku(msg):
    """
    发送弹幕
    :param msg: 弹幕内容
    :return:
    """
    threading.Thread(target=send_danmaku_origin, args=(msg,)).start()


class BliveHandler(blivedm.BaseHandler):
    # 演示如何添加自定义回调
    _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()

    # 入场消息回调
    async def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
        print(f"[{str(client.room_id)}] INTERACT_WORD: self_type={type(self).__name__}, room_id={str(client.room_id)},"
              f" uname={command['data']['uname']}")
        danmu_dict = {
            "multi": "false",
            "type": "enter",
            "modelId": config.MULTI_ID,
            "modelName": config.MULTI_NAME,
            # "text": config.WELCOME_PROMPT.replace("{user}", danmu.sender.name),
            "text": config.WELCOME_PROMPT.replace("{user}", "观众"),
            "id": "99999",
            "name": "观众",
            "msgId": ''.join(random.choice("123456789") for _ in range(8)),
            "steps": "-1",
            "timestamp": str(time.time())
        }
        # 随机概率执行
        if random.random() > config.INTERACT_MESSAGES_RANDOM:
            print("Interact message random rate limit reached, ignore this message, id=" + str(
                "99999") + " name=" + "观众")
            return
        # 判断条件
        current_time = time.time()
        if current_time - value.interact_last_append_time <= 60 and value.interact_messages_appended >= config.MAX_INTERACT_MESSAGES_PER_MINUTE:
            print("Interact message rate limit reached, ignore this message, id=" + str(
                "99999") + " name=" + "观众")
            return
        else:
            value.interact_last_append_time = current_time
            value.interact_messages_appended = 1
        value.msg_queue.append(danmu_dict)

    _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
        print(f'心跳包：[{str(client.room_id)}] 当前人气值：{message.popularity}')

    async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
        print(f'收到弹幕：[{str(client.room_id)}] {message.uname}：{message.msg}')
        danmu_dict = {
            "multi": "false",
            "type": "danmaku",
            "modelId": config.MULTI_ID,
            "modelName": config.MULTI_NAME,
            "text": message.msg,
            "id": str(client.room_id),
            "name": message.uname,
            "msgId": ''.join(random.choice("123456789") for _ in range(8)),
            "steps": "-1",
            "timestamp": str(time.time()),
        }
        # 替换中文符号
        danmu_dict["text"] = danmu_dict["text"].replace("：", ":", 1).replace("＃", "#", 1)
        # 避免机器人发送的弹幕被检测到
        if danmu_dict["id"] == str(config.BILI_USER_UID) and (
                config.TEXT_IGNORE_DANMAKU in danmu_dict["text"] or config.TEXT_DANMAKU_SAVED in danmu_dict[
            "text"] or config.TEXT_THINKING in
                danmu_dict["text"]):
            print(
                config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_ROBOT + "): text=" + danmu_dict["text"] + " id=" +
                danmu_dict[
                    "id"] + " name=" + danmu_dict["name"])
            return

        # 指定忽略的用户
        if danmu_dict["id"] in config.IGNORED_USERS:
            print(
                config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_USER + "): text=" + danmu_dict["text"] + " id=" +
                danmu_dict[
                    "id"] + " name=" + danmu_dict["name"])
            return

        # 弹幕是否合法
        if utils.is_valid_msg(danmu_dict):
            while len(value.msg_queue) >= config.MAX_DANMAKU_QUEUE_LENGTH:
                msg_temp = value.msg_queue.pop(0)
                print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_DELETE_EARLY_DANMAKU + "): text=" + msg_temp[
                    "text"] + " id=" +
                      msg_temp["id"] + " name=" + msg_temp["name"])
                send_danmaku(f"{config.TEXT_IGNORE_DANMAKU}: {config.TEXT_QUEUE_LIMITED}")

            # 检测是否为聊天信息或指令
            if not utils.is_cmd_or_msg(danmu_dict):
                print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IS_NOT_MSG_ALERT + "): text=" + danmu_dict[
                    "text"] + " id=" +
                      danmu_dict["id"] + " name=" + danmu_dict["name"])
                return
            # 去除前缀
            danmu_dict["text"] = danmu_dict["text"].replace(config.CONFIG_MATCH_COMMAND, "", 1)
            value.msg_queue.append(danmu_dict)
            print(config.TEXT_DANMAKU_SAVED + ": text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" +
                  danmu_dict["name"])
            send_danmaku(config.TEXT_DANMAKU_SAVED_ALERT)
        else:
            print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_QUEUE_SAME_MSG + "): text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" + danmu_dict["name"])
            send_danmaku(config.TEXT_QUEUE_SAME_MSG_ALERT)

    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        print(f'[{str(client.room_id)}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')
        danmu_dict = {
            "multi": "false",
            "type": "gift",
            "modelId": config.MULTI_ID,
            "modelName": config.MULTI_NAME,
            "text": config.THANKS_FOR_GIFT_PROMPT.replace("{user}", message.uname).replace("{gift}",
                                                                                           f"{message.gift_name}x{message.num}（{message.coin_type}瓜子x{message.total_coin}）"),
            "id": str(client.room_id),
            "name": message.uname,
            "msgId": ''.join(random.choice("123456789") for _ in range(8)),
            "steps": "-1",
            "timestamp": str(time.time()),
        }
        print("收到礼物：" + str(danmu_dict))
        value.msg_queue.append(danmu_dict)

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        print(f'[{str(client.room_id)}] {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        print(f'[{str(client.room_id)}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')


async def init_danmaku_main():
    value.room = blivedm.BLiveClient(config.BILI_ROOM_ID, ssl=False)
    handler = BliveHandler()
    value.room.add_handler(handler)
    value.room.start()
    try:
        await value.room.join()
    finally:
        await value.room.stop_and_close()


def init_danmaku(loop):
    """
    初始化弹幕库并保活
    :return:
    """
    print("Init danmaku library.")
    while True:
        try:
            sync(init_danmaku_main())
            print("弹幕库退出，等待5s运行")
        except:
            traceback.print_exc()
            print("弹幕库出现了奇怪的错误，等待5s运行")
        time.sleep(5)


# @value.room.on(Events.DANMU_MSG)
# async def on_danmaku(ctx: BLiverCtx):
#     """
#     收到弹幕
#     :param ctx:
#     :return:
#     """
#     danmu = DanMuMsg(ctx.body)
#     danmu_dict = {
#         "multi": "false",
#         "type": "danmaku",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         "text": danmu.content,
#         "id": str(danmu.sender.id),
#         "name": danmu.sender.name,
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time()),
#     }
#     print("收到弹幕：" + str(danmu_dict))
#     # 替换中文符号
#     danmu_dict["text"] = danmu_dict["text"].replace("：", ":", 1).replace("＃", "#", 1)
#     # 避免机器人发送的弹幕被检测到
#     if danmu_dict["id"] == str(config.BILI_USER_UID) and (
#             config.TEXT_IGNORE_DANMAKU in danmu_dict["text"] or config.TEXT_DANMAKU_SAVED in danmu_dict[
#         "text"] or config.TEXT_THINKING in
#             danmu_dict["text"]):
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_ROBOT + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict["name"])
#         return
#
#     # 指定忽略的用户
#     if danmu_dict["id"] in config.IGNORED_USERS:
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_USER + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict["name"])
#         return
#
#     # 弹幕是否合法
#     if utils.is_valid_msg(danmu_dict):
#         while len(value.msg_queue) >= config.MAX_DANMAKU_QUEUE_LENGTH:
#             msg_temp = value.msg_queue.pop(0)
#             print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_DELETE_EARLY_DANMAKU + "): text=" + msg_temp[
#                 "text"] + " id=" +
#                   msg_temp["id"] + " name=" + msg_temp["name"])
#             send_danmaku(f"{config.TEXT_IGNORE_DANMAKU}: {config.TEXT_QUEUE_LIMITED}")
#
#         # 检测是否为聊天信息或指令
#         if not utils.is_cmd_or_msg(danmu_dict):
#             print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IS_NOT_MSG_ALERT + "): text=" + danmu_dict[
#                 "text"] + " id=" +
#                   danmu_dict["id"] + " name=" + danmu_dict["name"])
#             return
#         # 去除前缀
#         danmu_dict["text"] = danmu_dict["text"].replace(config.CONFIG_MATCH_COMMAND, "", 1)
#         value.msg_queue.append(danmu_dict)
#         print(config.TEXT_DANMAKU_SAVED + ": text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" +
#               danmu_dict[
#                   "name"])
#         send_danmaku(config.TEXT_DANMAKU_SAVED_ALERT)
#     else:
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_QUEUE_SAME_MSG + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict[
#                   "name"])
#         send_danmaku(config.TEXT_QUEUE_SAME_MSG_ALERT)
#
#
# @value.room.on(Events.INTERACT_WORD)
# async def on_enter(ctx: BLiverCtx):
#     """
#     观众进入直播间
#     :param ctx:
#     :return:
#     """
#     danmu = DanMuMsg(ctx.body)
#     danmu_dict = {
#         "multi": "false",
#         "type": "enter",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         # "text": config.WELCOME_PROMPT.replace("{user}", danmu.sender.name),
#         "text": config.WELCOME_PROMPT.replace("{user}", "观众"),
#         "id": "99999",
#         "name": "观众",
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time())
#     }
#     print("收到入场消息：" + str(danmu_dict))
#     # 随机概率执行
#     if random.random() > config.INTERACT_MESSAGES_RANDOM:
#         print("Interact message random rate limit reached, ignore this message, id=" + str(
#             "99999") + " name=" + "观众")
#         return
#     # 判断条件
#     current_time = time.time()
#     if current_time - value.interact_last_append_time <= 60 and value.interact_messages_appended >= config.MAX_INTERACT_MESSAGES_PER_MINUTE:
#         print("Interact message rate limit reached, ignore this message, id=" + str(
#             "99999") + " name=" + "观众")
#         return
#     else:
#         value.interact_last_append_time = current_time
#         value.interact_messages_appended = 1
#     value.msg_queue.append(danmu_dict)
#
#
# @value.room.on(Events.SEND_GIFT)
# async def on_gift(ctx: BLiverCtx):
#     """
#     收到礼物
#     :param ctx:
#     :return:
#     """
#     danmu = DanMuMsg(ctx.body)
#     danmu_dict = {
#         "multi": "false",
#         "type": "gift",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         "text": config.THANKS_FOR_GIFT_PROMPT.replace("{user}", danmu.sender.name).replace("{gift}", danmu.content),
#         "id": str(danmu.sender.id),
#         "name": danmu.sender.name,
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time()),
#     }
#     print("收到礼物：" + str(danmu_dict))
#     value.msg_queue.append(danmu_dict)
#
#
# def init_danmaku(loop):
#     """
#     初始化弹幕库并保活
#     :return:
#     """
#     print("Init danmaku library.")
#     while True:
#         try:
#             loop.create_task(value.room.listen())
#             loop.run_forever()
#             print("弹幕库退出，等待5s运行")
#         except:
#             traceback.print_exc()
#             print("弹幕库出现了奇怪的错误，等待5s运行")
#         time.sleep(5)
#
# @value.room.on('INTERACT_WORD')
# async def on_enter(event):
#     """
#     观众进入直播间
#     :param event:
#     :return:
#     """
#     # 随机概率执行
#     if random.random() > config.INTERACT_MESSAGES_RANDOM:
#         print("Interact message random rate limit reached, ignore this message, id=" + str(
#             event["data"]["data"]["uid"]) + " name=" + event["data"]["data"]["uname"])
#         return
#     # 判断条件
#     current_time = time.time()
#     if current_time - value.interact_last_append_time <= 60 and value.interact_messages_appended >= config.MAX_INTERACT_MESSAGES_PER_MINUTE:
#         print("Interact message rate limit reached, ignore this message, id=" + str(
#             event["data"]["data"]["uid"]) + " name=" + event["data"]["data"]["uname"])
#         return
#     else:
#         value.interact_last_append_time = current_time
#         value.interact_messages_appended = 1
#
#     danmu_dict = {
#         "multi": "false",
#         "type": "enter",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         "text": config.WELCOME_PROMPT.replace("{user}", event["data"]["data"]["uname"]),
#         "id": str(event["data"]["data"]["uid"]),
#         "name": event["data"]["data"]["uname"],
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time())
#     }
#     value.msg_queue.append(danmu_dict)
#
#
# @value.room.on('SEND_GIFT')
# async def on_gift(event):
#     """
#     收到礼物
#     :param event:
#     :return:
#     """
#     # 收到礼物
#
#     danmu_dict = {
#         "multi": "false",
#         "type": "gift",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         "text": config.THANKS_FOR_GIFT_PROMPT.replace("{user}", event["data"]["data"]["uname"]),
#         "id": str(event["data"]["data"]["uid"]),
#         "name": event["data"]["data"]["uname"],
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time()),
#     }
#     value.msg_queue.append(danmu_dict)
#
#
# @value.room.on('DANMU_MSG')
# async def on_danmaku(event):
#     """
#     收到弹幕
#     :param event:
#     :return:
#     """
#
#     danmu_dict = {
#         "multi": "false",
#         "type": "danmaku",
#         "modelId": config.MULTI_ID,
#         "modelName": config.MULTI_NAME,
#         "text": event["data"]["info"][1],
#         "id": str(event["data"]["info"][2][0]),
#         "name": event["data"]["info"][2][1],
#         "msgId": ''.join(random.choice("123456789") for _ in range(8)),
#         "steps": "-1",
#         "timestamp": str(time.time()),
#     }
#     # 替换中文符号
#     danmu_dict["text"] = danmu_dict["text"].replace("：", ":", 1).replace("＃", "#", 1)
#     # 避免机器人发送的弹幕被检测到
#     if danmu_dict["id"] == str(config.BILI_USER_UID) and (
#             config.TEXT_IGNORE_DANMAKU in danmu_dict["text"] or config.TEXT_DANMAKU_SAVED in danmu_dict[
#         "text"] or config.TEXT_THINKING in
#             danmu_dict["text"]):
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_ROBOT + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict["name"])
#         return
#
#     # 指定忽略的用户
#     if danmu_dict["id"] in config.IGNORED_USERS:
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IGNORE_USER + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict["name"])
#         return
#
#     # 弹幕是否合法
#     if utils.is_valid_msg(danmu_dict):
#         while len(value.msg_queue) >= config.MAX_DANMAKU_QUEUE_LENGTH and time.time() - float(
#                 value.msg_queue[0]["timestamp"]) > 60.0:
#             msg_temp = value.msg_queue.pop(0)
#             print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_DELETE_EARLY_DANMAKU + "): text=" + msg_temp[
#                 "text"] + " id=" +
#                   msg_temp["id"] + " name=" + msg_temp["name"])
#             send_danmaku(f"{config.TEXT_IGNORE_DANMAKU}: {config.TEXT_QUEUE_LIMITED}")
#
#         # 检测是否为聊天信息或指令
#         if not utils.is_cmd_or_msg(danmu_dict):
#             print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_IS_NOT_MSG_ALERT + "): text=" + danmu_dict[
#                 "text"] + " id=" +
#                   danmu_dict["id"] + " name=" + danmu_dict["name"])
#             return
#         # 去除前缀
#         danmu_dict["text"] = danmu_dict["text"].replace(config.CONFIG_MATCH_COMMAND, "", 1)
#         value.msg_queue.append(danmu_dict)
#         print(config.TEXT_DANMAKU_SAVED + ": text=" + danmu_dict["text"] + " id=" + danmu_dict["id"] + " name=" +
#               danmu_dict[
#                   "name"])
#         send_danmaku(config.TEXT_DANMAKU_SAVED_ALERT)
#     else:
#         print(config.TEXT_IGNORE_DANMAKU + "(" + config.TEXT_QUEUE_SAME_MSG + "): text=" + danmu_dict["text"] + " id=" +
#               danmu_dict[
#                   "id"] + " name=" + danmu_dict[
#                   "name"])
#         send_danmaku(config.TEXT_QUEUE_SAME_MSG_ALERT)
#
#
# def disconnect():
#     try:
#         sync(value.room.disconnect())
#     except:
#         pass
#
#
# def connect():
#     try:
#         sync(value.room.connect())
#     except:
#         pass
#
#
# def init_danmaku():
#     """
#     初始化弹幕库并保活
#     :return:
#     """
#     print("Init danmaku library.")
#     threading.Thread(target=connect).start()
#     isOutput = True
#     while True:
#         time.sleep(1)
#         try:
#             if value.room.get_status() == 2:
#                 if isOutput:
#                     print("Danmaku library status: Connected.")
#                 isOutput = False
#                 continue
#             isOutput = True
#             print("Danmaku library status: " + str(value.room.get_status()) + ", we'll check the connection...")
#             if value.room.get_status() == 0:
#                 # 重新初始化
#                 print("Danmaku library status: 0, reconnecting...")
#                 threading.Thread(target=init_danmaku).start()
#                 return
#             if value.room.get_status() == 1:
#                 # 连接建立中
#                 print("Danmaku library status: 1, waiting for connection to be established...")
#                 i = 0
#                 while True:
#                     i += 1
#                     if value.room.get_status() == 2:
#                         break
#                     if value.room.get_status() == 5 or i > 100:
#                         if value.room.get_status() == 5:
#                             print("Danmaku library appears to error, status: 5, please pay attention.")
#                         # 断开连接
#                         threading.Thread(target=disconnect).start()
#                         # 重新初始化
#                         threading.Thread(target=init_danmaku).start()
#                         return
#                     time.sleep(1)
#                 continue
#             if value.room.get_status() == 3:
#                 # 断开连接中
#                 print("Danmaku library status: 3, waiting for disconnection...")
#                 i = 0
#                 while True:
#                     i += 1
#                     if value.room.get_status() == 4:
#                         # 重新初始化
#                         print("Danmaku library status: 4, disconnect, now reinitializing...")
#                         threading.Thread(target=init_danmaku).start()
#                         return
#                     if value.room.get_status() == 5 or i > 100:
#                         if value.room.get_status() == 5:
#                             print("Danmaku library appears to error, status: 5, please pay attention.")
#                         # 断开连接
#                         threading.Thread(target=disconnect).start()
#                         # 重新初始化
#                         threading.Thread(target=init_danmaku).start()
#                         return
#                     time.sleep(1)
#             if value.room.get_status() == 4:
#                 # 重新初始化
#                 print("Danmaku library status: 4, disconnect, now reinitializing...")
#                 threading.Thread(target=init_danmaku).start()
#                 return
#             if value.room.get_status() == 5:
#                 print("Danmaku library appears to error, status: 5, please pay attention.")
#                 # 断开连接
#                 threading.Thread(target=disconnect).start()
#                 # 重新初始化
#                 threading.Thread(target=init_danmaku).start()
#                 return
#         except:
#             traceback.print_exc()
#             continue
