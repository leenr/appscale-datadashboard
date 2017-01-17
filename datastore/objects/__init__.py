from base64 import b64encode
from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata as ndb_metadata

from .metadata import class_serializers as metadata_class_serializers

from ..ext.model import ExtKey, ExtModel


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

    elif isinstance(value, (ndb.Model, dict)):
        if isinstance(value, ndb.Model):
            value_info = serialize_entity(value)

    elif isinstance(value, ndb.Key):
        type_name = 'key'

        value = serialize_entity_key(value)
        if entity and entity.key:
            if value['app'] == entity.key.app():
                del value['app']

            if 'namespace' in value and value.get('namespace', '') == entity.key.namespace():
                del value['namespace']
            elif entity.key.namespace() == '':
                value['namespace'] = ''

    elif isinstance(value, users.User):
        type_name = 'user'

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


def serialize_property_info(prop, entity):
    compressed = getattr(prop, '_compressed', None)
    indexed = prop._indexed
    repeated = prop._repeated

    data_info = prop._data_info
    meaning = data_info.meaning  # see ext.model.ExtModel
    meaning_id = data_info.meaning_id  # see ext.model.ExtModel
    data_type = data_info.data_type  # see ext.model.ExtModel

    res = {}
    res['data_type'] = data_type
    res['indexed'] = indexed
    if compressed:
        res['compressed'] = True
    if repeated:
        res['repeated'] = True
    if meaning:
        res['meaning'] = meaning
        res['meaning_id'] = meaning_id

    return res


def _serialize_entity(entity, _data, _properties):
    for db_property in entity._properties.values():
        if isinstance(db_property, ndb.StructuredProperty):
            subentity = db_property._get_user_value(entity)
            _serialize_entity(subentity, _data, _properties)
            continue

        db_base_value = db_property._get_base_value(entity)
        data_info = db_property._data_info
        property_name = data_info.name

        _properties[property_name] = serialize_property_info(db_property, entity=entity)
        _data[property_name] = serialize_entity_value(db_base_value, entity=entity)

def serialize_entity(entity):
    data = {}
    properties = {}

    _serialize_entity(entity, data, properties)

    return {
        'key': entity._key,
        'data': data,
        'properties': properties,
    }


def serialize_entity_key(key):
    res = {
        'app': key.app(),
        'pairs': key.pairs(),
        'urlsafe': key.urlsafe(),
    }

    if key.namespace():
        res['namespace'] = key.namespace()

    return res


class_serializers = {
    ExtModel: serialize_entity,
    ndb.Key: serialize_entity_key,
}

class_serializers.update(metadata_class_serializers)


def api_serialize_obj(obj):
    for base_type, serializer in class_serializers.items():
        if isinstance(obj, base_type):
            res = serializer(obj)
            if res is not NotImplemented:
                return res

    if isinstance(obj, object):
        for func_name in ('_to_api', '_to_dict', 'to_dict'):
            serializer_func = getattr(obj, func_name, None)
            if callable(serializer_func):
                res = serializer_func()
                if res is not NotImplemented:
                    return res

    return NotImplemented
