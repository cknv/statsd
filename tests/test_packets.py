"""Test that the packet formatting function works as intended."""
import pytest

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


@pytest.mark.parametrize('case, expected', [
    (15, b'name:15|g'),
    (-15, b'name:0|g\nname:-15|g'),
    (0, b'name:0|g'),
])
def test_gauge_set_packet(case, expected):
    """Assert gauge_set_packet works."""
    assert packets.gauge_set_packet('name', case) == expected


@pytest.mark.parametrize('case, expected', [
    (15, b'name:+15|g'),
    (-15, b'name:-15|g'),
])
def test_gauge_update_packet(case, expected):
    """Assert gauge_update_package works."""
    assert packets.gauge_update_packet('name', case) == expected


def test_set_packet():
    """Assert set_packet works."""
    assert packets.set_packet('name', 15) == b'name:15|s'
