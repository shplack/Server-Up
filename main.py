import atexit
from serverup import *

def main():
    try:
        wait_for_online()
        start_server()
        wait_for_offline()
        stop_server()
        main()
    except KeyboardInterrupt:
        stop_server()
        exit()
        
main()

atexit.register(stop_server)