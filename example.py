# -*- encoding: utf-8 -*-
# ! python3

import logging

import click

from click_loguru.decorators import verbosity_multi_decorator
from click_loguru.intercept import setup_command_loguru

logger = logging.getLogger(__name__)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@verbosity_multi_decorator
@setup_command_loguru
def hello(**_):
    """
    Foo bar
    """
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    raise NotImplementedError()


if __name__ == "__main__":
    hello()
