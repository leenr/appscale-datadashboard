from werkzeug.local import LocalProxy

from core.dashboard_apps.spa import SinglePageApplication

from .api import UsersApi
from .objects import AppScaleUser


class UsersApp(SinglePageApplication):
    APP_NAME = 'users'
    APP_URL_NAME = 'users'
    APP_IMPORT_NAME = __name__

    APP_API_CLASS = UsersApi

current_user = LocalProxy(lambda: AppScaleUser.get_current())
