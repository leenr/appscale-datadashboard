from collections import OrderedDict

from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata as ndb_metadata


class Kind(ndb_metadata.Kind):
    def __init__(self, name, properties=None):
        self.kind = name
        self.properties = properties
        self._model = None

    def __del__(self):
        del ndb.Model._kind_map[self.kind]

    @property
    def model(self):
        if self._model is None:
            self._model = self._create_model()

        return self._model

    def _create_model(self):
        base_class = ndb.Model if self.properties else ndb.Expando
        model = type(str(self.kind), (base_class,), {})

        if self.properties:
            for prop in self.properties:
                model._properties[prop.name] = prop.model_attribute

        return model

    def _to_api(self):
        return {
            'name': self.kind,
            'properties': self.properties,
        }

class Property(ndb_metadata.Property):
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


class_serializers = {
    ndb_metadata.Namespace: lambda namespace: namespace.namespace_name,
    ndb_metadata.Kind: Kind._to_api,
    ndb_metadata.Property: Property._to_api,
}
