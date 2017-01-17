from google.appengine.ext import ndb
from google.appengine.ext.ndb.google_imports import datastore_rpc

from .model import GenericModel, ExtModel, ExtKey


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

    def pb_to_entity(self, pb):
        ''' Converts protocol buffer data into user-class entity. '''

        key = None
        kind = None

        pb_key = pb.key()
        if pb_key.path().element_size():
            key = ExtKey(reference=pb_key)
            kind = key.kind()

        entity = ExtModel._from_pb(pb, key=key, set_key=False)
        if self.want_pbs:
            entity._orig_pb = pb

        return entity


def _make_ext_connection():
    return ndb.make_connection(default_model=GenericModel)

_ext_connection = _make_ext_connection()
ext_context = ndb.Context(_ext_connection)
