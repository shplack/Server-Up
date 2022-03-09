from config import *
from logger import log
from docker_client import remove_containers, start_containers
import subprocess
from mount import mount, unmount


def ping(count: str) -> bool:
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
    log(f"Waiting for {host} to come online...")
    while not ping(p_on_count): pass
    log(f"Host {host} is up!")


def wait_for_offline() -> None:
    log(f"Waiting for {host} to go offline...")
    while ping(p_off_count): pass
    log(f"Host {host} went down!")


def stop_server():
    log('Stopping...', 'Server')
    remove_containers(dockerfile, docker_timeout, log)
    unmount(mountDir, mount_timeout, log)
    log('Stopped', 'Server')
    
    
def start_server():
    log('Starting...', 'Server')
    if not mount(mountDir, mount_timeout, log) or \
        not start_containers(dockerfile, docker_timeout, log):
        stop_server()
        quit()
    log('Started', 'Server')
