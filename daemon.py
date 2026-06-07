from __future__ import annotations

import atexit 
import logging
import os
import signal
import sys
import time 
from pathlib import Path
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def _write_pid(pid_path: str) -> None:
    Path(pid_path).parent.mkdir(parents=True, exist_ok=True)
    Path(pid_path).write_text(str(os.getpid()) + "\n" , encoding="utf-8")


def _read_pid(pid_path: str) -> Optional[int]:

    try:
        return int(Path(pid_path).read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        return None


def _remove_pid(pid_path: str) -> None:
    try:
        Path(pid_path).unlink()

    except FileNotFoundError:
        pass 




def _pid_is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False




class Daemon:

    def __init__(
            self,
            pid_file: str,
            run_fn: Callable[[], None],
            reload_fn: Optional[Callable[[], None]]=None,
            ) -> None:
            self._pid_file = pile_file
            self._run_fn = run_fn
            self._reload_fn = reload_fn
            self._shutdown_requested = False


    def start(self, foreground: bool = False) -> None:

        existing_pid = _read_pid(self._pid_file)
        if existing_pid and _pid_is_alive(existing_pid):
            print("netguard is already running ", file=sys.stderr)
            sys.exit(1)

        print("netguard is starting")

        if foreground:
            self._setup_signals()
            _write_pid(self._pid_file)
            atexit.register(_remove_pid, self._pid_file)
            self._run_fun()
        else:
            self._daemonise()

    def stop(self) -> None:

        pid = _read_pid(self._pid_file)
        if not pid or not _pid_is_alive(pid):
            print("netguard is not running ", file=sys.stderr)
            _remove_pid(self._pid_file)
            sys.exit(1)

        print(f"net guard stopping me from gooning :( ")
        os.kill(pid, signal.SIGTERM)

        
        for _ in range(20):
            time.sleep(0.5)
            if not _pid_is_alive(pid):
                print("netguard stopped ")
                return 

        print("netguard process did not stop ", file=sys.stderr)
        os.kill(pid, signal.SIGKILL)


    def restart(self) -> None:
        self.stop()
        time.sleep(1)
        print(f"restarting the daemon service ")
        self.start()

    def status(self) -> None:

        pid = _read_pid(self._pid_file_)
        if pid and _pid_is_alive(pid):
            print("Firewall is running ")

        else:
            print("netguard is not running ")

    
    def relaod(self) -> None:
        pid = _read_pid(self._pid_file)
        if not pid or not _pid_is_alive(pid):
            print("firewall is not working", file=sys.stderr)
            sys.exit(1)
        os.kill(pid, signal.SIGHUP)
        print(f"sent SIGHUP to pid")



    def _daemonise(self) -> None:

        try:
            pid = os.fork()
        except OSError as exc:
            logger.error("first fork failed %s", exc)
            sys.exit(1)

        if pid > 0:

            sys.exit(0)


        os.chdir("/")
        os.setsid()
        os.umask(0)


        try:
            pid = os.fork()
        except OSError as exc:
            logger.error("second fork failed %s", exc)
            sys.exit(1)

        if pid > 0:
            sys.exit(0)


        self._redirect_streams()
        self._setup_signals()

        _write_pid(self._pid_file)
        atexit.register(_remove_pid, self._pid_file)

        logger.info("Daemon started ", os.getpid())
        self._run_fn()


    def _redirect_streams(self) -> None:

        sys.stdout.flush()
        sys.stderr.flush()

        with open(os.devnull, "r") as devnull_r:
            os.dup2(devnull_r.fileno(), sys.stdin.fileno())

        with open(os.devnull, "a") as devnull_w:
            os.dup2(devnull_w.fileno(), sys.stdout.fileno())
            os.dup2(devnull_w.fileno(), sys.stderr.fileno())

    def _setup_signals(self) -> None:

        signal.signal(signal.SIGTERM, self._handle_sigterm)
        signal.signal(signal.SIGINT, self._handle_sigterm)
        signal.signal(signal.SIGHUP, self._handle_sighup)
        signal.signal(signal.SIGUSR1, self._handle_siguser1)


    def _handle_sigterm(self, signum: int, frame) -> None:
        logger.info("Recieved signal %d - shutting down ", signum)
        self._shutdown_requested = True

        raise KeyboardInterrupt
    

    def _handle_sighup(self, signum: int, frame) -> None:
        logger.info("recieves SIGHUP - reloading blocklist")
        if self._reload_fn:
            try:
                self._reload_fn()

            except Except as exc:
                logger.error("Reload failed : %s", exc)



    def _handle_sigusr1(self, signum:int, frame) -> None:

        logger.info("Recieved SIGUSR1 - rotating logs ")
        log.info("---LOG ROTATION MARKER ----")






   


            

