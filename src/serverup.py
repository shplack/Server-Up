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
        if "Host Unreachable" not in cpe.output:
            log(str(cpe), 'CalledProcessError')
        return False
    except KeyboardInterrupt:
        log('Keyboard interrupt')
        stop_server()
        quit()
    

def wait_for_online() -> None:
    log('Checking if host is up')
    log('Pinging host...')
    while not ping(p_on_count): pass
    log(f'Host [{host}] is up!')


def wait_for_offline() -> None:
    log('Waiting for host to go down')
    log('Pinging host...')
    while ping(p_off_count): pass
    log(f'Host [{host}]went down!')


def stop_server():
    log('Stopping...', 'Server')
    remove_containers(dockerfile, log)
    unmount(mountDir, mount_timeout, log)
    log('Stopped', 'Server')
    
    
def start_server():
    log('Starting...', 'Server')
    if not start_containers(dockerfile, log) or \
        not mount(mountDir, mount_timeout, log):
        quit()
    log('Started', 'Server')
