import importlib
import sys
import traceback

import bing
import config
import danmaku
import oa
import value
import utils
import os
import time
import signal


if __name__ == '__main__':
    sys.stdout.write(f"\x1b]2;{config.SHELL_TITLE}\x07")
    utils.clear_console()
    utils.main_init()
    time.sleep(0.75)
    print(f"Server started at http://localhost:{str(config.SERVER_PORT)}\n")
    print(f"If you want to display model images on a web page in OBS Studio or somewhere:")
    print(f"  1. Use http://localhost:{str(config.SERVER_PORT)} to access the translation page.")
    print(f"  2. Use http://localhost:{str(config.SERVER_PORT)}/image/ to access the model image page.\n")
    print(f"Use \"help\" to get help.\n")
    while True:
        try:
            inp = input(f"{config.CONFIG_NAME}@WaifuStream:~# ")
            inp = inp.replace("\n", "")
            if inp == "":
                continue
            elif inp == "help":
                print("Commands:")
                print("  help - Show this message.")
                print("  exit - Exit the program.")
                print("  clear - Clear the console.")
                print("  restart - Restart the program.")
                print("  image:<name> - Set the image.")
            elif inp == "exit":
                print("Exiting...")
                os.kill(os.getpid(), signal.SIGTERM)
            elif inp == "clear":
                utils.clear_console()
            elif inp == "restart":
                print("Restarting...")
                utils.restart()
            elif inp == "multiprocess":
                print("Set multiprocess status: " + str(not config.MULTI_MODE))
            elif inp == "key":
                print("API Keys: ")
                for i in config.OPENAI_API_KEY_LIST:
                    print("\n" + i)
            elif inp == "reload":
                print("Reloading config...")
                importlib.reload(config)
                print("Success")
            elif inp == "start":
                utils.start_stream()
            elif inp == "stop":
                utils.stop_stream()
            elif inp == "danmaku_status":
                print(f"Danmaku status: {value.room.get_status()}")
            elif inp.startswith("chat:"):
                if inp[5:] == "":
                    print("Please enter the content of the chat.")
                    continue
                if inp[5:] == "+reset":
                    if config.MODEL == "openai":
                        value.chat_dict[0] = oa.ChatGPT(config.SYSTEM_PROMPT)
                    elif config.MODEL == "bing":
                        value.chat_dict[0] = bing.BingAI(config.SYSTEM_PROMPT)
                    print("Chat Reset.")
                    continue
                danmu_dict = {
                    "type": "danmaku",
                    "text": inp[5:],
                    "id": "-10000",
                    "name": config.TERMINAL_CHAT_NAME,
                    "timestamp": str(time.time()),
                }
                value.msg_queue.append(danmu_dict)
            elif inp.startswith("c:"):
                if inp[2:] == "":
                    print("Please enter the content of the chat.")
                    continue
                if inp[2:] == "+reset":
                    if config.MODEL == "openai":
                        value.chat_dict[0] = oa.ChatGPT(config.SYSTEM_PROMPT)
                    elif config.MODEL == "bing":
                        value.chat_dict[0] = bing.BingAI(config.SYSTEM_PROMPT)
                    print("Chat Reset.")
                    continue
                danmu_dict = {
                    "type": "danmaku",
                    "text": inp[2:],
                    "id": "-10000",
                    "name": config.TERMINAL_CHAT_NAME,
                    "timestamp": str(time.time()),
                }
                value.msg_queue.append(danmu_dict)
            elif inp.startswith("image:"):
                print("Set image: " + inp[6:])
                utils.set_trans_image_url(config.EMOTION_IMAGE_URL + inp[6:])
            elif inp.startswith("danmaku:"):
                print("Send danmaku: " + inp[8:])
                danmaku.send_danmaku(inp[8:])
            else:
                print("Unknown command. Please try again.")
                continue
        except KeyboardInterrupt:
            continue
        except:
            traceback.print_exc()
            print("Failed. Please check the output.\n")
            continue
