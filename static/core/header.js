function HeaderController($scope, $state, appsService, usersService) {
    $scope.appsService = appsService;
    $scope.usersService = usersService;
    $scope.$state = $state;
}

export default {
    templateUrl: 'static/core/header.html',
    controller: HeaderController,
};
