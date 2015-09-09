# -*- coding: utf-8 -*-


class ResourceNotFound(Exception):
    pass


class ResourceCreationFailed(Exception):
    pass


class FloodCreationFailed(ResourceCreationFailed):
    pass


class GridCreationFailed(ResourceCreationFailed):
    pass
