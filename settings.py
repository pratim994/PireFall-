from __future__ import annotations

import os
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import logging


logger = logging.getLogger(__name__)

@dataclass

class LogingConfig:

    log_dir: str = "/var/log/netguard"
    human_log_file: str = "netguard.log"
    json_lof_file: str = "netguard.log"
    max_bytes: int = 10485760
    backup_count: int = 5
    retention_days: int = 30
    level: str = "INFO"


@dataclass
class MonitoringConfig:
    interfaces: List[str] = field(default_factory=lambda: ["eth0"])
    capture_filter: str = ""
    max_packet_queue: int = 1000
    worker_threads: int = 2


@dataclass
class DaemonConfig:
    pid_file: str ="/var/run/netguard.pid"
    user: str = "root"
    group: str = "root"


@dataclass
class AppConfig:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    blocking: BloackingConfig = field(default_factory=BlockingConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    daemon: DaemonConfig = field(default_factory=DaemonConfig)


    @classmethod
    def from_file(cls, path: str) -> "AppConfig":

        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found : {path}")

        with config_path.open("r") as fh:
            raw: dict = yaml.safe_load(fh) or {}

        return cls._from_dict(raw)


    @classmethod
    def _from_dict(cls, raw: dict) -> "AppConfig":

        def _merge(dataclass_interface, section: dict):

            for key, value in section.items():
                if hasattr(dataclass_instance, key):
                    setattr(dataclass_instance, key, value)

                else:
                    logger.warning("Unknown config key ignored %s ", key)

    cfg = cls()

    if "logging" in raw:
        _merge(cfg.logging, raw["logging"])

    if "blocking" in raw:
        _merge(cfg.blocking, raw["blocking"])

    if "monitoring" in raw:
        _merge(cfg.daemon, raw["daemon"])


    cls._validate(cfg)
    return cfg

    @staticmethod
    def _validate(cfg: "AppConfig") -> None:

        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR","CRITICAL"}

        if cfg.logging.level.upper() not in valid_levels:
            raise ValueError(
                f"Invalid log level please stop gooning"
                f"choose form : {valid_levels}"
            )

         
        if cfg.logging.max_bytes < 1024:
            raise ValueError("logging max bytes can be at most 1kb ")

        if cfg.logging.backup_count < 1:
            raise ValueError("logging backup count must be >= 1")

        if cfg.monitoring.worker_threads < 1:
            raise ValueError("monitoring worker threads must be greater than 1 or equal to 1")

        if not cfg.monitoring.interfaces:
            raise ValueError("monitoring interfaces must list at least one interface")

        if cfg.blocking.reload_interval_seconds < 5:
            raise ValueError("blocking.reload_interval_seconds must be >= 5")
