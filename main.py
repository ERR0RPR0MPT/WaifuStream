
import config
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
    utils.init_ws()
    threading.Thread(target=process.execute).start()
    threading.Thread(target=server.start_http_server).start()
    threading.Thread(target=danmaku.init_danmaku).start()
    time.sleep(0.75)
    utils.clear_console()
    print(f"Server started at http://localhost:{str(config.SERVER_PORT)}")
    while True:
        try:
            inp = input("root@WaifuStream:~# ")
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
            elif inp.startswith("chat:"):
                print("Chat: " + inp[5:])
                danmu_dict = {
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
