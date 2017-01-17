from datetime import datetime
import json

from flask import make_response
import flask_restful


class ApplicationApi(flask_restful.Api):
    API_URL_NAME = '_api'

    def __init__(self, bp):
        super(ApplicationApi, self).__init__(bp, '/' + self.API_URL_NAME)
        self.register_resources()
        self.representation('application/json')(self._json_representation_func)

    def register_resources(self):
        for resource in self.get_resources():
            self.add_resource(resource, *resource.urls)

    def serialize_obj(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        return NotImplemented

    def _json_representation_func(self, data, code, headers=None):
        def serialize_obj(obj):
            res = self.serialize_obj(obj)
            if res is NotImplemented:
                raise NotImplementedError('{!r} object is not serializable'.format(obj))
            else:
                return res

        resp = make_response(json.dumps(data, default=serialize_obj, sort_keys=True, ensure_ascii=False), code)
        resp.headers.extend(headers or {})
        return resp

class ApiResource(flask_restful.Resource):
    pass
