from flask import request

from core.dashboard_apps.api import ApiResource
from datastore.ext import ext_context
from datastore.ext.model import ExtKey, ExtModel
from datastore.objects.entity import unserialize_entity_to

from .ext_helper import ExtHelper
from .url_helpers import build_chain_urls


class Entity(ApiResource):
    # /apps/<app>/namespaces/<namespace>/kinds/<kind>/entities/<entity>/data
    urls = build_chain_urls('app', 'namespace', 'kind', 'entity', direct=True)
    # /apps/<app>/kinds/<kind>/entities/<entity>/data
    urls += build_chain_urls('app', 'kind', 'entity', direct=True)

    def entity_key(self, urlsafe=None, pairs=None, **kwargs):
        return ExtKey(urlsafe=urlsafe, pairs=pairs, _context=ext_context, **ExtHelper.partition_data(**kwargs))

    def get(self, kind, entity, **kwargs):
        key = self.entity_key(urlsafe=entity, **kwargs)
        entity = key.get()
        return entity

    def post(self, kind, entity, **kwargs):
        key = self.entity_key(urlsafe=entity, **kwargs)
        entity = ExtModel(_kind=kind, key=key, _context=ext_context)
        unserialize_entity_to(entity, request.json)
        entity.put()
        return entity

    def put_entity(self, kind, **kwargs):
        if 'key_pairs' in request.json:
            key = self.entity_key(pairs=request.json['key_pairs'], **kwargs)
        else:
            key = self.entity_key(kind, None, **kwargs)
        entity = ExtModel(_kind=kind, key=key, _context=ext_context)
        unserialize_entity_to(entity, request.json)
        entity.put()
        return entity

    def delete(self, entity, **kwargs):
        key = self.entity_key(urlsafe=entity, **kwargs)
        key.delete()
        return {}


ALL_RESOURCES = [Entity]
