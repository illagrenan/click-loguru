# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import functools
import logging
import sys
from typing import NoReturn

from loguru import logger

__all__ = ["InterceptHandler", "loguru_setup", "setup_command_loguru"]


class InterceptHandler(logging.Handler):
    #  https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def loguru_setup(quiet, verbose) -> NoReturn:
    logger.remove()
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logger.add(
        sys.stderr, level=max(logging.WARNING + (quiet - verbose), logging.NOTSET)
    )


def setup_command_loguru(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        loguru_setup(quiet=kwargs.pop("quiet"), verbose=kwargs.pop("verbose"))
        logger.debug("Loguru configured")
        return func(*args, **kwargs)

    return wrapper_do_twice
