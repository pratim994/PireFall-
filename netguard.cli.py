from __future__ import annotations

import argparse

import sys
import os


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from netguard.config.setting import AppConfig
from netguard.logging.logger import setup_logging
from netguard.core.app import NetGuardApp
from netguard.core.daemon import Daemon


DEFAULT_CONFIG = "/etc/netguard/config.yaml"


def _buid_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
            prog="netguard",
            description="firewall daemon .",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__doc__,
    )
    parser.add_argument(
        "command",
        choices["start", "stop", "restart", "status", "reload"],
        help="Deamon lifecycle command .",
    )

    parser.add_argument(
            "--config",
            default=DEFAULT_CONFIG,
            metavar="PATH",
            help=f"Path to YAML config file (default: {default config})."
    )

    parser.add_argument(
            "--foreground", "-f",
            action="store_true".
            help="Run in the foreground no daemonisation "
    )

    return parser

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        cfg = AppConfig.from_file(args.config)

    except FileNotFoundError:
        if args.command in ("start", "restart"):
            print(
                f"[netguard] config file not found: {args.config}\n"
                ,file=sys.stderr,
            )
            cfg = AppConfig()

        else:
            print(f"netguard config file not found : {args.config}", file=sys.stderr)

    except (ValueError, Exception) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)


    setup_logging(cfg.logging)

    app = NetGuardApp(cfg)

    daemon = Daemon(
            pid_file=cfg.daemon.pid_file,
            run_fn=app.start,
            relaod_fn=app.reload_blocklist,
    )

    command = args.command

    if command == "start":
        daemon.start(foreground=args.foreground)
            
    elif command == "stop":
        daemon.stop()

    elif command == "restart":
        daemon.restart()

    elif command == "reload":
        daemon.reload()

    elif command == "status":
        daemon.status()

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()





            
