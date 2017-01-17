import logging

from flask import current_app


class InfrastructureClient(object):
    CONFIG_NAME = None
    DEFAULT_PORT = None

    DEFAULT_TIMEOUT = 3
    ALLOW_LOCALHOST_FALLBACK = True

    NEED_SECRET = False

    CLIENTS = {}

    @classmethod
    def get(cls, **kwargs):
        kwargs = {}

        if cls.NEED_SECRET and not kwargs.get('secret', None):
            kwargs['secret'] = current_app.config['GLOBAL_SECRET']

        if cls.CONFIG_NAME:
            if not kwargs.get('host', None):
                kwargs['host'] = current_app.config.get('{}_IP'.format(cls.CONFIG_NAME), None)
                if not kwargs['host']:
                    kwargs['host'] = current_app.config.get('{}_HOST'.format(cls.CONFIG_NAME), None)
                if not kwargs['host']:
                    kwargs['host'] = None

            if not not kwargs.get('port', None):
                kwargs['port'] = current_app.config.get('{}_PORT'.format(cls.CONFIG_NAME), None)
                if not kwargs['port']:
                    kwargs['port'] = None

        if not kwargs.get('port', None):
            kwargs['port'] = cls.DEFAULT_PORT

        if not kwargs.get('host', None):
            error_text = 'Cannot determine host to estabilish connection with for {}'.format(cls)
            if cls.ALLOW_LOCALHOST_FALLBACK:
                kwargs['host'] = '127.0.0.1'
                if cls._get_connection_dst_id(kwargs) not in cls.CLIENTS:
                    logging.warning(error_text + ', trying to use localhost loopback address (127.0.0.1)')
            else:
                raise RuntimeError(error_text)

        #if getattr(cls, 'USE_HTTPS', False):
        #    if not kwargs.get('server_cert', None):
        #        kwargs['server_cert'] = current_app.config.get('CA_CERT_FILENAME', None)
        #    print(kwargs['server_cert'])

        client_dst = cls._get_connection_dst_id(kwargs)
        client = cls.CLIENTS.get(client_dst, None)
        if client is None:
            client = cls.CLIENTS[client_dst] = cls(**kwargs)
        assert client

        return client

    @classmethod
    def _get_connection_dst_id(cls, kwargs):
        assert kwargs.get('host', None)
        assert kwargs.get('port', None)
        return (kwargs['host'], kwargs['port'])
