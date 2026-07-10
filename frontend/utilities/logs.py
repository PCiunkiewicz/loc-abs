"""System logging utilities."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Literal, get_args

import loguru
from loguru import logger

if TYPE_CHECKING:
    from utilities.types.system import Writable

LogLevel = Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']

LOGGER_FORMAT = (
    '<light-black>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-black> | '
    '<level><bold>{level: >8}</bold></level> | '
    '<black>{path: >36}</black> | : '
    '<level>{message}</level>\n'
)

LEVEL_COLOR: dict[LogLevel, str] = {
    'TRACE': '<magenta>',
    'DEBUG': '<cyan>',
    'INFO': '<black><bold>',
    'SUCCESS': '<green><bold>',
    'WARNING': '<yellow><bold>',
    'ERROR': '<red><bold>',
    'CRITICAL': '<RED><bold>',
}


def configure_logger(level: LogLevel = 'SUCCESS', file: Writable | None = None) -> None:
    """Configure the logger with a specific level."""
    logger.remove()
    logger.add(sys.stderr, level=level, format=formatter)
    if file:
        logger.add(file, level=level, format=formatter)

    for loglevel in get_args(LogLevel):
        logger.level(loglevel, color=LEVEL_COLOR[loglevel])


def formatter(record: loguru.Record) -> str:
    """Format the log message based on the level."""
    record['path'] = f'{Path(*Path(record["file"].path).parts[-2:])}:{record["line"]}'
    return LOGGER_FORMAT
