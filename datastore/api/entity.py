from core.dashboard_apps.api import ApiResource
from datastore.ext import ext_context
from datastore.ext.model import ExtKey, ExtModel

from .ext_helper import ExtHelper
from .url_helpers import build_chain_urls


class Entity(ApiResource):
    # /apps/<app>/namespaces/<namespace>/kinds/<kind>/entities/<entity>/data
    urls = build_chain_urls('app', 'namespace', 'kind', 'entity', direct=True)
    # /apps/<app>/kinds/<kind>/entities/<entity>/data
    urls += build_chain_urls('app', 'kind', 'entity', direct=True)

    def get(self, kind, entity, **kwargs):
        key = ExtKey(urlsafe=entity, _context=ext_context, **ExtHelper.partition_data(**kwargs))
        entity = key.get()
        return entity

    def post(self, kind, entity, **kwargs):
        key = ExtKey(urlsafe=entity, _context=ext_context, **ExtHelper.partition_data(**kwargs))
        entity = ExtModel(_kind=kind, _context=ext_context)
        #entity.
        pass

    put = post

    def delete(self, entity, **kwargs):
        key = ExtHelper.key_from_urlsafe(entity)
        key.delete()


ALL_RESOURCES = [Entity]
