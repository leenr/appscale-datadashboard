from core.dashboard_apps.spa import SinglePageApplication

from .api import AppsApi


class AppsApp(SinglePageApplication):
    APP_NAME = 'apps'
    APP_URL_NAME = 'apps'
    APP_IMPORT_NAME = __name__

    APP_API_CLASS = AppsApi
