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
