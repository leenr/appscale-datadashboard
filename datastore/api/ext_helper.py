from flask import request

from google.appengine.ext import ndb
from google.appengine.ext.ndb import metadata as ndb_metadata

from ..objects.metadata import Kind, Property


class ExtHelper:
    @classmethod
    def query_for(cls, model, **override_kwargs):
        return model.query(**cls.kwargs(**override_kwargs))

    @classmethod
    def key(cls, *pairs, **override_kwargs):
        return ndb.Key(*pairs, **cls.kwargs(**override_kwargs))

    @classmethod
    def kwargs(cls, **override_kwargs):
        kwargs = request.view_args.copy()
        kwargs.update(override_kwargs)

        kwargs = dict(((key, value) for key, value in kwargs.items() if key in ('app', 'namespace', 'ancestor', 'keys_only')))
        if 'namespace' in kwargs and not kwargs['namespace']:
            del kwargs['namespace']

        return kwargs

    @classmethod
    @ndb.tasklet
    def get_kind(cls, kind):
        if isinstance(kind, basestring):
            kind_key = cls.key(ndb_metadata.Kind, kind)
        elif isinstance(kind, ndb.Key):
            kind_key = kind
        elif isinstance(kind, ndb_metadata.Kind):
            kind_key = kind.key

        properties = yield cls.query_for(ndb_metadata.Property, ancestor=kind_key).fetch_async()
        ext_properties = map(Property, properties)
        raise ndb.Return(Kind(kind_key.id(), properties))

    @classmethod
    def get_kinds(cls):
        return cls.query_for(ndb_metadata.Kind).map(cls.get_kind, keys_only=True)
