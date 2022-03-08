from docker import from_env
import subprocess
import yaml

client = from_env()


def _get_services_from_file(dockerfile: str) -> list:
    services = []
    with open(dockerfile) as f:
        data: dict = yaml.load(f, Loader=yaml.SafeLoader)
        services = [service for service in data.get('services')]
        f.close()
    return services
    


def _stop_container(container, log=lambda x: x) -> None:
    if container.status == "running":
        log(f"Stopping [{container.name}]")
        container.stop()
        container.reload()
        

def _kill_container(container, log=lambda x: x) -> None:
    if container.status == "running":
        log(f"Killing [{container.name}]")
        container.kill()
        container.reload()
    return container.status == "exited"


def _get_containers_by_name(services: list) -> list:
    containers = []
    for container in client.containers.list():
        if container.name in services:
            containers.append(container)
    return containers
        


def remove_containers(dockerfile: str, log=lambda x: x) -> None:
    log('Stopping containers...')
    services = _get_services_from_file(dockerfile)
    
    if not services:
        log(f"Unable to stop containers, no services found in '{dockerfile}'", 'FileNotFound')
        return
    
    for container in _get_containers_by_name(services):
        _stop_container(container)
    
    for container in _get_containers_by_name(services):
        if not _kill_container(container):
            log(f"Unable to kill [{container.name}]")
            

def start_containers(dockerfile: str, log=lambda x: x):
    log('Starting containers...')
    services = _get_services_from_file(dockerfile)
    
    try:
        subprocess.run(
            ['docker', '-f', dockerfile, 'up', '-d'] + services,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
        not_started = set(services).intersection(set(client.containers.list()))
        if not_started:
            log(f"Unable to start [{'|'.join(not_started)}]")
    except subprocess.CalledProcessError as cpe:
        log('Unable to start docker services')
        log(cpe.stderr, 'CalledProcessError')
        
