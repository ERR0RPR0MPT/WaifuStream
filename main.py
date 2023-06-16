
import sys
import config
import multiprocess
import nlp
import process
import value
import server
import utils
import danmaku
import os
import time
import signal
import threading


if __name__ == '__main__':
    sys.stdout.write(f"\x1b]2;{config.SHELL_TITLE}\x07")
    utils.init_ws()
    threading.Thread(target=process.execute).start()
    threading.Thread(target=multiprocess.multiprocess).start()
    threading.Thread(target=server.start_http_server).start()
    threading.Thread(target=danmaku.init_danmaku).start()
    time.sleep(0.75)
    utils.clear_console()
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
            elif inp.startswith("chat:"):
                if inp[5:] == "":
                    print("Please enter the content of the chat.")
                    continue
                if inp[5:] == "+reset":
                    value.chat_dict[0] = nlp.ChatGPT(config.SYSTEM_PROMPT)
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
            elif inp.startswith("image:"):
                print("Set image: " + inp[6:])
                utils.set_trans_image_url(config.EMOTION_IMAGE_URL + inp[6:])
            else:
                print("Unknown command. Please try again.")
                continue
        except KeyboardInterrupt:
            print("")
            continue

# chat:大家好，今天直播间到场有哪些人呢？报一下名字吧！