import create_api_factory from './api.js';

import core_api from './angular.js';

export default function create_angular_app(config) {
    if(!config.import_name) config.import_name = config.name;
    if(!config.url_name) config.url_name = config.name;

    if(!config.base_url) config.base_url = '/' + config.url_name;
    if(config.base_url.endsWith('/')) config.base_url = config.base_url.slice(0, -1);

    if(!config.api_base_url) config.api_base_url = config.base_url + '/_api';

    if(angular.isUndefined(config.register_api)) config.register_api = true;
    if(!config.api_config) config.api_config = {};

    if(!config.dependencies) config.dependencies = [];

    config.static_files_dir = config.import_name;

    let app = angular.module(config.import_name + 'App', []);

    if(config.register_api) {
        app.factory(config.import_name + '_api', create_api_factory(app, angular.extend({
            base_url: config.api_base_url,
        }, config.api_config)));
    }

    if(config.routes) {
        app.config(function($stateProvider) {
            for(let route of config.routes) {
                if(route.name == '.' || !route) {
                    route.name = config.import_name;
                } else if(route.name.startsWith('.')) {
                    route.name = config.import_name + route.name;
                } else if(!route.name.startsWith(config.import_name + '.') && route.name != config.import_name) {
                    console.warn('Following route in app with import name ' + config.import_name + ' use non-relative name with parent != app import name:', route);
                }

                if(route.relativeUrl) {
                    if(!route.relativeUrl.startsWith('/')) route.relativeUrl = '/' + route.relativeUrl;
                    route.url = config.base_url + route.relativeUrl;
                    delete route.relativeUrl;
                }

                if(route.templateFilename) {
                    route.templateUrl = config.static_files_dir + '/' + route.templateFilename;
                    delete route.templateFilename;
                }

                if(!route.resolve) {
                    route.resolve = {};
                }

                if(route.css) {
                    if(!(route.css instanceof Array)) {
                        route.css = [route.css];
                    }
                }

                $stateProvider.state(route);
            }
        });
        app.run(function($urlRouter) {
            $urlRouter.sync();
        });
    }

    app._boot_promise = core_api.resolve_dependencies(app, config.dependencies).then(() => {
        // ok
        core_api.boot_app(app);
    }, (error) => {
        // error
        throw Error('Cannot satisfy all dependencies for app ' + config.name + ', so app will not boot.');
    });

    return app;
};
