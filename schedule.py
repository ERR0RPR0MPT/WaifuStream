import time
import traceback
import config
import utils


def schedule():
    print(f"Schedule task: Set Start time: "+config.STREAM_SCHEDULE["START_TIME"])
    print(f"Schedule task: Set Stop time: "+config.STREAM_SCHEDULE["STOP_TIME"])
    while True:
        try:
            time.sleep(59)
            now = time.localtime()
            start_time_list = config.STREAM_SCHEDULE["START_TIME"].split("|")
            stop_time_list = config.STREAM_SCHEDULE["STOP_TIME"].split("|")
            for s in start_time_list:
                if len(s.split(":")) != 2:
                    print("Schedule task: Start time format error.")
                    return
                start_time_h = int(s.split(":")[0])
                start_time_m = int(s.split(":")[1])
                if now.tm_hour == start_time_h and now.tm_min == start_time_m:
                    print("Schedule task: Start stream.")
                    utils.start_stream()
                    break
            for s in stop_time_list:
                if len(s.split(":")) != 2:
                    print("Schedule task: Stop time format error.")
                    return
                stop_time_h = int(s.split(":")[0])
                stop_time_m = int(s.split(":")[1])
                if now.tm_hour == stop_time_h and now.tm_min == stop_time_m:
                    print("Schedule task: Stop stream.")
                    utils.stop_stream()
        except:
            traceback.print_exc()
            print("Error.")
