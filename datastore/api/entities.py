import json

from flask import request
from google.appengine.ext import ndb

from core.dashboard_apps.api import ApiResource

from ..ext.model import ExtKey
from ..ext.query import do_query_iter
from .url_helpers import build_chain_urls


ORDER_SIGNS = {
    '+': ndb.model.datastore_query.PropertyOrder.ASCENDING,
    '-': ndb.model.datastore_query.PropertyOrder.DESCENDING,
}

def parse_order_expr(expr):
    order = ORDER_SIGNS.get(expr[0], ndb.model.datastore_query.PropertyOrder.ASCENDING)
    prop_name = expr.strip(''.join(ORDER_SIGNS.keys()))
    return ndb.model.datastore_query.PropertyOrder(prop_name, order)

class Entities(ApiResource):
    # /apps/<app>/namespaces/<namespace>/kinds/<kind>/entities/
    urls = build_chain_urls('app', 'namespace', 'kind', 'entity')
    # /apps/<app>/kinds/<kind>/entities/
    urls += build_chain_urls('app', 'kind', 'entity')

    def get(self, app, kind, namespace=None):
        offset = request.args.get('offset', 0)
        if offset:
            offset = int(offset)

        limit = request.args.get('limit', 50)
        if limit:
            limit = int(limit)

        ancestor = request.args.get('ancestor_json', None)
        if ancestor:
            ancestor = ndb.Key(app=app, namespace=namespace, **json.loads(ancestor))

        start_cursor = request.args.get('cursor', None)
        if start_cursor:
            start_cursor = ndb.Cursor(urlsafe=start_cursor)

        filters = request.args.get('filters_json', None)
        if filters:
            filters = map(lambda pairs: ndb.FilterNode(*pairs), json.loads(filters))

        key = request.args.get('key_json', None)
        if key:
            key = ndb.Key(app=app, namespace=namespace, **json.loads(key))
            if not filters:
                filters = []
            filters.append(ndb.FilterNode('__key__', '=', key))

        projection = request.args.get('projection', None)
        if projection:
            projection = projection.split(',')

        orders = request.args.get('orders', None)
        if orders:
            orders = map(parse_order_expr, orders.split(','))
            if len(orders) > 0:
                orders = ndb.model.datastore_query.CompositeOrder(orders)

        group_by = request.args.get('group_by', None)
        if group_by:
            group_by = group_by.split(',')

        query = ndb.Query(kind=kind, ancestor=ancestor, filters=ndb.ConjunctionNode(*filters) if filters else None, orders=orders, app=app, namespace=namespace, group_by=group_by, projection=projection)
        count = query.count()

        if count:
            entities_iter = do_query_iter(query, start_cursor=start_cursor, offset=offset, limit=limit)
            entities = list(entities_iter)
        else:
            entities = []
            entities_iter = None

        return {
            'count': count,
            'entities': entities,
            'next_cursor': entities_iter.cursor_after().urlsafe() if entities_iter and entities_iter.probably_has_next() else None,
        }

ALL_RESOURCES = [Entities]
