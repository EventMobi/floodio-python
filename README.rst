==============
floodio-python
==============

A Flood.io client for Python 2 and 3.

Installation
============

.. code:: sh

    $ pip install floodio-python

Usage
=====

Instantiate a client with your Flood API key:

.. code:: python

    from floodio.client import Client
    
    client = Client('YOURAPIKEY')

Flood API
---------

:code:`client.floods` is iterable:

.. code:: python

    for flood in client.floods:
        print(flood)

or you can get a flood by its uuid:

.. code:: python

    flood = client.floods['SOMEUUID']
    
A flood has :code:`stop`, :code:`repeat`, and :code:`refresh` methods.

.. code:: python

    flood.stop()
    # keyword arguments are optional.
    flood.repeat(grid='SOMEGRIDUUID', region='AWSREGION')
    flood.refresh()  # pulls the latest state of this flood

Accessing :code:`flood.status` performs an implicit refresh.

.. code:: python

    flood.status
    >>> 'queued'
    flood.status
    >>> 'running'
    flood.status
    >>> 'finished'
    
Condensed results are available with :code:`flood.report`.

.. code:: python

    flood.report.summary
    flood.report.mean_response_time
    flood.report.mean_concurrency
    flood.report.mean_throughput
    flood.report.mean_error_rate
    flood.report.mean_apdex
    
and the detailed results are available with :code:`flood.results`, directly loading the JSON-response.

Any times returned by `Flood API V2`_ are parsed into native Python datetime objects.
eg. :code:`flood.started` and :code:`flood.ended`.

You can create a new flood with :code:`client.floods.create`. Test files are a list of two-tuples
with a filename, and either a file-like object or a string.

.. code:: python

    flood = client.floods.create(
        'jmeter-2.13',
        [('test.jmx', your_test_data)],
        name='client-test',
        duration=300,
        threads=200,
        rampup=300,
        grids='SOMEGRIDUUID',
    )

Grid API
--------

.. _Flood API V2: https://help.flood.io/docs/flood-api
