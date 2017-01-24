from datastore.ext.model import ExtModel, ExtKey
from datastore.objects.entity_key import serialize_entity_key
from datastore.objects.entity_property import serialize_property_info
from datastore.objects.entity_value import serialize_entity_value


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


class_serializers = {
    ExtModel: serialize_entity,
    ExtKey: serialize_entity_key,
}
