import yaml
import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def load_config(config_path = os.path.join(os.getcwd(), "config/config.yaml")):
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            database = config.get("database")
            return database
    
    except FileNotFoundError:
        raise FileNotFoundError(
            "Config file not found"
        )
    except Exception as e:
        raise Exception(
            f"Unexpected error: {e}"
        )


def setup_logging(
    log_dir: str = "logs",
    log_file: str | None = None,
    level: str | None = None,
) -> logging.Logger:
    """Minimal logging to console + logs/ (rotating file).

    Environment variables:
    - LOG_LEVEL (default: INFO)
    - LOG_FILE (default: app.log)
    """

    resolved_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    resolved_log_file = log_file or os.getenv("LOG_FILE", "app.log")

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / resolved_log_file

    root_logger = logging.getLogger()
    root_logger.setLevel(resolved_level)

    # Avoid duplicate handlers when re-running in the same interpreter.
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(resolved_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(resolved_level)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    root_logger.debug("Logging initialized -> %s", str(log_path))
    return root_logger