# -*- coding: utf-8 -*-

from dateutil.parser import parse

from . import exc
from .grids import Grid


class Flood(object):

    def __init__(self, response, client=None):
        self._client = client
        self.grids = []
        self._status = response.pop('status')
        for grid in response['_embedded']['grids']:
            self.grids.append(Grid(grid))
        del response['_embedded']
        del response['_links']
        for attr, value in response.items():
            setattr(self, attr, value)
        if response['started']:
            self.started = parse(response['started'])
        if response['stopped']:
            self.stopped = parse(response['stopped'])

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

    @property
    def status(self):
        if self._status != 'finished':
            self.refresh()
        return self._status

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
        url = "%s%s" % (self._client._base_url, endpoint)
        flood_resp = self._client._session.get(url).json()
        if flood_resp.get('error'):
            raise exc.ResourceNotFound(flood_resp['error'])
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

        data = {
            'flood[tool]': tool,
            'flood[privacy]': privacy,
        }
        files = self._build_files(flood_files)
        if name:
            data['flood[name]'] = name
        if notes:
            data['flood[notes]'] = notes
        if tag_list:
            data['flood[tag_list]'] = ",".join(tag_list)
        if threads:
            data['flood[threads]'] = threads
        if rampup:
            data['flood[rampup]'] = rampup
        if duration:
            data['flood[duration]'] = duration
        if override_hosts:
            data['flood[override_hosts]'] = override_hosts
        if override_parameters:
            data['flood[override_parameters]'] = override_parameters
        if grids:
            data['flood[grids][][uuid]'] = grids

        url = self._client._base_url + self._endpoint
        response = self._client._session.post(url, files=files, data=data)
        return Flood(response.json(), client=self._client)

    def _build_files(self, flood_files):
        return [
            ('flood_files[]', file)
            for file in flood_files
        ]

    def _next_page(self):
        return self._last_page['_links'].get('next', {}).get('href')

    def _get_page(self, link=None):
        """ Get a page of Flood data """
        url = "%s%s" % (self._base_url, link or self._endpoint)
        floods_resp = self._client._session.get(url).json()
        self._last_page = floods_resp
        return floods_resp['_embedded']['floods']


__all__ = ['Floods']
