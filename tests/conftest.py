"""Fixtures for testing."""
import random
import socketserver
import threading
import time

import pytest

import charcoal


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """Mixin for handling connections asynchronsly."""


class Listener(socketserver.BaseRequestHandler):
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
        cls.received.clear()


@pytest.yield_fixture(scope='session')
def listener():
    """Setup the listener for tests."""
    server_address = ('localhost', 8125)
    server = ThreadedUDPServer(server_address, Listener)
    # ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield Listener

    server.shutdown()
    server.server_close()


@pytest.fixture(scope='function')
def client():
    """Client for tests."""
    return charcoal.StatsClient('mystats')


@pytest.fixture(scope='function', autouse=True)
def fix_seed():
    """Fix the random seed, so randomness in tests is predictable."""
    random.seed('my fixed seed')
