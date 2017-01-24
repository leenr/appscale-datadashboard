from google.appengine.ext import ndb
from google.appengine.ext.ndb.google_imports import datastore_rpc

from .model import GenericExtModel, ExtModel, ExtKey


class ExtModelAdapter(ndb.ModelAdapter):
    # Do not even think about looking up kind model in ndb.Model._kind_map,
    # since queries with this adapter may envolve many different apps with
    # different schema. Another cause: security of dashboard models, which
    # is normal ndb.Model subclasses and because of it should be saved in
    # _kind_map. Queries for that uses normal ndb.model.ModelAdapter class,
    # so they will not be affected.
    # This adapter uses subclass of ndb.Model with extended functions, such
    # as saving property data info (data meaning, etc). Also, it don't do
    # some expensive data transformations, which is not needed for the
    # datastore API. See ExtModel and ExtKey for details on difference.

    ''' 
        External model adapter. Extends from ndb.ModelAdapter and uses
        subclasses of ndb.Model (.model.ExtModel) and ndb.Key (.model.ExtKey)
    '''

    def __init__(self, ext_model, default_model=None):
        self.ext_model = ext_model
        self.default_model = default_model
        self.context = None

    def _model_for_key(self, key):
        model = self.default_model

        if key is not None:
            model = self.ext_model._lookup_model_for_key(key) or model

        if model is None:
            raise RuntimeError('Cannot lookup model for {} key'.format(key))

        return model

    def pb_to_entity(self, pb):
        ''' Converts protocol buffer data into user-class entity. '''

        key = None

        pb_key = pb.key()
        if pb_key.path().element_size():
            key = ExtKey(reference=pb_key, _adapter=self)

        model = self._model_for_key(key)
        entity = model._from_pb(pb, key=key, set_key=False)

        return entity

    def _bind_context(self, context):
        self.context = context


def _make_ext_connection():
    adapter = ExtModelAdapter(ExtModel, GenericExtModel)
    return datastore_rpc.Connection(adapter=adapter, config=None)

_ext_connection = _make_ext_connection()
ext_context = ndb.Context(_ext_connection)
_ext_connection.adapter._bind_context(ext_context)
