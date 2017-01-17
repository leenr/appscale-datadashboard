import dashboard from 'core/angular.js';

let app = dashboard.create_angular_app({
    name: 'apps',
});

import appsService from './service.js';
app.service('appsService', appsService);

export default app;
