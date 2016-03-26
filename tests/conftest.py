"""Fixtures for testing."""
import socketserver
import threading
import time

import pytest

import stats


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """Mixin for handling connections asynchronsly."""


class Collector(socketserver.BaseRequestHandler):
    """Simple UDP listener for testing."""

    received = []

    def handle(self):
        """Handle incoming UDP messages."""
        data = self.request[0].strip()
        self.received.extend(data.split(b'\n'))

    @classmethod
    def load_received(cls, wait=0.01):
        """Yield from the received stats.

        But only after a slight delay, otherwise they might not all be there.
        """
        time.sleep(wait)
        yield from cls.received


@pytest.yield_fixture(scope='function')
def listener():
    """Setup the listener for tests."""
    server_address = ('localhost', 8125)
    server = ThreadedUDPServer(server_address, Collector)
    # ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield Collector

    server.shutdown()
    server.server_close()
    Collector.received = []


@pytest.fixture(scope='function')
def client():
    """Client for tests."""
    return stats.StatsClient('mystats')
