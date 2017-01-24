from google.appengine.ext import ndb

from datastore.ext.model import ExtModel, ExtKey
from datastore.objects.entity_key import serialize_entity_key
from datastore.objects.entity_property import serialize_property_info
from datastore.objects.entity_value import serialize_entity_value


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


class_serializers = {
    ExtModel: serialize_entity,
    ExtKey: serialize_entity_key,
}
