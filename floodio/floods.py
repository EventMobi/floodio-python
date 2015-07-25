# -*- coding: utf-8 -*-

try:
    import urllib.parse as urlp
except ImportError:
    import urlparse as urlp

from dateutil.parser import parse

from .grids import Grid


class Flood(object):

    def __init__(self, response, client=None):
        self._client = client
        self.uuid = response['uuid']
        if response['started']:
            self.started = parse(response['started'])
        else:
            self.started = None
        if response['stopped']:
            self.stopped = parse(response['stopped'])
        else:
            self.stopped = None
        self.grids = []
        for grid in response['_embedded']['grids']:
            self.grids.append(Grid(grid))

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.uuid)

    @property
    def report(self):
        url = '%s/api/floods/%s/report' % (self._client._base_url, self.uuid)
        report_data = self._client._session.get(url).json()
        return Report(report_data)

    @property
    def result(self):
        url = '%s/api/floods/%s/result' % (self._client._base_url, self.uuid)
        return self._client._session.get(url).json()

    def repeat(self, region=None, grid=None):
        url = '%s/api/floods/%s/repeat' % (self._client._base_url, self.uuid)
        params = {}
        if region:
            params['region'] = region
        if grid:
            params['grid'] = grid
        flood_resp = self._client._session.get(url, params=params).json()
        return Flood(flood_resp, client=self._client)

    def stop(self):
        url = '%s/api/floods/%s/stop' % (self._client._base_url, self.uuid)
        resp_data = self._client._session.get(url).json()
        self.__init__(resp_data, client=self._client)

    def refresh(self):
        url = '%s/api/floods/%s' % (self._client._base_url, self.uuid)
        resp_data = self._client._session.get(url).json()
        self.__init__(resp_data, client=self._client)


class Report(object):

    def __init__(self, data):
        del data['_links']
        for attr, value in data.items():
            setattr(self, attr, value)


class Floods(object):

    _endpoint = '/api/floods'

    def __init__(self, client):
        self._client = client

    def __getitem__(self, flood_id):
        endpoint = self._endpoint + '/' + flood_id
        url = urlp.urljoin(self._client._base_url, endpoint)
        flood_resp = self._client._session.get(url).json()
        return Flood(flood_resp, client=self._client)

    def all(self):
        """ Iterator returning all available floods. """
        for flood in self._get_page():
            yield Flood(flood)
        next_page = self._next_page()
        while next_page:
            for flood in self._get_page(next_page):
                yield Flood(flood)
            next_page = self._next_page()

    def create(self, tool, flood_files, name=None, notes=None, tag_list=None,
               privacy='private', threads=None, rampup=None, duration=None,
               override_hosts=None, override_parameters=None, grids=None):

        # Validation
        assert tool in ['jmeter-2.13', 'gatling-2.1.4']
        assert privacy in ['private', 'public']

        # TODO: post the flood
        self._client._session.post(
            files=flood_files,
            data={
            },
        )
        return Flood()

    def _next_page(self):
        return self._last_page['_links'].get('next', {}).get('href')

    def _get_page(self, link=None):
        """ Get a page of Flood data """
        url = urlp.urljoin(self._base_url, link or self._endpoint)
        floods_resp = self._client._session.get(url).json()
        self._last_page = floods_resp
        return floods_resp['_embedded']['floods']


__all__ = ['Floods']
