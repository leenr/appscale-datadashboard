from google.appengine.api import datastore_errors
from google.appengine.ext import ndb
from google.appengine.ext.ndb.key import _ConstructReference


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
    USER = 20  # not in google.appengine.datastore.entity_pb.Property, but seen in real data

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
        else:  # "A missing value implies null" (from ndb.model.GenericProperty._db_get_value)
            return PropertyDataTypes.NULL


class ExtKey(ndb.Key):
    # we use ndb.Key private properties and use proxies to make it
    __slots__ = ['_Key__reference', '_Key__pairs', '_Key__app', '_Key__namespace', '__adapter', '__context']

    def __new__(cls, *_args, **kwargs):
        adapter = None
        context = None
        if '_adapter' in kwargs:
            adapter = kwargs.pop('_adapter')
            context = adapter.context
        elif '_context' in kwargs:
            context = kwargs.pop('_context')

        # check arguments
        if _args:
            if len(_args) == 1 and isinstance(_args[0], dict):
                if kwargs:
                    raise TypeError('ExtKey() takes no keyword arguments when a dict is the '
                                    'the first and only non-keyword argument (for unpickling).')
                kwargs = _args[0]
            else:
                if 'flat' in kwargs:
                    raise TypeError('ExtKey() with positional arguments cannot accept flat as a keyword argument.')
                kwargs['flat'] = _args

        # ndb.Key is not designed to be a parent class, but we can do some things to make it work
        if 'reference' in kwargs or 'serialized' in kwargs or 'urlsafe' in kwargs:
            # if reference is set, we cannot use super().__new__ because _ConstructReference check first argument
            # to be ndb.Key class
            self = super(ndb.Key, cls).__new__(cls)
            self.__reference = _ConstructReference(ndb.Key, **kwargs)
            self.__pairs = None  # can be extracted from reference
            self.__app = None  # can be extracted from reference
            self.__namespace = None  # can be extracted from reference
        elif 'pairs' in kwargs or 'flat' in kwargs:
            # otherwise, _ConstructReference is not called and we can subclass as usual
            self = super(ExtKey, cls).__new__(cls, pairs=kwargs.get('pairs', None), flat=kwargs.get('flat', None))
        else:
            raise TypeError('Key() cannot create a Key instance without arguments.')

        self.__context = context
        self.__adapter = adapter

        return self

    # Alias private properties of ndb.Key

    @property
    def __reference(self): return self._Key__reference

    @__reference.setter
    def __reference(self, value): self._Key__reference = value

    @property
    def __pairs(self): return self._Key__pairs

    @__pairs.setter
    def __pairs(self, value): self._Key__pairs = value

    @property
    def __app(self): return self._Key__app

    @__app.setter
    def __app(self, value): self._Key__app = value

    @property
    def __namespace(self): return self._Key__namespace

    @__namespace.setter
    def __namespace(self, value): self._Key__namespace = value

    def get_async(self, **ctx_options):
        """Return a Future whose result is the entity for this Key.

        If no such entity exists, a Future is still returned, and the
        Future's eventual return result be None.
        """
        model = None
        if self.__adapter:
            model = self.__adapter._model_for_key(self)
            model._pre_get_hook(self)

        fut = self.__context.get(self, **ctx_options)

        if model:
            post_hook = model._post_get_hook
            fut.add_immediate_callback(post_hook, self, fut)

        return fut

    def delete_async(self, **ctx_options):
        """Schedule deletion of the entity for this Key.

        This returns a Future, whose result becomes available once the
        deletion is complete.  If no such entity exists, a Future is still
        returned.  In all cases the Future's result is None (i.e. there is
        no way to tell whether the entity existed or not).
        """

        model = None
        if self.__adapter:
            model = self.__adapter._model_for_key(self)
            model._pre_delete_hook(self)

        fut = self.__adapter.context.delete(self, **ctx_options)

        if model:
            post_hook = model._post_delete_hook
            fut.add_immediate_callback(post_hook, self, fut)

        return fut


class ExtModelKey(ndb.ModelKey):
    _KEY_CLASS = ExtKey

    # ndb.ModelKey's implementation of this method calls local _validate_key function in ndb.model module
    # It check for Key class to be IS ndb.Key, but we need to check for ExtKey, so we need to override entire method
    def _set_value(self, entity, value):
        """Setter for key attribute."""
        if value is not None:
            value = self._validate_key(value, entity=entity)
            value = entity._validate_key(value)
        entity._entity_key = value

    def _validate_key(self, value, entity=None):
        # Don't be like NDB developers, use ._KEY_CLASS constant, so subclasses can override key class :)
        if not isinstance(value, self._KEY_CLASS):
            raise datastore_errors.BadValueError('Expected %r instance, got %r' % (self._KEY_CLASS, value))
        return value

    # Same note as for ._set_value
    def _validate(self, value):
        return self._validate_key(value)


class ExtModel(ndb.Model):
    _key = ExtModelKey()
    key = _key

    def __init__(self, *args, **kwargs):
        self._property_data_info = {}

        self._adapter = None
        self._context = None
        if '_adapter' in kwargs:
            self._adapter = kwargs.pop('_adapter')
            self._context = self._adapter.context
        elif '_context' in kwargs:
            self._context = kwargs.pop('_context')
        elif '_kind' in kwargs:
            kind = kwargs.pop('_kind')
            self._get_kind = lambda: kind

        super(ExtModel, self).__init__(*args, **kwargs)

    @classmethod
    def _get_kind(cls):
        return ''

    def _get_property_for(self, p, indexed=True, depth=0):
        prop = super(ExtModel, self)._get_property_for(p, indexed=indexed, depth=depth)
        prop_data_info = PropertyDataInfo.from_pb(p)
        self._property_data_info[prop._name] = prop_data_info
        prop._data_info = prop_data_info
        return prop

    @classmethod
    def _lookup_model_for_key(cls, key):
        return None  # TODO: just a stub at this time

    def _put_async(self, **ctx_options):
        """Write this entity to the datastore.

        This is the asynchronous version of Model._put().
        """
        if self._projection:
            raise datastore_errors.BadRequestError('Cannot put a partial entity')
        self._prepare_for_put()
        if self._key is None:
            kind = self._get_kind()
            if kind is None:
                raise ValueError('Cannot determine kind name for this entity to construct key')
            self._key = self._key._KEY_CLASS(kind, None)
        self._pre_put_hook()
        fut = self._context.put(self, **ctx_options)
        post_hook = self._post_put_hook
        fut.add_immediate_callback(post_hook, fut)
        return fut

    put_async = _put_async


class GenericExtModel(ndb.Expando, ExtModel):
    def _fake_property(self, p, next, indexed=True):
        self._clone_properties()
        compressed = p.meaning_uri() == ndb.model._MEANING_URI_COMPRESSED
        prop = ndb.GenericProperty(next, repeated=p.multiple(), indexed=indexed, compressed=compressed)
        prop._code_name = next
        self._properties[prop._name] = prop
        return prop


class GenericPropertyWithMeaning(ndb.GenericProperty):
    def __init__(self, name=None, meaning=None, **kwargs):
        super(GenericPropertyWithMeaning, self).__init__(name, **kwargs)
        self._meaning = meaning

    def _db_set_value(self, v, p, value):
        super(GenericPropertyWithMeaning, self)._db_set_value(v, p, value)
        if self._meaning is not None:
            v.set_meaning(self._meaning)
