class usersService {
    constructor(users_api) {
        let self = this;

        this.api = users_api;

        this.current = users_api.one('current').customGET().then(function(user_data) {
            self.current = user_data;
            self._users_cache[user_data.id] = user_data;
        });

        this._users_cache = {};
        this._users_requests = {};
    }

    _request_user(user_id) {
        if(this._users_requests[user_id]) {
            return this._users_requests[user_id];
        }
        this._users_cache[user_id] = {id: user_id, email: user_id};

        let self = this;
        let request = this.api.one('users', user_id).customGET().then(function(user_data) {
            angular.extend(self._users_cache[user_id], user_data);
            return self._users_cache[user_id];
        });
        this._users_requests[user_id] = request;

        return request;
    }
}

export default usersService;
