# -*- coding: utf-8 -*-

from . import exc


class Grid(object):

    def __init__(self, data, client=None):
        self._client = client
        del data['_links']
        for attr, value in data.items():
            setattr(self, attr, value)

    def __repr__(self):
        return "<%s:%s>" % (self.__class__.__name__, self.uuid)

    def delete(self):
        """ Delete this Grid. """
        url = '%s/api/grids/%s' % self.uuid
        data = self._client._session.delete(url).json()
        self.__init__(data, self._client)


class Grids(object):

    _endpoint = '/api/grids'

    def __init__(self, client):
        self._client = client

    def __getitem__(self, grid_id):
        endpoint = self._endpoint + '/' + grid_id
        url = self._client._base_url + endpoint
        grid_resp = self._client._session.get(url).json()
        if grid_resp.get('error'):
            raise exc.ResourceNotFound(grid_resp['error'])
        return Grid(grid_resp, client=self._client)

    def all(self):
        url = '%s%s' % (self._client._base_url, self._endpoint)
        grids_resp = self._client._session.get(url).json()
        for grid in grids_resp['_embedded']['grids']:
            yield Grid(grid)

    def create(self, region, infrastructure, account_credential_id,
               instance_quantity, instance_type, stop_after,
               aws_spot_price=None, aws_tags=None, aws_availability_zone=None,
               aws_vpc_identifier=None, aws_vpc_subnet_public=None,
               aws_vpc_subnet_private=None, aws_vpc_security_groups=None):

        url = self._client._base_url + self._endpoint

        # Validation
        assert region in ['ap-southeast-2', 'us-east-1', 'us-west-1',
                          'us-west-2', 'eu-west-1', 'eu-central-1',
                          'ap-southeast-1', 'ap-northeast-1', 'sa-east-1']
        assert infrastructure in ['demand', 'hosted']
        assert instance_type in ['m3.xlarge', 'm3.2xlarge']

        # Required fields
        data = {
            'grid[region]': region,
            'grid[infrastructure]': infrastructure,
            'grid[instance_quantity]': instance_quantity,
            'grid[instance_type]': instance_type,
            'grid[stop_after]': stop_after,
        }

        # Optional fields
        if infrastructure == 'hosted':
            data['grid[account_credential_id]'] = account_credential_id
        if aws_spot_price:
            data['grid[aws_spot_price]'] = aws_spot_price
        if aws_availability_zone:
            data['grid[aws_availability_zone]'] = aws_availability_zone
        if aws_vpc_identifier:
            data['grid[aws_vpc_identifier]'] = aws_vpc_identifier
        if aws_vpc_subnet_public:
            data['grid[aws_vpc_subnet_public]'] = aws_vpc_subnet_public
        if aws_vpc_subnet_private:
            data['grid[aws_vpc_subnet_private]'] = aws_vpc_subnet_private
        if aws_vpc_security_groups:
            data['grid[aws_vpc_security_groups]'] = aws_vpc_security_groups

        grid_resp = self._client._session.post(url, data=data).json()
        if grid_resp.get('error'):
            raise exc.GridCreationFailed(grid_resp['error'])
        return Grid(grid_resp, client=self._client)
