from google.appengine.ext import ndb


# from google.appengine.datastore.entity_pb.Property
class PbMeaning:
    NO_MEANING = 0
    ATOM_CATEGORY = 1
    ATOM_LINK = 2
    ATOM_TITLE = 3
    ATOM_CONTENT = 4
    ATOM_SUMMARY = 5
    ATOM_AUTHOR = 6
    GD_WHEN = 7
    GD_EMAIL = 8
    GEORSS_POINT = 9
    GD_IM = 10
    GD_PHONENUMBER = 11
    GD_POSTALADDRESS = 12
    GD_RATING = 13
    BLOB = 14
    TEXT = 15
    BYTESTRING = 16
    BLOBKEY = 17
    INDEX_VALUE = 18
    ENTITY_PROTO = 19
    USER = 20 # not in google.appengine.datastore.entity_pb.Property, but seen in real data

    NAMES = {
        0: 'no_meaning',
        1: 'atom_category',
        2: 'atom_link',
        3: 'atom_title',
        4: 'atom_content',
        5: 'atom_summary',
        6: 'atom_author',
        7: 'datetime',
        8: 'email',
        9: 'geo_point',
        10: 'im_handle',
        11: 'phone_number',
        12: 'postal_address',
        13: 'rating',
        14: 'blob',
        15: 'text',
        16: 'bytestring',
        17: 'blobstorage_key',
        18: 'value_from_index',
        19: 'entity_proto',
        20: 'user',
    }


class PropertyDataTypes:
    NULL = 'null'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    STRING = 'string'
    DOUBLE = 'double'
    POINT = 'point'
    USER = 'user'
    KEY = 'key'


class PropertyDataInfo(object):
    def __init__(self, pb):
        self.pb = pb

    @classmethod
    def from_pb(cls, pb):
        return cls(pb)

    @property
    def name(self):
        return self.pb.name()

    @property
    def meaning_id(self):
        if self.pb.has_meaning():
            return self.pb.meaning()

    @property
    def meaning(self):
        meaning_id = self.meaning_id
        if meaning_id is not None:
            return PbMeaning.NAMES.get(meaning_id, None) or meaning_id

    @property
    def meaning_uri(self):
        return self.pb.meaning_uri()

    @property
    def is_compressed(self):
        return self.meaning_uri == ndb.model._MEANING_URI_COMPRESSED

    @property
    def data_type(self):
        pb_value = self.pb.value()

        if pb_value.has_int64value():
            return PropertyDataTypes.INTEGER
        elif pb_value.has_booleanvalue():
            return PropertyDataTypes.BOOLEAN
        elif pb_value.has_stringvalue():
            return PropertyDataTypes.STRING
        elif pb_value.has_doublevalue():
            return PropertyDataTypes.DOUBLE
        elif pb_value.has_pointvalue():
            return PropertyDataTypes.POINT
        elif pb_value.has_uservalue():
            return PropertyDataTypes.USER
        elif pb_value.has_referencevalue():
            return PropertyDataTypes.KEY
        else: # "A missing value implies null" (from ndb.model.GenericProperty._db_get_value)
            return PropertyDataTypes.NULL


class ExtKey(ndb.Key):
    pass


class ExtModel(ndb.Model):
    def __init__(self, *args, **kwargs):
        self._property_data_info = {}
        super(ExtModel, self).__init__(*args, **kwargs)

    def _get_property_for(self, p, indexed=True, depth=0):
        prop = super(ExtModel, self)._get_property_for(p, indexed=indexed, depth=depth)
        prop_data_info = PropertyDataInfo.from_pb(p)
        self._property_data_info[prop._name] = prop_data_info
        prop._data_info = prop_data_info
        return prop

    #@classmethod
    #def _lookup_model(cls, kind, default_model=None, app=None):
    #    super(Model, cls)._lookup_model((app, kind))

    #@classmethod
    #def _update_kind_map(cls, kind):
    #    pass

    #@classmethod
    #def _reset_kind_map(cls):
    #    """Clear the kind map.  Useful for testing."""
    #    # Preserve "system" kinds, like __namespace__
    #    keep = {}
    #    for (app, name), value in cls._kind_map.iteritems():
    #        if name.startswith('__') and name.endswith('__'):
    #            keep[name] = value
    #        cls._kind_map.clear()
    #        cls._kind_map.update(keep)


# prevent ModelKey._validate_key function from raising an error
# "Expected Key kind to be GenericModel; received %s"
class GenericModelKey(ndb.ModelKey):
    def _validate_key(self, value, entity=None):
        try:
            return ndb.model._validate_key(value, entity=entity)
        except ndb.KindError:
            return value

    def _validate(self, value):
        return self._validate_key(value)

    def _set_value(self, entity, value):
        """Setter for key attribute."""
        if value is not None:
            value = self._validate_key(value, entity=entity)
            value = entity._validate_key(value)
        entity._entity_key = value


class GenericModel(ndb.Expando, ExtModel):
    _key = GenericModelKey()
    key = _key

    def _fake_property(self, p, next, indexed=True):
        """Internal helper to create a fake Property."""
        self._clone_properties()
        if p.name() != next and not p.name().endswith('.' + next):
            prop = ndb.StructuredProperty(GenericModel, next)
            prop._store_value(self, ndb.model._BaseValue(GenericModel()))
        else:
            compressed = p.meaning_uri() == ndb.model._MEANING_URI_COMPRESSED
            prop = ndb.GenericProperty(next,
                                       repeated=p.multiple(),
                                       indexed=indexed,
                                       compressed=compressed)
        prop._code_name = next
        self._properties[prop._name] = prop
        return prop

## monkey-patch Model and Key classes from ndb
#ndb.model.Model = Model
#ndb.key.Key = Key
