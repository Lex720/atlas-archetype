import json
import sys
from typing import TypeVar

from loguru import logger

TBase = TypeVar("Base")


def sink_serializer(message: TBase) -> None:
    """Formats the data into the necessary structure for the logger to print."""
    record = message.record
    simplified = {
        "tag": record["extra"]["tag"],
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "msg": record["message"],
        "file": record["file"].name,
        "line": record["line"],
        "level": record["level"].name.lower(),
    }
    print(json.dumps(simplified), file=sys.stdout, flush=True)


def configure_logging() -> None:
    """Removes default logger and add new serialized one."""
    logger.remove()
    logger.add(sink_serializer)
