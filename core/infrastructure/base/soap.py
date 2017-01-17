from __future__ import absolute_import

from functools import partial
import json
from time import sleep

import pysimplesoap.client
import pysimplesoap.transport

from ..clients import InfrastructureClient


class SoapClient(InfrastructureClient):
    USE_HTTPS = False

    AUTO_METHODS = True

    MAX_RETRIES = 10
    RETRY_SLEEP = 0.1

    def __init__(self, host, port=None, timeout=None, secret=None, ns=''): # , server_cert=None
        if port is None:
            port = self.DEFAULT_PORT
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        assert host is not None
        assert port is not None
        assert secret or not self.NEED_SECRET

        assert isinstance(host, str)
        assert isinstance(port, (int, long))
        assert isinstance(timeout, (int, long, type(None)))

        self._soap = pysimplesoap.client.SoapClient(
            'http{s}://{host}:{port}'.format(s=('s' if self.USE_HTTPS else ''), host=host, port=port),
            cacert = None,#server_cert if self.USE_HTTPS else None,
            timeout = timeout or self.DEFAULT_TIMEOUT,
            namespace = ns,
        )
        self._secret = secret

    def __getattr__(self, attr_name):
        if self.AUTO_METHODS and not attr_name.startswith('_'):
            return self._soap_method(attr_name)
        else:
            return super(SoapClient, self).__getattribute__(attr_name)

    def _soap_method(self, method_name):
        soap_method_call = partial(self._soap_call, method_name)
        #soap_method_call.__repr__ = soap_method_call.__str__ = lambda call: '<{!r} SOAP method {!r}>'.format(self, method_name)
        return soap_method_call

    def _soap_call(self, method_name, *args, **kwargs):
        #assert len(args) == 0 or len(kwargs) == 0

        args = list(args)
        args = [('v{}'.format(i), self._parse_arg_value(value)) for i, value in enumerate(args, 1)]

        for arg_name, arg_value in kwargs.items():
            kwargs[arg_name] = self._parse_arg_value(arg_name)

        if self.NEED_SECRET:
            args.append(('secret', self._secret))

        return self._try(lambda: self._soap.call(method_name, *args))

    def _try(self, try_func):
        for i in range(self.MAX_RETRIES):
            try:
                return try_func()
            except IOError as e:
                if i == self.MAX_RETRIES:
                    pass
                sleep(self.RETRY_SLEEP)
        else:
            raise e

    def _parse_arg_value(self, value):
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        else:
            return value
