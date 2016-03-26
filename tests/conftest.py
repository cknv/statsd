"""Fixtures for testing."""
import pytest
import stats

import time
import threading
import socketserver


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """Mixin for handling connections asynchronsly."""


class Collector(socketserver.BaseRequestHandler):

    received = []

    def handle(self):
        data = self.request[0].strip()
        self.received.extend(data.split(b'\n'))

    @classmethod
    def load_received(cls, wait=0.01):
        """Yield from the received stats

        But only after a slight delay, otherwise they might not all be there.
        """
        time.sleep(wait)
        yield from cls.received


@pytest.yield_fixture(scope='function')
def listener():
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
    return stats.StatsClient('mystats')


@pytest.fixture(scope='function')
def mocked_client(mocker):
    """Mock the client."""
    client = stats.StatsClient('mystats')
    client.send = mocker.MagicMock()
    return client



