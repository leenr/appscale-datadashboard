let storage_key = 'apps_selected_app_id';
let session_storage = window.sessionStorage;

class appsService {
    constructor(apps_api) {
        let self = this;

        this.api = apps_api;

        this.available = this.api.all('available').getList().then(function(available_apps) {
            self.available = available_apps;
        });

        this._app_cache = {};
        this._app_id_cache = {};
        this._app_requests = {};
    }

    get selected() {
        let id = session_storage.getItem(storage_key);
        if(!id) return undefined;

        if(this._app_cache[id] === undefined) {
            this._request_app(id);
        }
        return this._app_cache[id];
    }

    set selected(new_app) {
        if(new_app.id) new_app = new_app.id;
        session_storage.setItem(storage_key, new_app);
    }

    _request_app(app_id) {
        if(this._app_requests[app_id]) {
            return this._app_requests[app_id];
        }
        this._app_cache[app_id] = {id: app_id, name: name};

        let self = this;
        let request = this.api.one('apps', app_id).customGET().then(function(app_data) {
            angular.extend(self._app_cache[app_id], app_data);
            return self._app_cache[app_id];
        });
        this._app_requests[app_id] = request;

        return request;
    }
}

export default appsService;
