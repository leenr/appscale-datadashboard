export default {
    templateUrl: 'static/datastore/entities.html',

    bindings: {
        app_datastore: '<appDatastore',
        request_arguments: '<requestArguments',
    },

    controller: function($element, $sce, $scope, $state, $stateParams, $q, $uibModal, $window, NgTableParams, ngTableEventsChannel) {
        function get_page_for_offset(offset, count, old_count) {
            if(angular.isUndefined(old_count) || count < old_count) {
                return Math.floor(offset / count) + 1;
            } else {
                return Math.ceil(offset / count) + 1;
            }
        }
        function get_start_offset(page, count) {
            return count * (page - 1);
        }

        function compare_objects(obj1, obj2) {
            return angular.toJson(obj1) == angular.toJson(obj2);
        }

        let app_datastore = this.app_datastore;
        let request_arguments = this.request_arguments;

        let dom_header = $element.find('.header');
        let dom_table_wrapper = $element.find('.entities-table-wrapper');
        let dom_footer = $element.find('.footer');
        function calculate_table_count(new_view_height) {
            let one_row_height = 34;

            let table_height = new_view_height - dom_table_wrapper.position().top - dom_footer.outerHeight();
            let table_header_height = one_row_height;
            let table_footer_height = 0;
            let table_body_height = table_height - table_header_height - table_footer_height;

            let new_count = Math.floor(table_body_height / one_row_height);
            new_count = Math.max(new_count, 10); // 10 is minimum

            if($scope.entities_table) {
                let old_count = $scope.entities_table.count();

                if(old_count != new_count) {
                    let old_page = $scope.entities_table.page();
                    let old_offset = get_start_offset(old_page, old_count);
                    let new_page = get_page_for_offset(old_offset, new_count, old_count);

                    $scope.entities_table.parameters({
                        'count': new_count,
                        'page': new_page,
                    });

                    try {
                        $scope.$digest();
                    } catch(e) { }
                }
            }

            return new_count;
        }
        let root_datastore_scope = $scope.$parent.$parent;
        root_datastore_scope.$watch('view_height', calculate_table_count);
        let table_count = calculate_table_count(root_datastore_scope.view_height);

        let filter_params = {};

        let current_page = 1;
        let offset = $stateParams.offset;
        let orders = $stateParams.orders;
        if(offset > 0) {
            current_page = get_page_for_offset(parseInt(offset), table_count);
        }

        let common_columns = [
            {
                title: 'Entity key',
                common: true,
            },
        ];

        let current_entities_cache = null;

        function get_entities_from_cache(current_query) {
            if(!current_entities_cache) {
                return null;
            }

            let cached_data = current_entities_cache.data;

            let cache_query = current_entities_cache.query_params;
            let cache_query_offsetless = angular.copy(cache_query);
            delete cache_query_offsetless.limit;
            delete cache_query_offsetless.offset;

            let current_query_offsetless = angular.copy(current_query);
            delete current_query_offsetless.limit;
            delete current_query_offsetless.offset;

            if(compare_objects(cache_query_offsetless, current_query_offsetless)) {
                let offset_diff = current_query.offset - cache_query.offset;
                let limit_diff = current_query.limit - cache_query.limit;
                let limit_diff_abs = Math.abs(limit_diff);

                if(limit_diff > 0) {
                    return null; // requested more than before
                } else if(limit_diff == 0 && offset_diff != 0) {
                    return null; // limit the same, but offset is not
                } else if(offset_diff < 0) {
                    return null; // right boundary out of cache
                } else if(offset_diff > limit_diff_abs) {
                    return null; // left boundary out of cache
                } else if(limit_diff_abs == offset_diff) {
                    return cached_data;
                } else {
                    return cached_data.slice(offset_diff, -(limit_diff_abs - offset_diff));
                }

            } else {
                // another sort/order/filter/etc...
                return null;
            }
        }

        $scope.entities_table = new NgTableParams({
            count: table_count,
            page: current_page,
        }, {
            getData: (params) => {
                let count = params.count();
                let page = params.page();
                let offset = get_start_offset(page, count);

                let orders = params.orderBy();

                let query_params = {
                    limit: count,
                    offset: offset,
                };
                if(orders.length > 0) {
                    query_params['orders'] = orders;
                }
                angular.extend(query_params, filter_params);

                let entities_from_cache = get_entities_from_cache(query_params);
                if(entities_from_cache !== null) {
                    return entities_from_cache;
                }

                $state.go('.', {
                    orders: orders,
                    offset: offset > 0 ? offset : undefined,
                });

                $scope.entities_table_loading = true;
                return $q.when(app_datastore.entities(...request_arguments, query_params)).then((entities) => {
                    current_entities_cache = {
                        data: entities,
                        query_params: query_params,
                    };

                    $scope.entities_table.total(entities.count);

                    $scope.properties = entities.properties;
                    $scope.entities_table_columns = angular.copy(common_columns);
                    for(let property_name in entities.properties) {
                        let property_info = entities.properties[property_name];
                        $scope.entities_table_columns.push({
                            title: property_name,
                            field: property_name,
                            sortable: property_info.indexed ? property_name : null,
                        });
                    }

                    $scope.entities_table_loading = false;
                    return entities;
                });
            },

            counts: [],
        });

        ngTableEventsChannel.onAfterReloadData((params) => {
            $scope.entities_table_pages = params.generatePagesArray();
        }, $scope, $scope.entities_table);

        $scope.refresh_entities = function() {
            current_entities_cache = null;
            $scope.entities_table.reload();
        };

        $scope.filter_dialog = function() {
            $uibModal.open({
                component: 'entitiesFilterDialog',
                size: 'xs',
                resolve: {
                    kind_path: function() {return request_arguments},
                    properties: $scope.properties,
                    app_datastore: app_datastore,
                    filter_params: filter_params
                }
            }).result.then(function(new_filter_params) {
                filter_params = new_filter_params;
                $scope.has_filter_params = !$.isEmptyObject(filter_params);
                $scope.entities_table.page(1).reload();
            });
        }
    },
};
