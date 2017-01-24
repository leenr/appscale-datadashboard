def serialize_entity_key(key):
    res = {
        'app': key.app(),
        'pairs': key.pairs(),
        'urlsafe': key.urlsafe(),
    }

    if key.namespace():
        res['namespace'] = key.namespace()

    return res
