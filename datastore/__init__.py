from core.dashboard_apps.spa import SinglePageApplication

from .api import DatastoreApi


class DatastoreApp(SinglePageApplication):
    APP_NAME = 'datastore'
    APP_URL_NAME = APP_NAME
    APP_IMPORT_NAME = __name__

    APP_API_CLASS = DatastoreApi
