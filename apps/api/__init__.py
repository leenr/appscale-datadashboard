from __future__ import absolute_import

from flask_restful import Resource, Api

from core.dashboard_apps.api import ApplicationApi

from users import current_user

from ..objects import AppScaleApp


class AppsApi(ApplicationApi):
    def get_resources(self):
        from . import apps
        return apps.ALL_RESOURCES

    def serialize_obj(self, obj):
        res = super(AppsApi, self).serialize_obj(obj)
        if res is not NotImplemented:
            return res

        if isinstance(obj, AppScaleApp):
            app = obj
            return {
                'id': app.id,
                'name': app.name,

                'host': app.host,
                'ports': app.ports,

                'created_on': app.created_on,
                'updated_on': app.updated_on,
                'update_id': app.update_id,
            }

        return NotImplemented
