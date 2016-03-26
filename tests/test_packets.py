"""Test that the packet formatting function works as intended."""
from stats import packets


def test_timer_packet():
    """Assert timer_packet works."""
    assert packets.timer_packet('name', 15) == b'name:15000|ms'


def test_counter_packet():
    """Assert counter_packet works."""
    assert packets.counter_packet('name', 15) == b'name:15|c'


def test_counter_packet_negative():
    """Assert counter_packet works, also with negative numbers."""
    assert packets.counter_packet('name', -15) == b'name:-15|c'


def test_gauge_packet():
    """Assert gauge_packet works."""
    assert packets.gauge_packet('name', 15) == b'name:15|g'


def test_set_packet():
    """Assert set_packet works."""
    assert packets.set_packet('name', 15) == b'name:15|s'
