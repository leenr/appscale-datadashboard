import $ from 'jquery';
import angular from 'angular';

import create_angular_app from './angular_apps.js';

import HeaderComponent from './header.js';

let dashboard_app = null;

let core_app_name = 'DashboardCoreApp',
    core_dependencies = [
        // list of these core app dependencies (excluding dashboard apps)
        'oc.lazyLoad from oclazyload/dist/modules/ocLazyLoad.core.js', // lazy loader of angular modules
        'import oclazyload/dist/modules/ocLazyLoad.loaders.core.js after', // only after module above import loaders

        'ct.ui.router.extras.core from ct.ui.router.extras/release/modular/ct-ui-router-extras.core', // dependency of ct.ui.router.extras.future
        'ct.ui.router.extras.future from ct.ui.router.extras/release/modular/ct-ui-router-extras.future', // for lazy loading routes

        'ui.router from angular-ui-router',

        'restangular', // for api

        'ngTable from ng-table', // lazy load of ngTable is not load it properly, as ngTable defines run() blocks on 'ng' module, which is not executing, since at the time of lazy load, run-blocks of 'ng' module was executed already
    ], bootstrap_apps = [
        // list of applications, which we need to load with dashboard core bootstraping
        'apps', 'users',
    ],
    all_apps = {
        // list of applications 
        'apps': {
            'url_name': 'apps',
        },
        'datastore': {
            'url_name': 'datastore',
        },
        'users': {
            'url_name': 'users',
        },
    };

var ocLazyLoad = null;

let core_api = {
    get dashboard_app() { return dashboard_app; },

    bootstrap: (into_elm) => {
        dashboard_app = angular.module(core_app_name, []);
        dashboard_app.component('dashboardHeader', HeaderComponent);

        dashboard_app.config(function($futureStateProvider) {
            $futureStateProvider.stateFactory('app', (futureState) => {
                return core_api.load_app(futureState.src).then(() => {}, (error) => {
                    console.error(error);
                    throw Error('Cannot load app ' + futureState.src);
                });
            });
            for(let app_name in all_apps) {
                let app_url_name = all_apps[app_name].url_name;
                $futureStateProvider.futureState({
                    stateName: app_name,
                    bname: app_name,
                    urlPrefix: '/' + app_url_name,
                    type: 'app',
                    src: app_name,
                });
            }
        });

        dashboard_app.config(($locationProvider) => { $locationProvider.html5Mode({enabled: true, requireBase: false}); });
        dashboard_app.run(($transitions, $q) => {
            $transitions.onEnter({}, (transition, state) => {
                let css_loaded_defer = $q.defer();

                let css_s = [];
                if(state.css) {
                    css_s.push(...state.css);
                }
                let css_pause = state.css_pause;

                for(let state_cur = state.parent; state_cur != null; state_cur = state_cur.parent) {
                    if(state_cur.css) {
                        css_s.push(...state_cur.css);
                        css_pause |= state_cur.css_pause;
                    }
                }

                for(let css_src of css_s) {
                    System.import(css_src + '!').then(() => {
                        css_loaded_defer.resolve();
                    }, (error) => {
                        console.error(error);
                        css_loaded_defer.reject(error);
                        throw Error('Cannot load css with url ' + css_src + ' for state ' + state.name);
                    });
                }
                return state.css_pause && css_s ? css_loaded_defer.promise : true;
            });
        });

        dashboard_app.run(($ocLazyLoad) => { ocLazyLoad = $ocLazyLoad; });

        if(window['ui-router-visualizer']) {
            dashboard_app.run(function($uiRouter) {
                window['ui-router-visualizer'].visualizer($uiRouter);
            });
        }

        let promises = [core_api.resolve_dependencies(dashboard_app, core_dependencies)];
        promises.push(core_api.load_app(...bootstrap_apps));

        Promise.all(promises).then(() => {
            angular.bootstrap(into_elm, [dashboard_app.name]);
        }, (error) => {
            console.error(error);
            throw Error('Cannot satisfy core dashboard app dependencies');
        });
    },

    load_app: (...app_import_names) => core_api.load_app_into(dashboard_app, ...app_import_names),
    load_apps: (app_import_names) => core_api.load_apps_into(dashboard_app, app_import_names),

    load_apps_into: (into, app_import_names) => {
        return core_api.load_modules(
            app_import_names.map((app_import_name) => app_import_name + '/index.js'),
        ).then((app_modules) => {
            let apps = app_modules.map((app_module) => app_module.default);
            let boot_promises = [];
            for(let app of apps) {
                boot_promises.push(app._boot_promise);
                into.requires.push(app.name);
            }
            return Promise.all(boot_promises).then(() => apps);
        }, (error) => {
            console.error(error);
            throw Error('Cannot load ' + app_import_names + ' into ' + into.name + '.');
        });
    },
    load_app_into: (into, ...app_import_names) => core_api.load_apps_into(into, app_import_names),

    load_module: (...modules) => core_api.load_modules(modules),
    load_modules: (modules) => Promise.all(modules.map((module_name) => System.import(module_name))),

    resolve_dependencies: (angular_app, dependencies) => {
        let import_name, angular_name; 

        let load_modules_map = {};
        let res_promises = [];

        for(let dependency of dependencies) {
            let promise_func;
            let import_name, angular_name;

            let delay_load = false;
            if(dependency.endsWith(' after')) {
                delay_load = true;
                dependency = dependency.slice(0, -6);
            }

            if(dependency.startsWith('app ')) {
                import_name = dependency.slice(4);
                promise_func = () => core_api.load_app_into(angular_app, import_name);
            } else if(dependency.startsWith('import ')) {
                import_name = dependency.slice(7);
                promise_func = () => core_api.load_module(import_name);
            } else {
                if(dependency.indexOf(' from ') >= 0) {
                    [angular_name, import_name] = dependency.split(' from ');
                } else {
                    angular_name = import_name = dependency;
                }
                angular_app.requires.push(angular_name);
                promise_func = () => core_api.load_module(import_name);
            }

            let dependency_error_func = (error) => {
                console.error(error);
                throw Error('Cannot load dependency for angular module ' + angular_app.name + ': ' + dependency);
            };

            let promise = !delay_load ? promise_func().catch(dependency_error_func) : res_promises.pop().then(promise_func, dependency_error_func);

            res_promises.push(promise);
        }

        return Promise.all(res_promises);
    },

    boot_app: (app) => {
        if(ocLazyLoad) {
            return ocLazyLoad.inject(app, {}, true);
        }
    },

    create_angular_app: create_angular_app,
};

export default core_api;
