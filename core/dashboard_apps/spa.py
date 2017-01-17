from flask import Blueprint, send_file
import flask_restful


class SinglePageApplication(Blueprint):
    APP_API_CLASS = None
    SPA_PROVIDER = 'angular'

    def __init__(self, app):
        super(SinglePageApplication, self).__init__(self.APP_NAME, self.APP_IMPORT_NAME)

        self.template_folder = self.APP_IMPORT_NAME

        self._init_views()
        self._init_api()

        app.register_blueprint(self,
            url_prefix = '/{}'.format(self.APP_URL_NAME),
            template_folder = self.template_folder,
            static_folder = 'static/' + self.APP_IMPORT_NAME,
            static_url_path = 'static/' + self.APP_URL_NAME,
        )

    def _init_api(self):
        self.api = self.APP_API_CLASS(self)
        self.api.init_app(self)

    def _init_views(self):
        self.route('/')(self.index)
        self.route('/<path:path>')(self.index)
        self.context_processor(self._context_processor)

    def index(self, path=None):
        return send_file('static/{}_spa.html'.format(self.SPA_PROVIDER))

    def _context_processor(self):
        return {
            'current_app': self,
        }
