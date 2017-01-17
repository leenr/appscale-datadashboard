import { Entity, EntityList } from './datastore_entity.js';

export default ($q, CacheFactory, datastore_api) => {
    return class {
        constructor(app_id) {
            this._app_id = app_id;

            let cache_id = 'datastore_app_' + this._app_id;
            this._cache = CacheFactory.get(cache_id);
            if(!this._cache) this._cache = CacheFactory(cache_id);

            this._app_api = datastore_api.one('apps', this._app_id);

            this._gapi_run_query = datastore_api.all('datastore_api/v1/' + this._app_id + ':runQuery');
            this._gapi_lookup = datastore_api.all('datastore_api/v1/' + this._app_id + ':lookup');

            this.__pending = {'__cache': 'pending'};
        }

        _cached(cache_key, func) {
            let res = this.__pending;

            if(!this._cache.info(cache_key)) {
                this._cache.put(cache_key, res);
                $q.when(func()).then((res) => this._cache.put(cache_key, res));
            } else {
                res = this._cache.get(cache_key);
            }

            return res != this.__pending ? res : undefined;
        }

        get namespaces() {
            return this._cached('namespaces', () => this._app_api.all('namespaces').getList());
        }

        _namespace_api(namespace) {
            return namespace ? this._app_api.one('namespaces', namespace) : this._app_api;
        }
        _namespace_cache_key(namespace) {
            return 'namespace_' + namespace
        }

        kinds(namespace = '') {
            return this._cached(this._namespace_cache_key(namespace) + '_kinds', () => this._namespace_api(namespace).all('kinds').getList());
        }

        _kind_api(namespace = '', kind) {
            return this._namespace_api(namespace).one('kinds', kind);
        }

        entities(namespace = '', kind, query_params = {limit: 50}) {
            return this._kind_api(namespace, kind).all('entities').getList(query_params).then((entities) => new EntityList(entities, entities.next_cursor, entities.count));
        }
    }
};
