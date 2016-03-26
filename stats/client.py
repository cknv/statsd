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

    <key>:<value>|ms
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix
        self._value = None
        self._intermediate = None

    def _send(self, key, value):
        """Send a timer off."""
        if key is None:
            self.client.send(
                packets.timer_packet(
                    self.prefix,
                    value,
                )
            )
        else:
            self.client.send(
                packets.timer_packet(
                    dot_join(self.prefix, key),
                    value,
                )
            )

    def start(self):
        """Start the timer."""
        self._value = time.time()
        return self

    def intermediate(self, key=None):
        """Send an intermediate time."""
        since = self._intermediate or self._value
        self._send(key, time.time() - since)
        self._intermediate = time.time()

    def stop(self, key='total'):
        """Stop the timer."""
        self._send(key, time.time() - self._value)
        self._value = None


class Counter:
    """Counter class.

    <key>:<value>|c
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix

    def increment(self, key, count):
        """Increment the counter."""
        self.client.send(
            packets.counter_packet(
                dot_join(self.prefix, key),
                count,
            )
        )

    def decrement(self, key, count):
        """Decrement the counter."""
        self.increment(key, -count)

    def from_mapping(self, mapping):
        """Send many values at once from a mapping."""
        parts = (
            packets.counter_packet(
                dot_join(self.prefix, key),
                count,
            )
            for key, count in mapping.items()
        )
        self.client.send(b'\n'.join(parts))


class Gauge:
    """Gauge class.

    <key>:<value>|g
    """

    def __init__(self, client, prefix):
        """Return a new counter."""
        self.client = client
        self.prefix = prefix

    def set(self, key, value):
        """Set the current value of the gauge."""
        line = packets.gauge_packet(dot_join(self.prefix, key), value)
        self.client.send(line)


# class Set(StatsClient):

#     """Set class

#     <key>:<value>|s
#     """

#     def add(self, key, value):
#         """Add a value to the set."""
#         self._send(packets.set_packet(key, value))
