"""Test that the packet formatting function works as intended."""
import pytest

from charcoal import packets


def test_timer_packet():
    """Assert timer_packet works."""
    assert list(packets.timer_packet('name', 15)) == ['name:15000|ms']


def test_counter_packet():
    """Assert counter_packet works."""
    assert list(packets.counter_packet('name', 15)) == ['name:15|c']


def test_counter_packet_negative():
    """Assert counter_packet works, also with negative numbers."""
    assert list(packets.counter_packet('name', -15)) == ['name:-15|c']


def test_counter_with_sampling():
    """Assert that counter_packet can take an optional sample."""
    assert list(packets.counter_packet('name', 15, sample=1.0)) == ['name:15|c|@1.0']


@pytest.mark.parametrize('case, expected', [
    (15, ['name:15|g']),
    (-15, ['name:0|g', 'name:-15|g']),
    (0, ['name:0|g']),
])
def test_gauge_set_packet(case, expected):
    """Assert gauge_set_packet works."""
    assert list(packets.gauge_set_packet('name', case)) == expected


@pytest.mark.parametrize('case, expected', [
    (15, ['name:+15|g']),
    (-15, ['name:-15|g']),
])
def test_gauge_update_packet(case, expected):
    """Assert gauge_update_package works."""
    assert list(packets.gauge_update_packet('name', case)) == expected


def test_set_packet():
    """Assert set_packet works."""
    assert list(packets.set_packet('name', 15)) == ['name:15|s']
