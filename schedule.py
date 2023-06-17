import time
import traceback
import config
import utils


def schedule():
    start_time_h = int(config.STREAM_SCHEDULE["START_TIME"].split(":")[0])
    start_time_m = int(config.STREAM_SCHEDULE["START_TIME"].split(":")[1])
    stop_time_h = int(config.STREAM_SCHEDULE["STOP_TIME"].split(":")[0])
    stop_time_m = int(config.STREAM_SCHEDULE["STOP_TIME"].split(":")[1])
    print(f"Schedule task: Set Start time: {str(start_time_h)}:{str(start_time_m)}")
    print(f"Schedule task: Set Stop time: {str(stop_time_h)}:{str(stop_time_m)}")
    while True:
        try:
            time.sleep(59)
            now = time.localtime()
            if now.tm_hour == start_time_h and now.tm_min == start_time_m:
                print("Schedule task: Start stream.")
                utils.start_stream()
            if now.tm_hour == stop_time_h and now.tm_min == stop_time_m:
                print("Schedule task: Stop stream.")
                utils.stop_stream()
        except:
            traceback.print_exc()
            print("Error.")
