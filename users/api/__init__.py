from flask_restful import Resource, Api

from core.dashboard_apps.api import ApplicationApi

from ..objects import AppScaleUser


class UsersApi(ApplicationApi):
    def get_resources(self):
        from . import users
        return users.ALL_RESOURCES

    def serialize_obj(self, obj):
        res = super(UsersApi, self).serialize_obj(obj)
        if res is not NotImplemented:
            return res

        if isinstance(obj, AppScaleUser):
            user = obj
            return {
                'user_type': user.user_type,
                'enabled': user.enabled,
                'email': user.email,
                'created_on': user.created_on,
                'updated_on': user.updated_on,
                'capabilities': user.capabilities,
                'applications': user.applications,
                'is_cloud_admin': user.is_cloud_admin,
                'last_login_on': user.last_login_on,

                'name': user.name,
                'id': user.id,
            }

        return NotImplemented
