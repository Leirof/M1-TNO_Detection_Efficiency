import os
#from numba import njit, objmode
term_size = os.get_terminal_size().columns

lastProgressPrinted : int = -1
lastBarPrinted : int = -1

def printr(string): print(string,end="\r")

def progressbar(progress: float, prefix = "", stop:bool=False) -> None:
    global lastBarPrinted, lastProgressPrinted
    currentProgress = int(progress*100)
    margin = len(prefix) + 7
    currentBar = int(progress*(term_size-margin))
    if not (currentProgress == lastProgressPrinted and currentBar == lastBarPrinted):
        if stop: print(f"{prefix}[{'='*currentBar}{' '*(term_size-margin-currentBar)}] {currentProgress}%", end="\r")
        else   : print(f"{prefix}[{'='*currentBar}{' '*(term_size-margin-currentBar)}] {currentProgress}%")
    lastProgressPrinted = currentProgress
    lastBarPrinted = currentBar

N = 1000
for i in range(N):
    progressbar(i/N)