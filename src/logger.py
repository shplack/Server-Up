import os
from io import FileIO
from time import strftime, localtime
from config import logDir, logfileName

_logFile: FileIO


def now():
    return strftime("%H:%M:%S", localtime())


def _init_log():
    global _logFile
    
    if not os.path.exists(logDir):
        os.makedirs(logDir)
        if not os.path.exists(logDir):
            print(f"Unable to create directory '{logDir}'")
        
    if not os.access(logDir, os.W_OK):
        print(f"Check write permissions for '{logDir}'")
        quit()
    
    _logFile = open(logDir + logfileName, "a")
    _logFile.write(f'\n----------------------------Started [{logfileName}] at: [{strftime("%Y/%m/%d")} {now()}]----------------------------\n')
    
    
def log(msg: str, header=''):
    output = f'[{now()}] '
    if header:
        output += f'{header}: '
    output += msg
    if not _logFile.writable():
        print(f"Unable to write to logfile: '{logDir + logfileName}'")
    else:
        _logFile.write(output + '\n')
        _logFile.flush()
    print(output)
    
    
_init_log()