"""The various clients that help you send stats."""
import socket
import time

from . import packets
from .helpers import dot_join


class StatsClient:
    """Basic stats client.

    Holds some functionality, but is not recommended for direct use.
    """

    def __init__(self, prefix, host=None, port=None, disabled=None):
        """Return a new StatsClient."""
        self.prefix = prefix
        self.port = port or 8125
        self.host = host or 'localhost'
        self.disabled = disabled or False

        if not self.disabled:
            self.socket = self.connect(self.host, self.port)

    def counter(self, suffix):
        """Return a counter."""
        return Counter(
            self,
            dot_join(self.prefix, suffix),
        )

    def timer(self, suffix):
        """Return a timer."""
        return Timer(
            self,
            dot_join(self.prefix, suffix),
        )

    def gauge(self, suffix):
        """Return a gauge."""
        return Gauge(self, dot_join(self.prefix, suffix))

    def set(self, suffix):
        """Return a set."""
        return Set(self, dot_join(self.prefix, suffix))

    def send(self, packet):
        """Send a packet."""
        if self.disabled:
            return

        self.socket.send(packet)

    @staticmethod
    def connect(host, port):
        """Connect to the host."""
        connection_info = (host, port)
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conn.connect(connection_info)
        return conn


class Timer:
    """Timer class.

    <name>:<value>|ms
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix
        self._start = None
        self._intermediate = None

    def _send(self, name, value):
        """Send a timer off."""
        self.client.send(
            packets.timer_packet(
                dot_join(self.prefix, name),
                value,
            )
        )

    def start(self):
        """Start the timer."""
        self._start = time.time()
        return self

    def intermediate(self, name):
        """Send an intermediate time."""
        since = self._intermediate or self._start
        self._send(name, time.time() - since)
        self._intermediate = time.time()

    def stop(self, name='total'):
        """Stop the timer."""
        self._send(name, time.time() - self._start)
        self._start = None


class Counter:
    """Counter class.

    <name>:<value>|c
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix

    def increment(self, name, count):
        """Increment the counter."""
        self.client.send(
            packets.counter_packet(
                dot_join(self.prefix, name),
                count,
            )
        )

    def decrement(self, name, count):
        """Decrement the counter."""
        self.increment(name, -count)

    def from_mapping(self, mapping):
        """Send many values at once from a mapping."""
        parts = (
            packets.counter_packet(
                dot_join(self.prefix, name),
                count,
            )
            for name, count in mapping.items()
        )
        self.client.send(b'\n'.join(parts))


class Gauge:
    """Gauge class.

    <name>:<value>|g
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix

    def set(self, name, value):
        """Set the current value of the gauge."""
        line = packets.gauge_set_packet(dot_join(self.prefix, name), value)
        self.client.send(line)

    def update(self, name, value):
        """Update the current value with a relative change."""
        line = packets.gauge_update_packet(dot_join(self.prefix, name), value)
        self.client.send(line)


class Set:
    """Set class.

    <name>:<value>|s
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix

    def add(self, name, value):
        """Add a value to the set."""
        self.client.send(packets.set_packet(dot_join(self.prefix, name), value))
