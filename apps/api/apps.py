from core.dashboard_apps.api import ApiResource

from ..actions import get_app, get_available_apps


class AvailableApps(ApiResource):
    urls = ['/available']

    def get(self):
        return get_available_apps()

class AppResource(ApiResource):
    urls = ['/apps/<string:app_id>']

    def get(self, app_id):
        return get_app(app_id)


ALL_RESOURCES = [AvailableApps, AppResource]
