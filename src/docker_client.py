from docker import from_env
import subprocess

client = from_env()       


def _start_stop(process: str, args: list, timeout: int, log: callable) -> bool:
    log(f'{process.lower().capitalize()}ing containers...')
    
    proc = subprocess.Popen(
        args=args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
     
    try:
        proc.wait(timeout)
    except subprocess.TimeoutExpired as te:
        log(str(te), f'Timeout {process.lower()}ing containers')
        return False
    except subprocess.CalledProcessError as cpe:
        log(str(cpe), 'CalledProcessError')
        return False
    except Exception as e:
        log(str(e), 'Error')
        return False
    
    
    log(f'Successfully {process.lower()}ed containers')
    return True

def remove_containers(dockerfile: str, docker_timeout: int, log=lambda x: x) -> bool:
    return _start_stop(
        process='stopp',
        args=['docker-compose', '-f', dockerfile, 'down'],
        timeout=docker_timeout,
        log=log
    )
            

def start_containers(dockerfile: str, docker_timeout: int, log=lambda x: x) -> bool:
    return _start_stop(
        process='start',
        args=['docker-compose', '-f', dockerfile, 'up', '-d'],
        timeout=docker_timeout,
        log=log
    )
    
        
    
