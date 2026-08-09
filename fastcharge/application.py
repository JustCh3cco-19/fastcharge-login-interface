"""Coordinamento del ciclo di vita dell'applicazione."""

import logging
import threading

from fastcharge.services.notifier import monitor_log
from fastcharge.ui.interface import run_interface


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    monitor_thread = threading.Thread(
        target=monitor_log,
        daemon=True,
        name="email-notifier",
    )
    monitor_thread.start()
    run_interface()
