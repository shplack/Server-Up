import sys
from docker import DockerClient, from_env, errors
import subprocess

client: DockerClient = None
try:
    client = from_env()
except errors.DockerException as de:
    if 'Permission denied' in str(de):
        print('Do you have permission to use docker?')
    elif 'Connection refused' in str(de):
        print('Do you have docker installed?')
    print(str(de))
    sys.exit(-1)

def _start_stop(process: str, args: list, timeout: int, log: callable) -> bool:
    log(f'{process.lower().capitalize()}ing containers...')
    
    success = False
    
    try:
        proc = subprocess.Popen(
            args=args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        try:
            proc.wait(timeout)
            success = True
            log(f'Successfully {process.lower()}ed containers')
        except subprocess.TimeoutExpired as te:
            log(str(te), f'Timeout {process.lower()}ing containers')
        except subprocess.CalledProcessError as cpe:
            log(str(cpe), 'CalledProcessError')
        except Exception as e:
            log(str(e), 'Error')
        finally:
            proc.kill()
            proc.stderr.close()
            proc.stdout.close()
        
    except FileNotFoundError as fnfe:
        log(str(fnfe), 'FileNotFoundError')
        print("Is docker-compose installed and on path?")
        
    
    return success

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
    
        
    
