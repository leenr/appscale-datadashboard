from core.dashboard_apps.api import ApiResource

from ..objects import AppScaleUser


class CurrentUser(ApiResource):
    urls = ['/current/']

    def get(self):
        return AppScaleUser.get_current()


ALL_RESOURCES = [CurrentUser]
