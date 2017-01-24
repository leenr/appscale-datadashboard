from .entity import class_serializers as entity_class_serializers
from .metadata import class_serializers as metadata_class_serializers


class_serializers = {}
class_serializers.update(metadata_class_serializers)
class_serializers.update(entity_class_serializers)


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
