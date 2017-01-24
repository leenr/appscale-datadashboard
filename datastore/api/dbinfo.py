from google.appengine.ext.ndb import metadata as ndb_metadata

from core.dashboard_apps.api import ApiResource

from .ext_helper import ExtHelper
from .url_helpers import build_chain_urls


class Namespaces(ApiResource):
    # /apps/<app>/namespaces/
    urls = build_chain_urls('app', 'namespace')

    def get(self, app):
        return [namespace.namespace_name for namespace in ExtHelper.query_for(ndb_metadata.Namespace).fetch()]


class Kinds(ApiResource):
    # /apps/<app>/namespaces/<namespace>/kinds/
    urls = build_chain_urls('app', 'namespace', 'kind')
    # /apps/<app>/kinds/
    urls += build_chain_urls('app', 'kind')

    def get(self, app, namespace=None):
        return ExtHelper.get_kinds()


class Properties(ApiResource):
    # /apps/<app>/namespace/<namespace>/kinds/<kind>/properties/
    urls = build_chain_urls('app', 'namespace', 'kind', 'property')
    # /apps/<app>/kinds/<kind>/properties/
    urls += build_chain_urls('app', 'kind', 'property')

    def get(self, app, kind, namespace=None):
        return ExtHelper.get_kind(kind).get_result().properties


ALL_RESOURCES = [Namespaces, Kinds, Properties]
