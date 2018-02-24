"use-strict";

angular.module('GhcnApp').factory('resourceFactory', ['$http', '$q', function($http, $q){
    var resourceFactory = {};
    var httpRequestProcessor = {
        'list': []
    };

    resourceFactory.get = function(url, params){
      var q = $q.defer();
      var url = url;
      httpRequestProcessor.list.push(url);
      $http({method : 'GET', url : url, params : params, cache : false})
        .success(function(data, status, headers, config){
          _.pull(httpRequestProcessor.list, url);
          q.resolve(data);
        })
        .error(function(error){
          _.pull(httpRequestProcessor.list, url);
          alert('Get Request Failure. Your view may be out of sync with storage.');
          if(error !== undefined){
            alert(JSON.stringify(error));
          }
        });
      return q.promise
    };


    resourceFactory.post = function(url, dataObject){
      var url = url;
      var q = $q.defer();
      httpRequestProcessor.list.push(url);
      $http({method : 'POST', url : url, cache : false, data : dataObject, params:dataObject})
        .success(function(data, status, headers, config){
          _.pull(httpRequestProcessor.list, url);
          var header = headers();
          if(header["content-type"] === "text/html;charset=UTF-8"){
            if(header.location === undefined){
              window.open(window.location, "_self");
            }else{
              window.open(header.location, "_self");
            }
          }
          q.resolve(data);
        })
        .error(function(xhr, status, errorThrown){
          _.pull(httpRequestProcessor.list, url);
          alert('Post Request Failure. Your view may be out of sync with storage.');
        });
      return q.promise;
    };


return resourceFactory;
}]);

angular.module('GhcnApp').factory('mapFactory', [function(){
    var mapFactory = {};
    return mapFactory;
}]);

angular.module('GhcnApp').factory('structureFactory', ['resourceFactory', '$q',
    function(resourceFactory, $q){
        /* Internal factory methods
        */

        var object_keys = {};
        object_keys['field'] = ['default', 'required', 'type', 'name'];
        object_keys['template'] = ['name', 'description', 'fields'];
        object_keys['structure'] = ['name', 'description', 'templates'];
        object_keys['templates'] = ['name'];

        var get_possible_inverse_variables = function(node_type){
            var possible_inverse_variables = {};
            possible_inverse_variables['template'] = {};
            possible_inverse_variables['template']['fields'] = '_fields';
            possible_inverse_variables['structure'] = {};
            possible_inverse_variables['structure']['templates'] = '_templates';
            possible_inverse_variables['group'] = {};
            possible_inverse_variables['group']['structures'] = '_structures';
            possible_inverse_variables['root'] = {};
            possible_inverse_variables['root']['groups'] = '_groups';
            return possible_inverse_variables[node_type];
        };

        var process_object_closure = function(keys){
            var keys = keys;
            this.operation = function(o){
                var update = {};
               _.forEach(o, function(value, key){
                   if (_.indexOf(keys, key) > -1){
                       update[key] = o[key];
                   }
               });
               return update;
           };
           return this.operation;
       };

       var get_type = function(node){
           switch(node.type){
               case 'group':
               case 'structure':
               case 'template':
                    return node.type;
               default:
                    return 'field';
           }
       }

       var router = {};

       router['update'] = function(update, params){
            var node = update['node'];
            var changes = update['changes'];
            var server_object = {};
            server_object['update'] = {};
            server_object['_id'] = node['_id'];
            server_object['action'] = update['action'];
            server_object['type'] = get_type(node);
            server_object['changes'] = changes;
            var processor = new process_object_closure(object_keys[node['type']]);
            _.forEach(changes, function(change){
                switch(change){
                    case 'fields':
                        var field_processor = new process_object_closure(object_keys['field']);
                        if (node['_fields']){
                            server_object['update'][change] = _.map(node['_fields'], field_processor);
                        } else {
                            server_object['update'][change] = _.map(node['fields'], field_processor);
                        }
                        break;
                    case 'templates':
                        var template_processor = new process_object_closure(object_keys['templates']);
                        if (node['_templates']){
                            server_object['update'][change] = _.flattenDeep(_.map(_.map(node['_templates'], template_processor), _.values));
                        } else {
                            server_object['update'][change] = _.flattenDeep(_.map(_.map(node['templates'], template_processor), _.values));
                        }
                        break;
                    default:
                        if (!_.has(server_object['update'], change)){
                            _.forEach(processor(node),function(value, key){
                                if (_.includes(changes, key)){
                                    server_object['update'][key] = value;
                                }
                            });
                        }
                        break;
                }
            });
            if (server_object['changes'].length){
                params['update'].push(server_object);
            }
            return params;
        };

        router['add'] = function(add, params){
            var server_object = {};
            var node = add['node'];
            server_object['action'] = add['action'];
            server_object['type'] = node['type'];
            server_object['parent'] = add['parent'];
            server_object['order'] = add['order'];
            server_object['update'] = {};
            var processor = new process_object_closure(object_keys[server_object['type']]);
            var possible_inverses = get_possible_inverse_variables(node['type']);
            _.forEach(processor(node),function(value, key){
                if (node[key] == null && _.has(possible_inverses, key) &&
                    _.has(node, possible_inverses[key]) && node[possible_inverses[key]] != null){
                    server_object['update'][key] = node[possible_inverses[key]]
                } else {
                    server_object['update'][key] = value;
                }
            });
            params['update'].push(server_object);
            return params;
        };

        router['remove'] = function(remove, params){
            var server_object = {};
            var node = remove['node'];
            server_object['action'] = remove['action'];
            server_object['_id'] = node['_id'];
            server_object['type'] = node['type'];
            server_object['parent'] = remove['parent'];
            params['update'].push(server_object);
            return params;
        };

        router['move'] = function(move, params){
            var server_object = {};
            var node = move['node'];
            server_object['action'] = move['action'];
            server_object['_id'] = node['_id'];
            server_object['type'] = node['type'];
            server_object['new_parent'] = move['new_parent'];
            server_object['old_parent'] = move['old_parent'];
            server_object['old_name'] = move['old_name'];
            server_object['new_name'] = node['name'];
            params['update'].push(server_object);
            return params;
        };

        /* Exposed factory methods (API)
        */
        var structureFactory = {};

        structureFactory.get_structures = function(){
            var q = $q.defer();
            resourceFactory.get('/parameters/get_tree').then(function(data){
                root = data;
                root.x0 = 1;
                root.y0 = 1;
                q.resolve(root);
            });
            return q.promise;
        };

        structureFactory.update = function(updates){
            var q = $q.defer();
            var params = {};
            params['update'] = [];
            if (Array.isArray(updates)){
                _.forEach(updates, function(update){
                    params = router[update['action']](update, params);
                });
            } else if (_.isObject(updates)){
                params = router[updates['action']](updates, params);
            }
            resourceFactory.post('/parameters/update', params).then(function(data){
                q.resolve(data);
            });
            return q.promise;
        };

        return structureFactory;
}]);
