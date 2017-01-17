from flask_restful import Resource, Api

from core.dashboard_apps.api import ApplicationApi

from ..objects import api_serialize_obj


class DatastoreApi(ApplicationApi):
    def get_resources(self):
        from . import dbinfo, entities
        return dbinfo.ALL_RESOURCES + entities.ALL_RESOURCES

    def serialize_obj(self, obj):
        res = super(DatastoreApi, self).serialize_obj(obj)
        return api_serialize_obj(obj) if res is NotImplemented else res
