from datastore.ext.model import ExtModel, ExtKey
from datastore.objects.entity_key import serialize_entity_key
from datastore.objects.entity_property import serialize_property_info, unserialize_property_info_into
from datastore.objects.entity_value import serialize_entity_value, unserialize_entity_value


def serialize_entity(entity):
    data = {}
    properties = {}

    for db_property in entity._properties.values():
        db_base_value = db_property._get_base_value(entity)
        data_info = db_property._data_info
        property_name = data_info.name

        properties[property_name] = serialize_property_info(db_property, entity=entity)
        data[property_name] = serialize_entity_value(db_base_value, entity=entity)

    return {
        'key': entity._key,
        'data': data,
        'properties': properties,
    }


def unserialize_entity_to(entity, api_data):
    data = api_data.get('data')
    properties = api_data.get('properties')

    for prop_name, property_info in properties.iteritems():
        api_value = data.get(prop_name)
        ndb_property = unserialize_property_info_into(entity, prop_name, property_info)
        ndb_value = unserialize_entity_value(ndb_property, api_value, entity=entity)
        ndb_property._set_value(entity, ndb_value)

    return entity


class_serializers = {
    ExtModel: serialize_entity,
    ExtKey: serialize_entity_key,
}
