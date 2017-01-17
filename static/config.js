System.config({
  baseURL: "/static/",
  defaultJSExtensions: true,
  transpiler: "babel",
  babelOptions: {
    "optional": [
      "runtime",
      "optimisation.modules.system"
    ]
  },
  paths: {
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },

  meta: {
    "*.css": {
      "loader": "css"
    },
    "github:mgonto/restangular@1.5.2/restangular.js": {
      "format": "global",
      "globals": {
        "_": "lodash"
      }
    }
  },

  map: {
    "angular": "github:angular/bower-angular@1.5.8",
    "angular-bootstrap": "github:angular-ui/bootstrap-bower@2.2.0",
    "angular-cache": "npm:angular-cache@4.6.0",
    "angular-css": "github:castillo-io/angular-css@1.0.8",
    "angular-filter": "npm:angular-filter@0.5.11",
    "angular-moment": "npm:angular-moment@1.0.0",
    "angular-route": "github:angular/bower-angular-route@1.5.8",
    "angular-ui-router": "github:angular-ui/angular-ui-router-bower@1.0.0-beta.3",
    "babel": "npm:babel-core@5.8.38",
    "babel-runtime": "npm:babel-runtime@5.8.38",
    "bootstrap": "github:twbs/bootstrap@3.3.7",
    "core-js": "npm:core-js@1.2.7",
    "css": "github:systemjs/plugin-css@0.1.32",
    "ct.ui.router.extras": "npm:ui-router-extras@0.1.3",
    "jquery": "npm:jquery@3.1.1",
    "lodash": "npm:lodash@4.16.6",
    "lodash/lodash": "github:lodash/lodash@4.16.6",
    "lookfirst/oclazyload-systemjs-router": "github:lookfirst/oclazyload-systemjs-router@1.2.2",
    "ng": "github:Hypercubed/systemjs-plugin-ng@0.0.3",
    "ng-annotate": "npm:ng-annotate@1.2.1",
    "ng-table": "npm:ng-table@2.1.0",
    "oclazyload": "github:ocombe/ocLazyLoad@1.0.9",
    "oclazyload-systemjs-router": "github:lookfirst/oclazyload-systemjs-router@1.2.2",
    "pako": "npm:pako@1.0.3",
    "plugin-babel": "npm:systemjs-plugin-babel@0.0.17",
    "restangular": "github:mgonto/restangular@1.5.2",
    "github:Hypercubed/systemjs-plugin-ng@0.0.3": {
      "ng-annotate": "npm:ng-annotate@1.2.1"
    },
    "github:angular-ui/ui-router@0.2.18": {
      "angular": "github:angular/bower-angular@1.5.8"
    },
    "github:angular/bower-angular-route@1.5.8": {
      "angular": "github:angular/bower-angular@1.5.8"
    },
    "github:jspm/nodelibs-assert@0.1.0": {
      "assert": "npm:assert@1.4.1"
    },
    "github:jspm/nodelibs-buffer@0.1.0": {
      "buffer": "npm:buffer@3.6.0"
    },
    "github:jspm/nodelibs-events@0.1.1": {
      "events": "npm:events@1.0.2"
    },
    "github:jspm/nodelibs-os@0.1.0": {
      "os-browserify": "npm:os-browserify@0.1.2"
    },
    "github:jspm/nodelibs-path@0.1.0": {
      "path-browserify": "npm:path-browserify@0.0.0"
    },
    "github:jspm/nodelibs-process@0.1.2": {
      "process": "npm:process@0.11.9"
    },
    "github:jspm/nodelibs-stream@0.1.0": {
      "stream-browserify": "npm:stream-browserify@1.0.0"
    },
    "github:jspm/nodelibs-util@0.1.0": {
      "util": "npm:util@0.10.3"
    },
    "github:jspm/nodelibs-vm@0.1.0": {
      "vm-browserify": "npm:vm-browserify@0.0.4"
    },
    "github:lookfirst/oclazyload-systemjs-router@1.2.2": {
      "angular": "github:angular/bower-angular@1.5.8",
      "angular-ui-router": "github:angular-ui/ui-router@0.2.18",
      "oclazyload": "github:ocombe/ocLazyLoad@1.0.9",
      "ui-router-extras": "github:christopherthielen/ui-router-extras@0.0.13"
    },
    "github:mgonto/restangular@1.5.2": {
      "angular": "github:angular/bower-angular@1.5.8",
      "lodash": "npm:lodash@3.10.1"
    },
    "github:twbs/bootstrap@3.3.7": {
      "jquery": "npm:jquery@3.1.1"
    },
    "npm:@types/angular@1.5.19": {
      "@types/jquery": "npm:@types/jquery@2.0.33"
    },
    "npm:acorn@2.6.4": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "stream": "github:jspm/nodelibs-stream@0.1.0"
    },
    "npm:alter@0.2.0": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "stable": "npm:stable@0.1.5"
    },
    "npm:angular-cache@4.6.0": {
      "angular": "npm:angular@1.5.8"
    },
    "npm:angular-filter@0.5.11": {
      "angular": "npm:angular@1.5.8"
    },
    "npm:angular-moment@1.0.0": {
      "moment": "npm:moment@2.16.0"
    },
    "npm:assert@1.4.1": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "util": "npm:util@0.10.3"
    },
    "npm:babel-runtime@5.8.38": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:buffer@3.6.0": {
      "base64-js": "npm:base64-js@0.0.8",
      "child_process": "github:jspm/nodelibs-child_process@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "ieee754": "npm:ieee754@1.1.8",
      "isarray": "npm:isarray@1.0.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:convert-source-map@1.1.3": {
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0"
    },
    "npm:core-js@1.2.7": {
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "systemjs-json": "github:systemjs/plugin-json@0.1.2"
    },
    "npm:core-util-is@1.0.2": {
      "buffer": "github:jspm/nodelibs-buffer@0.1.0"
    },
    "npm:inherits@2.0.1": {
      "util": "github:jspm/nodelibs-util@0.1.0"
    },
    "npm:lodash@3.10.1": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:ng-annotate@1.2.1": {
      "acorn": "npm:acorn@2.6.4",
      "alter": "npm:alter@0.2.0",
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "convert-source-map": "npm:convert-source-map@1.1.3",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "optimist": "npm:optimist@0.6.1",
      "ordered-ast-traverse": "npm:ordered-ast-traverse@1.1.1",
      "os": "github:jspm/nodelibs-os@0.1.0",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "simple-fmt": "npm:simple-fmt@0.1.0",
      "simple-is": "npm:simple-is@0.2.0",
      "source-map": "npm:source-map@0.5.6",
      "stable": "npm:stable@0.1.5",
      "stringmap": "npm:stringmap@0.2.2",
      "stringset": "npm:stringset@0.2.1",
      "systemjs-json": "github:systemjs/plugin-json@0.1.2",
      "tryor": "npm:tryor@0.1.2"
    },
    "npm:ng-table@2.1.0": {
      "@types/angular": "npm:@types/angular@1.5.19",
      "angular": "npm:angular@1.5.8"
    },
    "npm:optimist@0.6.1": {
      "minimist": "npm:minimist@0.0.10",
      "path": "github:jspm/nodelibs-path@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "wordwrap": "npm:wordwrap@0.0.3"
    },
    "npm:ordered-ast-traverse@1.1.1": {
      "ordered-esprima-props": "npm:ordered-esprima-props@1.1.0"
    },
    "npm:os-browserify@0.1.2": {
      "os": "github:jspm/nodelibs-os@0.1.0"
    },
    "npm:pako@1.0.3": {
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:path-browserify@0.0.0": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:process@0.11.9": {
      "assert": "github:jspm/nodelibs-assert@0.1.0",
      "fs": "github:jspm/nodelibs-fs@0.1.2",
      "vm": "github:jspm/nodelibs-vm@0.1.0"
    },
    "npm:readable-stream@1.1.14": {
      "buffer": "github:jspm/nodelibs-buffer@0.1.0",
      "core-util-is": "npm:core-util-is@1.0.2",
      "events": "github:jspm/nodelibs-events@0.1.1",
      "inherits": "npm:inherits@2.0.1",
      "isarray": "npm:isarray@0.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2",
      "stream-browserify": "npm:stream-browserify@1.0.0",
      "string_decoder": "npm:string_decoder@0.10.31"
    },
    "npm:source-map@0.5.6": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:stream-browserify@1.0.0": {
      "events": "github:jspm/nodelibs-events@0.1.1",
      "inherits": "npm:inherits@2.0.1",
      "readable-stream": "npm:readable-stream@1.1.14"
    },
    "npm:string_decoder@0.10.31": {
      "buffer": "github:jspm/nodelibs-buffer@0.1.0"
    },
    "npm:ui-router-extras@0.1.3": {
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:util@0.10.3": {
      "inherits": "npm:inherits@2.0.1",
      "process": "github:jspm/nodelibs-process@0.1.2"
    },
    "npm:vm-browserify@0.0.4": {
      "indexof": "npm:indexof@0.0.1"
    }
  }
});
