import pako from 'pako';


export class UserValue {
    static get DATA_TYPE_NAME() { return 'user'; }

    constructor(data) {
        angular.merge(this, data);
    }

    toString() {
        return '<User ' + this.email + '>';
    }
}

export class PointValue {
    static get DATA_TYPE_NAME() { return 'point'; }

    constructor(data) {
        // TODO
    }
}

export class KeyValue {
    static get DATA_TYPE_NAME() { return 'key'; }

    constructor(data) {
        this.app = data.app;
        this.namespace = data.namespace;

        this.pairs = data.pairs;
        this.pairs_rev = angular.copy(data.pairs).reverse();

        this.urlsafe = data.urlsafe;
    }

    get_entity(app_datastore) {
        // TODO
    }

    get kind() { return this.pairs.slice(-1)[0][0]; }
    get id() { return this.pairs.slice(-1)[0][1]; }

    toString(without_first_kind = false) {
        
    }
}

export class DateTimeValue {
    static get MEANING_NAME() { return 'datetime'; }

    constructor(data) {
        this.datetime = new Date(data * 1000);
    }

    toString() {
        return this.datetime.toLocaleString();
    }
}


export class RepeatedValue extends Array {
    constructor(property, data) {
        super();
        this._property_info = property;
        this.push(...data);
    }

    push(...elements) {
        elements = elements.map((element) => parse_value(this._property_info, element));
        super.push(...elements);
    }

    toString() {
        return '[' + this.map((element) => angular.toJson(element)).join(', ') + ']'
    }
}


let all_complex_types = [
    DateTimeValue,
    KeyValue,
    PointValue,
    RepeatedValue,
    UserValue,
];

export function parse_value(property, data) {
    if(property.repeated && data instanceof Array) {
        return new RepeatedValue(property, data);
    }

    if(property.compressed) {
        data = pako.inflate(atob(data), {to: 'string'});
    }

    for(let type_class of all_complex_types) {
        if((type_class.DATA_TYPE_NAME && type_class.DATA_TYPE_NAME == property.data_type) || (type_class.MEANING_NAME && type_class.MEANING_NAME == property.meaning)) {
            return new type_class(data);
        }
    }
    return data;
}
