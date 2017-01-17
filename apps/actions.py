from core.infrastructure.uaserver import UAServerClient

from users import current_user

from .objects import AppScaleApp


def get_available_apps():
    uaserver = UAServerClient.get()
    app_list = uaserver.get_all_apps()
    return filter(current_user.is_app_available, [AppScaleApp(id=app_id, **data) for app_id, data in app_list.items()])

def get_app(app_id):
    uaserver = UAServerClient.get()
    return AppScaleApp(id=app_id, **uaserver.get_app_data(app_id))
