from subprocess import Popen, PIPE, TimeoutExpired


def _mount_unmount(mountDir:str , mount_timeout: int, mount=True, lazy=False, log=lambda x: x) -> bool:
    process = "mount" if mount else "unmount"
    args = ["mount" if mount else "umount", mountDir]
    if not mount and lazy:
        args.insert(1, '-l')
    
    log(f"{process.capitalize()}ing network share at '{mountDir}'...")
    proc = Popen(args, text=True, stdout=PIPE, stderr=PIPE)
    success = False
    try:
        proc.wait(mount_timeout)
        success = True
    except TimeoutExpired as te:
        log(str(te), f'Timeout {"un" if not mount else ""}mounting network share')
    except Exception as err:
        stderr = proc.stderr.readlines()
        if not stderr:
            log(str(err), "Exception")
            return False
        if stderr and not mount and "Host is down":
            return True
        log(f"Could not {process} network share")
        [log(err, f"Error {process}ing") for err in proc.stderr.readlines()]
    finally:
        proc.kill()
        proc.stderr.close()
        proc.stdout.close()
    
    
    if success:
        log(f"Successfully {process}ed network share")
    return success
            
            
def mount(mountDir:str , mount_timeout: int, log=lambda x: x) -> bool:
    return _mount_unmount(mountDir, mount_timeout, log=log)


def unmount(mountDir:str , mount_timeout: int, log=lambda x: x) -> bool:
    def _unmount() -> bool:
        return _mount_unmount(mountDir, mount_timeout, mount=False, log=log)
    def _lazy_unmount() -> bool:
        log("Lazily unmounting network share...")
        return _mount_unmount(mountDir, mount_timeout, mount=False, lazy=True, log=log)
    return _unmount() or _lazy_unmount()