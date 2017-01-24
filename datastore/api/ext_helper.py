from flask import request

from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata as ndb_metadata

from datastore.ext.model import ExtKey
from ..objects.metadata import Kind, Property


class ExtHelper:
    @classmethod
    def partition_data(cls, **view_args):
        return {
            'app': view_args['app'],
            'namespace': view_args.get('namespace', None),
        }

    @classmethod
    @ndb.tasklet
    def get_kind(cls, kind, **kwargs):
        if isinstance(kind, basestring):
            paritition_data = ExtHelper.partition_data(**kwargs)
            kind_key = ExtKey(ndb_metadata.Kind, kind, **paritition_data)
        elif isinstance(kind, (ExtKey, ndb.Key)):
            kind_key = kind
        elif isinstance(kind, ndb_metadata.Kind):
            kind_key = kind.key
        else:
            raise ValueError('Invalid kind: {}'.format(kind))

        paritition_data = {'app': kind_key.app(), 'namespace': kind_key.namespace()}
        properties = yield ndb_metadata.Property.query(ancestor=kind_key, **paritition_data).fetch_async()
        raise ndb.Return(Kind(kind_key.id(), properties))

    @classmethod
    def get_kinds(cls, **partition_data):
        return ndb_metadata.Kind.query(**partition_data).map(cls.get_kind, keys_only=True)
