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


def gauge_set_packet(name, value):
    """Return a gauge formatted packet."""
    if value >= 0:
        return packet(name, str(value), 'g')
    else:
        return packet(name, 0, 'g') + b'\n' + packet(name, str(value), 'g')


def gauge_update_packet(name, value):
    """Return a gauge formatted packet."""
    if value >= 0:
        value = '+{}'.format(value)
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
