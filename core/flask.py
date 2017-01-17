from __future__ import absolute_import

from flask import Flask


class FlaskApp(Flask):
    def __init__(self):
        super(FlaskApp, self).__init__('main',
            template_folder = 'static',
        )

    def create_jinja_environment(self):
        env = super(FlaskApp, self).create_jinja_environment()
        env.variable_start_string, env.variable_end_string = '{=', '=}'
        return env
