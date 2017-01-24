from google.appengine.ext import ndb

from datastore.ext.model import GenericPropertyWithMeaning


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


def unserialize_property_info_into(entity, property_name, property_info):
    data_type = property_info.get('data_type')
    meaning_id = property_info.get('meaning_id', None)
    indexed = property_info.get('indexed')
    repeated = property_info.get('repeated', False)
    compressed = property_info.get('compressed', False)

    common_options = {
        'name': property_name,
        'indexed': indexed,
        'repeated': repeated,
        'compressed': compressed,
    }

    if data_type == 'key':
        property = ndb.KeyProperty(**common_options)
    elif data_type == 'user':
        property = ndb.UserProperty(**common_options)
    elif data_type == 'null':
        property = ndb.GenericProperty(**common_options)
    elif data_type == 'point':
        property = ndb.GeoPtProperty(**common_options)
    else:
        property = GenericPropertyWithMeaning(meaning=meaning_id, **common_options)

    entity._properties[property_name] = property

    return property
