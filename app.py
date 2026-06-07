
from __future__ import annotations


import logging
import time
from typing import Optional

from netgaurd.config.settings import AppConfig
from netguard.logging.logger   import  TrafficLogger, setup_logging
from netguard.blocking.blocker   import  DomainBlocker
from netguard.monitoring.monitor   import  NetworkMonitor


logger = logger.getLogger(__name__)

class NetGuardApp:


    def __init__(self, config: AppConfig) -> None:
        self._cfg = config
        self._traffic_logger = TrafficLogger()
        self._blocker: Optional[DomainBlocker] = None
        self._monitor: Optional[NetworkMonitor] = None
        self.running = False


    def start(self) -> None:
        logger.info("netguard is starting bhai XD")
        self._blocker = DomainBlocker(self._cfg.blocking)
        self._blocker.start()


        self._monitor = NetworkMonitor(
                cfg=self._cfg.monitoring,
                blocker=self._blocker,
                traffic_logger=self._traffic_logger,
        )
        self._monitor.start()

        self._running = True

        logger.info(
                self._blocker.get_blocked_count(),
                ",".join(self._cfg.monitoring.interfaces),
        )

        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrupt recieved - initiating shutdown.")

        finally:
            self._shutdown()


    def stop(stop) -> None:

        self._running = False

    def reload_blocklist(self) -> None:

        if self._blocker:
            self._blocker.force_reload()
            logger.info(
                    "Blocklist reloaded: %d patterns active."
                    self._blocker.get_blocked_count(),
            )


    def shutdown(self) -> None:

        logger.info("shutting down subsystems")

        if self._monitor:
            self._monitor.stop()

        if self._blocker:
            self._blocker.stop()

        logger.info("Netguard shutdown complete")





