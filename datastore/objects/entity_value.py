from base64 import b64encode
from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

from datastore.objects.entity_key import serialize_entity_key


def serialize_entity_value(base_value, entity=None):
    if isinstance(base_value, list):
        return map(serialize_entity_value, base_value)
    elif base_value is None:
        return None

    value = base_value.b_val

    if isinstance(value, ndb.model._CompressedValue):
        value = b64encode(value.z_val)

    elif isinstance(value, list):
        value = [
            serialize_entity_value(subvalue, entity=entity)
            for subvalue in value
        ]

    elif isinstance(value, ndb.Key):
        value = serialize_entity_key(value)
        if entity and entity.key:
            if value['app'] == entity.key.app():
                del value['app']

            if 'namespace' in value and value.get('namespace', '') == entity.key.namespace():
                del value['namespace']
            elif entity.key.namespace() == '':
                value['namespace'] = ''

    elif isinstance(value, users.User):
        value = {
            'user_id': value.user_id(),
            'email': value.email(),
            'auth_domain': value.auth_domain(),
            'federated_identity': value.federated_identity(),
            'federated_provider': value.federated_provider(),
            'nickname': value.nickname(),
        }

    elif isinstance(value, datetime):
        value = (value - datetime(1970, 1, 1)).total_seconds()

    elif isinstance(value, (int, long, float, basestring, type(None), bool)):
        pass

    return value
