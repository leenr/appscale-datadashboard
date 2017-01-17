from functools import partial
from datetime import datetime
import json

from .base.soap import SoapClient


class UAServerClient(SoapClient):
    DEFAULT_PORT = 4343
    NEED_SECRET = True
    USE_HTTPS = True

    LIST_SEPARATOR = ':'

    CONFIG_NAME = 'UASERVER'

    def _parse_arg_value(self, value):
        if isinstance(value, (list,)):
            return self.LIST_SEPARATOR.join(value)
        elif value is None:
            return self.LIST_SEPARATOR.join(value)

        return value

    def _unparse_value(self, value, type_name, may_be_notset=False, notset_values=None, list_sep=LIST_SEPARATOR):
        if may_be_notset:
            if notset_values is None:
                default_notset_values = ('', 'notSet')
                notset_values = {
                    'timestamp': tuple(list(default_notset_values) + ['0']),
                }.get(type_name, default_notset_values)

            if value in notset_values:
                return None

        if type_name == 'bool':
            return {'true': True, 'false': False}.get(value.lower(), None)
        elif type_name == 'str':
            return unicode(value)
        elif type_name == 'int':
            return int(float(value) if '.' in value else value)
        elif type_name == 'float':
            return float(value)
        elif type_name == 'timestamp':
            return datetime.fromtimestamp(float(value))
        elif type_name.endswith('_list'):
            child_type = type_name[:-len('_list')]
            return map(partial(self._unparse_value, type_name=child_type), value.split(list_sep))

        return value

    def _unparse_by_defs(self, data, defs):
        for prop_name, prop_def in defs.items():
            if prop_name not in data:
                continue

            if '->' in prop_name:
                prop_name, new_name = (s.strip() for s in prop_name.split('->'))
            else:
                prop_name = new_name = prop_name.strip()

            if isinstance(prop_def, basestring):
                prop_def = {'type_name': prop_def}

            new_name = str(prop_def.pop('new_name', prop_name))
            data[new_name] = self._unparse_value(data[prop_name], **prop_def)
            if new_name != prop_name:
                del data[prop_name]

        return data

    def get_user_data(self, username):
        user_data = self._soap_call('get_user_data', username)('Result')
        user_data = unicode(user_data).strip().split('\n')
        user_data = dict((line.split(':', 1) for line in user_data))

        defs = {
            'type': 'str',
            'enabled': 'bool',
            'user_email': 'str',
            'password': 'str',

            'creation_date': 'timestamp',
            'change_date': 'timestamp',

            'ck_sum': 'int',
            'visit_cnt': 'int',

            'capabilities': 'str_list',
            'is_cloud_admin': 'bool',
            'applications': 'str_list',
            'num_apps': 'int',

            'appdrop_rem_token': {'type_name': 'str', 'may_be_notset': True},
            'session_cookie': {'type_name': 'str', 'may_be_notset': True},
            'login_date': 'timestamp',
            'cookie_ip': 'str',
            'cookie_exp': {'type_name': 'timestamp', 'may_be_notset': True},
        }

        return self._unparse_by_defs(user_data, defs)

    def get_app_data(self, app_id):
        app_data = self._soap_call('get_app_data', app_id)('Result')
        app_data = json.loads(unicode(app_data))

        defs = {
            'name': 'str',
            'enabled': 'bool',
            'language': 'str',

            'owner': 'str',
            'admins_list': 'str_list',

            'creation_date': 'timestamp',
            'last_time_updated_date': 'timestamp',

            'ck_sum': 'int',

            'host': 'str',
            'port -> ports': {'type_name': 'int_list', 'list_sep': '-'},
        }

        return self._unparse_by_defs(app_data, defs)

    def get_all_apps(self):
        app_ids = self._unparse_value(unicode(self._soap_call('get_all_apps')('Result')).strip('____:'), 'str_list')
        res = {}
        for app_id in app_ids:
            res[app_id] = self.get_app_data(app_id)
        return res
