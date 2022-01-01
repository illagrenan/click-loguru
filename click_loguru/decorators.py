# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Callable

import click

__all__ = ["verbosity_multi_decorator"]


def verbosity_multi_decorator(func: Callable):
    """
    Verbosity multi-decorator.

    Ref.: https://stackoverflow.com/questions/5409450/can-i-combine-two-decorators-into-a-single-one-in-python
    """

    def _composed(*decs):
        def deco(f):
            for dec in reversed(decs):
                f = dec(f)
            return f

        return deco

    return _composed(
        click.option(
            "-v",
            "--verbose",
            callback=lambda ctx, param, value: value * 10,
            count=True,
            help=(
                "Increase logging verbosity. Can be repeated to increase verbosity even"
                " more."
            ),
        ),
        click.option(
            "-q",
            "--quiet",
            callback=lambda ctx, param, value: value * 10,
            count=True,
            help=(
                "Decrease logging verbosity. Can be repeated to decrease verbosity even"
                " more."
            ),
        ),
    )(func)
