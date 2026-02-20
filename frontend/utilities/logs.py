"""System logging utilities."""

from __future__ import annotations

import contextlib
import json
import os
import sys
from functools import partialmethod
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TextIO, get_args

import loguru
from loguru import logger

if TYPE_CHECKING:
    from utilities.types.system import ClosableAndWritable, OpenTextMode, Writable

LogLevel = Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL', 'PROFILER', 'RELOADER']

LOGGER_FORMAT = (
    '<light-black>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-black> | '
    '<level><bold>{level: >8}</bold></level> | '
    '<black>{path: >36}</black> | : '
    '<level>{message}</level>\n'
)

PROFILER_FORMAT = (
    '<light-black>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-black> | '
    '<level><bold>{level: >8}</bold></level> | '
    '<black>{source: >36}</black> | '
    '<black>{name: >32}</black> | '
    '<black>{ncall: >8}</black> | '
    '<cyan>{tavg: ^8}</cyan> | '
    '<green>{ttot: ^8}</green> | '
    '<light-black>{tsub: ^8}</light-black>\n'
)

HEADER_FORMAT = (
    '\n<black><bold>{label: <62}</bold></black>   '
    '<black><bold>{source: >8}</bold></black>   '
    '<black><bold>{name: >32}</bold></black>   '
    '<bold><black>{ncall: >8}</black></bold>   '
    '<cyan><bold>{tavg: >8}</bold></cyan>   '
    '<green><bold>{ttot: >8}</bold></green>   '
    '<light-black><bold>{tsub: >8}</bold></light-black>\n'
)

RELOADER_FORMAT = (
    '<light-black>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-black> | '
    '<level><bold>RELOADER</bold></level> | '
    '<light-black>{path: >36}</light-black> | : '
    '<level>{message}</level>\n'
)

LEVEL_COLOR: dict[LogLevel, str] = {
    'TRACE': '<magenta>',
    'DEBUG': '<cyan>',
    'INFO': '<black><bold>',
    'PROFILER': '<magenta>',
    'RELOADER': '<magenta>',
    'SUCCESS': '<green><bold>',
    'WARNING': '<yellow><bold>',
    'ERROR': '<red><bold>',
    'CRITICAL': '<RED><bold>',
}

MAX_PATH_CHARS = 30


def configure_logger(level: LogLevel = 'SUCCESS', file: Writable | None = None) -> None:
    """Configure the logger with a specific level."""
    logger.remove()
    logger.add(sys.stderr, level=level, format=formatter)
    if file:
        logger.add(file, level=level, format=formatter)

    for loglevel in ['RELOADER', 'PROFILER']:
        try:
            logger.level(loglevel, no=20, color=LEVEL_COLOR[loglevel])
            setattr(logger.__class__, loglevel.lower(), partialmethod(logger.__class__.log, loglevel))
        except ValueError:
            # If the level already exists, we can just use it
            pass

    for loglevel in get_args(LogLevel):
        logger.level(loglevel, color=LEVEL_COLOR[loglevel])


def formatter(record: loguru.Record) -> str:
    """Format the log message based on the level."""
    if record['level'].name == 'PROFILER':
        record.update(json.loads(record['message']))
        return HEADER_FORMAT if record['source'] == 'source' else PROFILER_FORMAT
    if record['level'].name == 'RELOADER':
        record.update(json.loads(record['message']))
        if len(record['path']) > MAX_PATH_CHARS:
            record['path'] = f'..{record["path"][-(MAX_PATH_CHARS - 2) :]}'
        if record['path']:
            record['path'] = f'file::{record["path"]}'
        return RELOADER_FORMAT
    record['path'] = f'{Path(*Path(record["file"].path).parts[-2:])}:{record["line"]}'
    return LOGGER_FORMAT


class Redirector:
    """Write stdout and stderr to both the terminal and a file."""

    def __init__(self, file: ClosableAndWritable | Path, mode: OpenTextMode = 'a') -> None:
        """Initialize the redirector."""
        self.file = file
        self.mode = mode
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def __enter__(self) -> None:
        """Enter the context manager."""
        if isinstance(self.file, Path):
            self.file = self.file.open(self.mode)

        configure_logger('TRACE', TeeWriter(self.file))
        sys.stdout = TeeWriter(self.stdout, self.file)
        sys.stderr = TeeWriter(self.stderr, self.file)

    def __exit__(self, exc_type: type, exc_value: Exception, traceback: str) -> None:
        """Exit the context manager."""
        configure_logger('TRACE', None)
        sys.stdout.flush()
        sys.stderr.flush()
        self.file.close()

        sys.stdout = self.stdout
        sys.stderr = self.stderr


class TeeWriter:
    """Write to multiple files."""

    def __init__(self, *files: TextIO) -> None:
        """Initialize the tee writer."""
        self.files = files

    def write(self, message: str) -> None:
        """Write the message to all files."""
        for file in self.files:
            if '\033[F\033[K' in message and file.name not in ('<stdout>', '<stderr>'):
                continue
            file.write(message)

    def flush(self) -> None:
        """Flush all files."""
        for file in self.files:
            file.flush()
            with contextlib.suppress(AttributeError, OSError):
                os.fsync(file.fileno())


class NullWriter:
    """Null values passed to `write`."""

    def write[**P](self, *_: P.args) -> None:
        """Do nothing."""
