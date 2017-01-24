from collections import OrderedDict

from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata as ndb_metadata


class Kind(ndb_metadata.Kind):
    def __init__(self, name, properties=None):
        self.kind = name
        self.properties = properties

    def _to_api(self):
        return {
            'name': self.kind,
            'properties': self.properties,
        }


class Property(ndb.model.Property):
    def _to_api(self):
        return {
            'name': self._name,
            'verbose_name': self._verbose_name,
            'indexed': self._indexed,
            'repeated': self._repeated,
            'required': self._required,
            'default': self._default,
            'choices': self._choices,
            'validator': self._validator,
        }

    @staticmethod
    def get_type_name(prop):
        types_dict = OrderedDict([
            (ndb.IntegerProperty, 'integer'),
            (ndb.FloatProperty, 'float'),
            (ndb.BooleanProperty, 'boolean'),

            (ndb.StringProperty, 'string'),
            (ndb.TextProperty, 'text'),
            (ndb.BlobProperty, 'blob'),

            (ndb.DateTimeProperty, 'datetime'),
            (ndb.DateProperty, 'date'),
            (ndb.TimeProperty, 'time'),

            (ndb.GeoPtProperty, 'geopt'),

            (ndb.KeyProperty, 'key'),
            (ndb.BlobKeyProperty, 'blobkey'),

            (ndb.UserProperty, 'user'),
            (ndb.StructuredProperty, 'structured'),

            (ndb.LocalStructuredProperty, 'serialized'),
            (ndb.JsonProperty, 'serialized'),
            (ndb.PickleProperty, 'serialized'),

            (ndb.ComputedProperty, 'unknown'),
            (ndb.GenericProperty, 'unknown'),
        ])


class MetadataProperty(ndb_metadata.Property):
    def _to_api(self):
        return {
            'name': self.property_name,
            'property_representation': self.property_representation,
        }


class_serializers = {
    ndb_metadata.Namespace: lambda namespace: namespace.namespace_name,
    ndb_metadata.Kind: Kind._to_api,
    ndb_metadata.Property: MetadataProperty._to_api,
    ndb.model.Property: Property._to_api,
}
