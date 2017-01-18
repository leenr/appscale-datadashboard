import dashboard from 'core/angular.js';

import AppDatastoreFactory from './app_datastore.js';
import DatastoreEntitiesComponent from './entities.js';
import TablePropertyValueComponent from './table_property_value.js';
import EntitiesFilterDialogComponent from './entities_filter_dialog.js';

let app = dashboard.create_angular_app({
    name: 'datastore',

    dependencies: [
        'app apps',
        'angular-cache',
        'ui.bootstrap from angular-bootstrap',
        'ngTable from ng-table',
        'angularMoment from angular-moment',
        'angular.filter from angular-filter',
    ],
    routes: [
        {
            name: 'datastore',
            url: '/datastore/',

            templateUrl: 'static/datastore/index.html',
            controller: ($scope, $state, $window, app_datastore) => {
                $scope.$state = $state;
                $scope.app_datastore = app_datastore;

                let jq_window = $($window);
                function calculate_height() {
                    $scope.window_height = jq_window.height();
                    $scope.view_height = jq_window.height() - 50 - 15 * 2;
                    try {
                        $scope.$digest();
                    } catch(e) { }
                }
                jq_window.resize(calculate_height);
                calculate_height();
            },

            data: {
                container_fluid: true,
            },

            resolve: {
                app_datastore: (AppDatastore, appsService) => {
                    let use_app = appsService.selected;
                    return use_app ? new AppDatastore(use_app.id) : null;
                },
            },
        },

        {
            name: 'datastore.entities',
            abstract: true,

            css: '/static/datastore/entities.css',
            css_pause: true, // defer transition while css is loading (needed because of row calculating)

            params: {
                namespace: {type: 'string', value: ''},
                orders: {dynamic: true, array: true, type: 'string', value: []},
                offset: {dynamic: true, type: 'int', value: 0},
                filters: {dynamic: true, array: true, type: 'json', value: []},
            },

            resolve: {
                request_arguments: ($stateParams) => {
                    return [$stateParams.namespace, $stateParams.kind];
                },
            },
            views: {
                'entities@datastore': {
                    template: '<datastore-entities app-datastore="$resolve.app_datastore" request-arguments="$resolve.request_arguments"></datastore-entities>'
                },
            },
        },

        {
            name: 'datastore.entities.kind',
            url: 'kinds/{kind}',

            params: {
                kind: {type: 'string'},
            },
        },

        {
            name: 'datastore.entity',
            url: 'kinds/{kind}/entity/{key_urlsafe}',

            params: {
                kind: {type: 'string'},
                key_urlsafe: {type: 'string'},
            },

            onEnter: function($state, $uibModal) {
                $state.data.modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'entity.html',
                    controller: 'EntityCtrl',
                    controllerAs: '$ctrl',
                    size: 'md',
                    resolve: {
                        items: function () {
                            return;
                        }
                    }
                });
                $state.data.modalInstance.result['finally'](function() {
                    $state.data.modalInstance = null;
                    if($state.$current.name === stateName) {
                        $state.go('^');
                    }
                });
            },

            onExit: function($state) {
                if($state.data.modalInstance) {
                    $state.data.modalInstance.close();
                }
            },
        },
    ],

    api_config: {
        response_interceptor: (data, operation, what, url, response, deferred) => {
            let res = data;

            if(operation == 'getList' && angular.isObject(data) && angular.isDefined(data.next_cursor)) {
                res = data[what];
                res.next_cursor = data.next_cursor;
                res.count = data.count;
            }

            return res;
        },
    },
});

app.config(($uibTooltipProvider) => {
    $uibTooltipProvider.options({'placement': 'bottom-left'});
});

app.factory('AppDatastore', AppDatastoreFactory);

app.component('datastoreEntities', DatastoreEntitiesComponent);
app.component('tablePropertyValue', TablePropertyValueComponent);
app.component('entitiesFilterDialog', EntitiesFilterDialogComponent);

export default app;
