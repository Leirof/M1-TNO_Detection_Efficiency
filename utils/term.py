import os
term_size = os.get_terminal_size().columns

lastProgressPrinted : int = -1
lastBarPrinted : int = -1

def progressbar(progress: float, prefix = "", stop:bool=False) -> None:
    global lastBarPrinted, lastProgressPrinted
    
    progress = max(min(progress,100),0)
    currentProgress = int(progress*100)
    margin = len(prefix) + 8
    currentBar = int(min(progress*(term_size-margin),term_size-margin))
    currentProgress = int(min(progress*100,100))
    if not (currentProgress == lastProgressPrinted and currentBar == lastBarPrinted):
        if not stop and progress < 1: print(f"{prefix}[{'='*currentBar}{' '*(term_size-margin-currentBar)}] {currentProgress}%", end="\r")
        else:print(f"{prefix}[{'='*currentBar}{' '*(term_size-margin-currentBar)}] {currentProgress}%")
    lastProgressPrinted = currentProgress
    lastBarPrinted = currentBar