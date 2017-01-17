import { parse_value, KeyValue } from './datastore_types.js';


const DEFAULT_PROPERTY_DICT = {
    compressed: false,
    repeated: false,
};

export class PropertiesInfo {
    _add(name, property_dict) {
        if(name in this && this[name].data_type != 'null') {
            let current_info = this[name];
            let new_info = property_dict;

            // skip null, as we does not have almost all information about in this state
            if(new_info.data_type == 'null') {
                return;
            }

            for(let attr_name in new_info) {
                if(attr_name in new_info && attr_name in current_info && new_info[attr_name] != current_info[attr_name]) {
                    current_info[attr_name] = undefined;
                }
            }

        } else {
            this[name] = angular.extend({}, DEFAULT_PROPERTY_DICT, property_dict);
        }
    }

    _extend(other) {
        for(let name in other) {
            this._add(name, other[name]);
        }
    }
}

export class Entity {
    constructor(entity_dict) {
        this._properties = new PropertiesInfo();
        this._data = entity_dict.data;

        for(let property_name in entity_dict.properties) {
            let property_dict = entity_dict.properties[property_name];
            this._properties._add(property_name, property_dict);

            let data = this._data[property_name];
            let value = parse_value(property_dict, data);

            this[property_name] = value;
        }

        this.key = new KeyValue(entity_dict.key);

        Object.defineProperties(this, {
            key: {enumerable: false},
            _properties: {enumerable: false},
            _data: {enumerable: false},
        });
    }

    [Symbol.iterator]() {
        let index = -1;
        let data = this._values;

        return {
            next: () => ({
                value: data[++index],
                done: !(index in data),
            })
        };
    }
}

export class EntityList extends Array {
    constructor(entities, next_cursor, count) {
        super();

        this.properties = new PropertiesInfo();

        this.push(...entities);

        this.next_cursor = next_cursor;
        this.count = count;
    }

    push(...entities) {
        for(let entity of entities) {
            if(!(entity instanceof Entity)) {
                entity = new Entity(entity);
            }
            super.push(entity);
            this.properties._extend(entity._properties);
        }
    }

    slice(...args) {
        return new EntityList(super.slice(...args), this.next_cursor, this.count);
    }
}
