import dotenv
import os


def _get_config(key: str) -> str:
    return dotenv.get_key(dotenv.find_dotenv(), key)


logDir = _get_config('LOGDIR') or 'logs'
if logDir[-1] is not '/':
    logDir += '/'
logfileName = _get_config('LOGFILENAME') or 'serverup.py.log'
mountDir = _get_config('MOUNTDIR')
mount_timeout = int(_get_config('MOUNT_TIMEOUT') or 30)
dockerfile = _get_config('DOCKERFILE')
docker_timeout = int(_get_config('DOCKER_TIMEOUT') or 60)
host = _get_config('HOST')
p_on_count = _get_config('PING_ONLINE_COUNT') or '16'
p_off_count = _get_config('PING_OFFLINE_COUNT') or '128'


if not mountDir:
    print('No mount directory configured')
    quit()
    
if not dockerfile:
    print('No docker-compose.yaml file path configured')
    quit()
    
if not host:
    print('No host configured')
    quit()
    
if not os.access('/'.join(dockerfile.split('/')[:-1]), os.R_OK):
    print(f"Unable to access '{dockerfile}'. Check permissions/path")
    quit()