import angular from 'angular';

import dashboard from 'core/angular.js';

let app = dashboard.create_angular_app({name: 'users'});

import usersService from './service.js';
app.service('usersService', usersService);

export default app;
