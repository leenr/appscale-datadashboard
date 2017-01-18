import { KeyValue } from './datastore_types.js';

export default {
    templateUrl: 'static/datastore/entities_filter_dialog.html',

    bindings: {
        resolve: '<',
        modal_instance: '<modalInstance'
    },

    template: '',
    controller: function($scope) {
        let $ctrl = this;
        $scope.$ctrl = $ctrl;

        $scope.kind_path = $ctrl.resolve.kind_path;
        $scope.properties = $ctrl.resolve.properties;
        $scope.app_datastore = $ctrl.resolve.app_datastore;

        $scope.key_filter = {
            id: '',
            ancestors: [[]]
        };
        $scope.property_filters = [
            {name: '', predicate: '=', value: ''}
        ];

        if(!$.isEmptyObject($ctrl.resolve.filter_params)) {
            $scope.key_filter = $ctrl.resolve.filter_params._key_filter;
            $scope.property_filters = $ctrl.resolve.filter_params._property_filters;
        }

        var kind = $scope.kind_path[1];

        function construct_key_filter_definition(filter) {
            let key_pairs = [];
            for(let ancestor_pair of filter.ancestors) {
                if(ancestor_pair[0]) key_pairs.push(ancestor_pair);
            }
            key_pairs.push([kind, filter.id]);

            let key_value = new KeyValue({
                app: undefined, // not used by backend
                namespace: undefined, // not used by backend
                pairs: key_pairs
            });
            return angular.toJson(key_value.toObject());
        }

        function construct_ancestor_filter_definition(filter) {
            let key_pairs = [];
            for(let ancestor_pair of filter.ancestors) {
                if(ancestor_pair[0]) key_pairs.push(ancestor_pair);
            }
            let key_value = new KeyValue({
                app: undefined, // not used by backend
                namespace: undefined, // not used by backend
                pairs: key_pairs
            });
            return angular.toJson(key_value.toObject());
        }

        function construct_properties_filter_definition(filters) {
            let filter_arrays = [];
            for(let filter of filters) {
                filter_arrays.push([filter.name, filter.predicate, filter.value]);
            }
            return angular.toJson(filter_arrays);
        }

        $scope.apply = function() {
            let res = {};

            Object.defineProperties(res, {
                _key_filter: {
                    value: $scope.key_filter,
                    enumerable: false,
                },
                _property_filters: {
                    value: $scope.property_filters,
                    enumerable: false,
                },
            });

            if($scope.key_filter.id) {
                res['key_json'] = construct_key_filter_definition($scope.key_filter);
            } else if($scope.key_filter.ancestors[0][0]) {
                res['ancestor_json'] = construct_ancestor_filter_definition($scope.key_filter);
            } else if($scope.property_filters) {
                res['filters_json'] = construct_properties_filter_definition($scope.property_filters);
            }

            $ctrl.modal_instance.close(res);
        }
    },
};
