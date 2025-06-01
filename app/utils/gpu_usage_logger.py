import time
import threading
from pynvml import *

def start_gpu_monitoring(interval=1):
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)

    def monitor():
        while monitoring_flag:
            mem_info = nvmlDeviceGetMemoryInfo(handle)
            util = nvmlDeviceGetUtilizationRates(handle)
            print(f"[GPU Monitor] Util: {util.gpu}% | Mem: {mem_info.used // (1024 ** 2)}MB / {mem_info.total // (1024 ** 2)}MB")
            time.sleep(interval)

    global monitoring_flag
    monitoring_flag = True
    thread = threading.Thread(target=monitor)
    thread.start()
    return thread

def stop_gpu_monitoring():
    global monitoring_flag
    monitoring_flag = False
    nvmlShutdown()
