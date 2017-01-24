from base64 import b64encode, b64decode
from datetime import datetime
from functools import partial

from google.appengine.api import users
from google.appengine.ext import ndb

from datastore.ext.model import GenericPropertyWithMeaning, PbMeaning
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


def unserialize_entity_value(ndb_property, value, entity=None):
    if ndb_property._repeated and isinstance(value, list):
        value = map(partial(unserialize_entity_value, ndb_property, entity=entity), value)
    elif ndb_property._compressed:
        value = ndb.model._CompressedValue(b64decode(value))

    if isinstance(ndb_property, ndb.UserProperty):
        value = users.User(
            email=value.get('email'),
            _user_id=value.get('user_id'),
            _auth_domain=value.get('auth_domain', None),
            federated_identity=value.get('federated_identity', None),
            federated_provider=value.get('federated_provider', None),
        )

    elif isinstance(ndb_property, ndb.KeyProperty):
        if 'app' not in value:
            value['app'] = entity.key.app()
        if 'namespace' not in value:
            value['namespace'] = entity.key.namespace()
        value = ndb.Key(**value)

    elif isinstance(ndb_property, GenericPropertyWithMeaning):
        if ndb_property._meaning == PbMeaning.GD_WHEN:
            value = datetime.fromtimestamp(value)

    return value
