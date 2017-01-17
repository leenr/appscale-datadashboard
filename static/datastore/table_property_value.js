export default {
    templateUrl: 'static/datastore/table_property_value.html',

    bindings: {
        entity: '<',
        property: '<',
    },

    template: '',
    controller: function($scope) {
        var $ctrl = this;
        $scope.$ctrl = $ctrl;

        function update() {
            let entity = $ctrl.entity;
            let property_name = $ctrl.property;

            let property_info = entity._properties[property_name];
            let value = entity[property_name];

            $scope.value = value;
            $scope.value_full_string = (angular.isDefined(value) && value != null) ? value.toString() : '';
            $scope.property = property_info;

            if(property_info) {
                $scope.data_type = property_info.data_type;

                if(property_info.data_type == 'string') {
                    $scope.value_json_pretty = pretty_json(value);
                }
            }
        }

        $scope.$watch('$ctrl.value', update);
        update();

        function pretty_json(string) {
            if(!angular.isString(string)) {
                return null;
            }
            if(!($.inArray(string.charAt(0), ['[', '{']) >= 0 && $.inArray(string.charAt(string.length - 1), [']', '}']) >= 0)) {
                return null;
            }

            let obj;
            try {
                obj = angular.fromJson(string);
            } catch(e) {
                return null;
            }

            return angular.toJson(obj, 4);
        }
    },
};
