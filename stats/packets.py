"""Packet formatter functions."""


def timer_packet(name, value):
    """Return a timer formatted packet."""
    return packet(
        name,
        int(value * 1000),
        'ms',
    )


def counter_packet(name, value):
    """Return a counter formatted packet."""
    return packet(name, str(value), 'c')


def gauge_packet(name, value):
    """Return a gauge formatted packet."""
    return packet(name, str(value), 'g')


def set_packet(name, value):
    """Return a set formatted packet."""
    return packet(name, value, 's')


def packet(name, value, suffix):
    """Return a formatted packet.

    General utility function, to build other formatters on top of.
    """
    return '{name}:{value}|{suffix}'.format(
        name=name,
        value=str(value),
        suffix=suffix,
    ).encode()
