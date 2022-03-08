import atexit
from config import *
from logger import log
from docker_client import remove_containers, start_containers
import subprocess
from mount import mount, unmount


def ping(count) -> bool:
    try:
        process = subprocess.run(
            ['ping', '-c', count, host], 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        process.check_returncode()
        return True
    except subprocess.CalledProcessError as cpe:
        log(cpe.stderr, 'CalledProcessError')
        return False
    except KeyboardInterrupt:
        # TODO stop server
        pass
    

def wait_for_online() -> None:
    log('Checking if host is up')
    log('Pinging host...')
    while not ping(): pass
    log(f'Host [{host}] is up!')


def wait_for_offline() -> None:
    log('Waiting for host to go down')
    log('Pinging host...')
    while ping(64): pass
    log(f'Host [{host}]went down!')


def stop_server():
    log('Stopping server...')
    remove_containers(dockerfile, log)
    unmount(mountDir, mount_timeout, log)
    quit()
    
    
atexit.register(stop_server)