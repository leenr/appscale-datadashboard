from google.appengine.api import users as gusers

from core.infrastructure.uaserver import UAServerClient


class AppScaleUserType:
    XMPP = 'xmpp'
    APP = 'app'

    ALL = [XMPP, APP]

class AppScaleUserCapability:
    UPLOAD_APP = 'upload_app'

    ALL = [UPLOAD_APP]

class AppScaleUser(object):
    def __init__(self, guser, **user_data):
        self.guser = guser

        self.user_type = user_data.pop('type', AppScaleUserType.XMPP)
        self.enabled = user_data.pop('enabled', True)

        self.email = user_data.pop('user_email', None)
        self.hashed_password = user_data.pop('password', None)

        self.created_on = user_data.pop('creation_date', None)
        self.updated_on = user_data.pop('change_date', None)

        self.capabilities = user_data.pop('capabilities', [])
        self.applications = user_data.pop('applications', [])

        self.is_cloud_admin = user_data.pop('is_cloud_admin', False)

        self.session_cookie = user_data.pop('session_cookie', None)
        self.last_login_on = user_data.pop('login_date', None)
        self.cookie_ip = user_data.pop('cookie_ip', None)
        self.cookie_exp = user_data.pop('cookie_exp', None)

        self.extra = user_data

    @classmethod
    def get_current(cls):
        guser = gusers.get_current_user()
        if guser is None:
            return None

        uaserver = UAServerClient.get()
        user_data = uaserver.get_user_data(guser.email())
        return cls(guser, **user_data)

    @property
    def id(self):
        return self.email

    @property
    def name(self):
        return self.guser.nickname()

    def is_app_available(self, app):
        return self.email == app.owner_email or app.id in self.applications
