"""Full end to end tests using an actual UDP listener."""
from freezegun import freeze_time


def test_timer(client, listener):
    """Test a timer."""
    with freeze_time('2016-03-26 12:00:00') as frozen_datetime:
        timer = client.timer('mytimer').start()
        frozen_datetime.tick()
        timer.intermediate('halfway')
        frozen_datetime.tick()
        timer.intermediate('done')
        timer.stop()

    assert list(listener.load_received()) == [
        b'mystats.mytimer.halfway:1000|ms',
        b'mystats.mytimer.done:1000|ms',
        b'mystats.mytimer.total:2000|ms',
    ]


def test_timer_reuse(client, listener):
    """Test that after stopping a timer it can be reused."""
    with freeze_time('2016-03-26 12:00:00') as frozen_datetime:
        timer = client.timer('mytimer').start()
        frozen_datetime.tick()
        timer.intermediate('halfway')
        frozen_datetime.tick()
        timer.intermediate('done')
        timer.stop()

    assert list(listener.load_received()) == [
        b'mystats.mytimer.halfway:1000|ms',
        b'mystats.mytimer.done:1000|ms',
        b'mystats.mytimer.total:2000|ms',
    ]

    with freeze_time('2016-03-26 18:00:00') as frozen_datetime:
        timer.start()
        frozen_datetime.tick()
        timer.intermediate('halfway')
        frozen_datetime.tick()
        timer.intermediate('done')
        timer.stop()

    assert list(listener.load_received()) == [
        b'mystats.mytimer.halfway:1000|ms',
        b'mystats.mytimer.done:1000|ms',
        b'mystats.mytimer.total:2000|ms',
    ]


def test_timer_manual_measurements(client, listener):
    """Test that the timer supports premeasured times."""
    timer = client.timer('mytimer')

    timer.send('something', 10)
    timer.send('something', 15)

    assert list(listener.load_received()) == [
        b'mystats.mytimer.something:10000|ms',
        b'mystats.mytimer.something:15000|ms',
    ]


def test_timer_sampling(client, listener):
    """Test timers, with sampling works as intended."""
    with freeze_time('2016-03-26 12:00:00') as frozen_datetime:
        timer = client.timer('mytimer').start()
        frozen_datetime.tick()
        timer.intermediate('halfway')
        frozen_datetime.tick()
        timer.intermediate('done')
        timer.stop()

    assert list(listener.load_received()) == [
        b'mystats.mytimer.halfway:1000|ms',
        b'mystats.mytimer.done:1000|ms',
        b'mystats.mytimer.total:2000|ms',
    ]


def test_counter(client, listener):
    """Test a counter."""
    counter = client.counter('mycounter')

    counter.increment('a', 5)
    counter.increment('b', 1)
    counter.increment('c', 15)

    assert set(listener.load_received()) == {
        b'mystats.mycounter.a:5|c',
        b'mystats.mycounter.b:1|c',
        b'mystats.mycounter.c:15|c',
    }


def test_counter_from_mapping(client, listener):
    """Test a counter ability to use a dict like object."""
    counter = client.counter('mycounter')

    counted_values = {
        'a': 5,
        'b': 1,
        'c': 15,
    }
    counter.from_mapping(counted_values)

    assert set(listener.load_received()) == {
        b'mystats.mycounter.a:5|c',
        b'mystats.mycounter.b:1|c',
        b'mystats.mycounter.c:15|c',
    }


def test_counter_sampling(client, listener):
    """Test counting, with sampling works as intended."""
    counter = client.counter('mycounter')

    for i in range(20):
        counter.increment('a', i, sample=0.2)

    assert set(listener.load_received()) == {
        b'mystats.mycounter.a:8|c|@0.2',
        b'mystats.mycounter.a:6|c|@0.2',
        b'mystats.mycounter.a:2|c|@0.2',
        b'mystats.mycounter.a:13|c|@0.2',
        b'mystats.mycounter.a:4|c|@0.2',
        b'mystats.mycounter.a:1|c|@0.2',
    }


def test_gauge_set(client, listener):
    """Test setting a gauge."""
    gauge = client.gauge('mygauge')

    gauge.set('value', 5)
    gauge.set('value', 5)
    gauge.set('value', 10)

    assert list(listener.load_received()) == [
        b'mystats.mygauge.value:5|g',
        b'mystats.mygauge.value:5|g',
        b'mystats.mygauge.value:10|g',
    ]


def test_gauge_update(client, listener):
    """Test updating a gauge."""
    gauge = client.gauge('mygauge')

    gauge.set('value', 10)
    gauge.update('value', 5)
    gauge.update('value', -5)
    gauge.set('value', -10)

    assert list(listener.load_received()) == [
        b'mystats.mygauge.value:10|g',
        b'mystats.mygauge.value:+5|g',
        b'mystats.mygauge.value:-5|g',
        b'mystats.mygauge.value:0|g',
        b'mystats.mygauge.value:-10|g',
    ]


def test_set(client, listener):
    """Test adding to a set."""
    uniques = client.set('myset')

    uniques.add('value', 5)
    uniques.add('value', 5)
    uniques.add('value', 10)

    assert list(listener.load_received()) == [
        b'mystats.myset.value:5|s',
        b'mystats.myset.value:5|s',
        b'mystats.myset.value:10|s',
    ]
