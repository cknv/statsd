"""Packet formatter functions."""
from random import random


def timer_packet(name, value):
    """Return a timer formatted packet."""
    yield from packet(
        name,
        int(value * 1000),
        'ms',
    )


def counter_packet(name, value, sample=None):
    """Return a counter formatted packet."""
    yield from packet(name, str(value), 'c', sample)


def gauge_set_packet(name, value):
    """Return a gauge formatted packet."""
    if value < 0:
        yield from packet(name, '0', 'g')

    yield from packet(name, str(value), 'g')


def gauge_update_packet(name, value):
    """Return a gauge formatted packet."""
    if value >= 0:
        value = '+{}'.format(value)
    yield from packet(name, str(value), 'g')


def set_packet(name, value):
    """Return a set formatted packet."""
    yield from packet(name, value, 's')


def packet(name, value, suffix, sample=None):
    """Return a formatted packet.

    General utility function, to build other formatters on top of.
    """
    if sample is None:
        yield '{name}:{value}|{suffix}'.format(
            name=name,
            value=str(value),
            suffix=suffix,
        )
    else:
        if sample >= random():
            yield '{name}:{value}|{suffix}|@{sample}'.format(
                name=name,
                value=str(value),
                suffix=suffix,
                sample=sample
            )
