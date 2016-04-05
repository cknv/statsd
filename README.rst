Stats
=====

A simple library for sending `StatsD metrics <https://github.com/etsy/statsd/blob/master/docs/metric_types.md>`_ in python. It aims to provide a high level API for the user, however that also means that much of the lower level functionality found in most ofther StatsD clients are not exposed, frankly because I do not find that I need it. So no manually timing things and etc.

Use it like so:

.. code-block:: python

    import stats

    my_client = stats.StatsClient(prefix, host, port)

For development, the client also provides a ``disabled`` kwarg, so you do not have change anything in the code when you want to not send stats:

.. code-block:: python

    my_client = stats.StatsClient(prefix, host, port, disabled=True)

By itself, the client does not provide much use, but it does provide easy ways to get specific sub-clients, such as timers, counters, etc.

Timing
------

.. code-block:: python

    timer = my_client.timer('my-timer-name').start()

    this_takes_a_while()
    timer.intermediate('first-pass')

    this_takes_a_while()
    timer.intermediate('second-pass')
    timer.stop()

Counting
--------

.. code-block:: python

    counter = my_client.counter('my-counter-name')

    counter.increment('some-value', 10)
    counter.decrement('some-other-value', 10)

The counter can even be fed a dict like object, such as the Counter from the standard library and send the stats as a single message.

.. code-block:: python

    pre_counted = {
        'a-name': 5,
        'another-name': 10,
    }

    counter.from_mapping(pre_counted)

Gauges
------

For setting the current value.

.. code-block:: python

    gauge = my_client.gauge('my-gauge')

    gauge.set('a-name', 10)
    gauge.update('a-name', 10)

Sets
----

For counting unique events, such as unique users on a page.

.. code-block:: python

    visitors = my_client.set('visitors')
    visitors.add('ids', user.id)

Custom
------

In case the server you are using supports more metric types than this library, you can send raw metrics:

.. code-block:: python

    my_client.send('metric.name', value)
