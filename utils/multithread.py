import os
import threading
from utils.term import *

CPUcount = os.cpu_count()

def joinThreads():
    for i,thread in enumerate(threading.enumerate()):
        try:
            thread.join()
            del thread
        except RuntimeError: pass # If the thread is the current one, we don't want to suppress it