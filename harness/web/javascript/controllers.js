"use-strict";


GhcnApp.controller('viewController', ['$rootScope', '$scope', '$window',
'$timeout', 'resourceFactory',
function($rootScope, $scope, $window, $timeout, resourceFactory){

    $scope.tabSelected = function(name){
        $scope.choose_tab(name);
        $scope.on_resize();
    };

    $scope.on_resize = function() {
    var body = document.getElementById('body');
    var tabs = document.getElementsByTagName('md-tabs')[0];
    var tabs_wrap = document.getElementsByTagName('md-tabs-wrapper')[0];
    var content = document.getElementsByTagName('md-tabs-content-wrapper')[0];
    var height = body.offsetHeight - tabs_wrap.offsetHeight;
    var width = body.offsetWidth;
    $(tabs).height(body.offsetHeight);
    $(tabs).width(width);
    $(content).height(height);
    $(content).width(width);
    var size = {
        'name': 'content-size',
        'height': height+'px',
        'width': width+'px'
        };
    $rootScope.$broadcast('rootScope:broadcast', size);
    };

    $scope.choose_tab = function(tab_name){
        $rootScope.$broadcast('rootScope:change_tab', tab_name);
    };

    angular.element($window).bind('resize', function() {
        $scope.on_resize();
        $scope.$apply();
    });

    $timeout(function() {
        $scope.on_resize();
    }, 300);

}]);


GhcnApp.controller('mapController', ['$rootScope', '$scope', 'resourceFactory',
function($rootScope, $scope, resourceFactory){

    $scope.container = {
        'name': 'content-size',
        'height': '0px',
        'width': '0px'
    };

    $scope.$on('rootScope:change_tab', function (event, data) {
        if (data == 'map'){
            if (!$scope.initial_load){
                $scope.initial_load = true;
                $scope.container = data;
                $scope.map = new ol.Map({
                        target: 'map',
                        layers: [
                            new ol.layer.Tile({
                                name: 'Satellite',
                                source: new ol.source.OSM()
                            })
                        ],
                        view: new ol.View({
                            center: ol.proj.fromLonLat([-105.1314,40.6147]),
                            zoom: 3
                        })
                    });
                $scope.map.on('click', function() {
                });
            }
        }
    });


    $scope.$on('rootScope:broadcast', function (event, data) {
        $scope.container = data;
      });


    $scope.program = {
        options: ['ghcnm','ushcn','northam'],
        selection: 'ghcnm',
        changed: function(){
        }
    };

    $scope.parameter = {
        options: ['tmax','tmin','tavg'],
        selection: 'tmax',
        changed: function(){
        }
    };

    $scope.station_tools = {
        get_all_stations: function(){
            resourceFactory.get("/get_all_stations_by_program/ghcnm").then(function(data){
                stations = station_library.get_ol_stations(data);
                layer = map_library.make_point_layer('All Stations', stations);
                map_library.add_layer_to_map($scope.map, layer);
            });
        },
        get_random_stations: function(){
            resourceFactory.get("/get_random_stations_by_program/ghcnm").then(function(data){
                stations = station_library.get_ol_stations(data);
                layer = map_library.make_point_layer('Random Stations', stations);
                map_library.add_layer_to_map($scope.map, layer);
            });
        }
    };

    $scope.zoom = function(){
        map_library.zoom_map($scope.map);
    };

    $scope.initial_load = false;


}]);


GhcnApp.controller('componentController', ['$scope', 'resourceFactory',
    function($scope, resourceFactory){

}]);


GhcnApp.controller('functionController', ['$scope', 'resourceFactory',
    function($scope, resourceFactory){
}]);


GhcnApp.controller('workflowController', ['$scope', 'resourceFactory',
    function($scope, resourceFactory){
}]);


GhcnApp.controller('projectController', ['$scope', '$modal', '$tooltip', '$dropdown', 'resourceFactory',
    function($scope, resourceFactory){
}]);


GhcnApp.controller('evaluationController', ['$scope', 'resourceFactory',
    function($scope, resourceFactory){
}]);


GhcnApp.controller('structureController', ['$scope', '$compile', '$modal', '$aside', '$tooltip', '$popover',
                                           '$dropdown', 'resourceFactory', 'structureFactory',
    function($scope, $compile, $modal, $aside, $tooltip, $popover, $dropdown, resourceFactory, structureFactory){

        var first_look = true;
        var loaded = false;
        var node_count = 0;
        var dragging = false;
        var root_node = null;
        var drag_node = null;
        var drop_node = null;
        var current_node = null;
        var pan_timer = false;
        var move_action = null;
        var node_clone = null;
        var node_copy = null;
        var d3_tree = null;
        var d3_canvas = null;
        var d3_group = null;
        var server_string = 'http://localhost:8018';
        var structure_div = '#structure-tree';

        $scope.menu_node = null;

        var container = {
            'name': 'content-size',
            'height': '0px',
            'width': '0px'
        };

        var update_d3 = function(target){
            /* A method that updates the d3 tree view.
            This function accepts the current node (top level of change)
            and recalculates/redraws the d3 tree. It should be called whenever
            the view needs to change.
            */
            tree_library.update(d3_group, d3_tree, root_node, target, node_count, callbacks);
            structure_library.update_template_dictionary(root_node, structure_library.template_dictionary);
        };

        $scope.fields = {};

        $scope.fields.types = structure_library.get_field_types();
        $scope.fields.fundamental_types = structure_library.get_fundamental_field_types();
        $scope.fields.type_structures = [];
        $scope.fields.type_templates = [];
        $scope.fields.orders = [];

        $scope.modals = {};

        $scope.asides = {};

        $scope.asides.action = function(action, type){
            switch (action){
                case 'add':
                    $scope.menu_node = structure_library.make_new_menu_node(current_node, root_node);
                case 'inspect':
                    var template = server_string + "/html/menus/"+ action +"/"+ type +".html";
                    var aside = $aside({scope: $scope, show:true, templateUrl: template});
                    aside.$promise.then(function(){
                        aside.show();
                    });
                    break;
                case 'remove':
                    var parent = current_node.parent;
                    var updates = [];
                    switch (type){
                        case 'template':
                            structure_library.remove_fields_by_node_type(current_node, root_node);
                        case 'structure':
                            updates.push(structure_library.get_remove_object(current_node));
                            break;
                        default:
                            updates.push(structure_library.get_update_object(parent, [structure_library.get_child_type(parent)]));
                            break;
                    }
                    structure_library.remove_node(current_node);
                    update_d3(parent);
                    structureFactory.update(updates);
                default:
                    break;
            }
        };

        $scope.asides.template = {};

        $scope.asides.template.change_type_name = function(){
        };

        $scope.asides.template.save = function(method, hide){
            switch(method){
                case 'add':
                    var node = structure_library.get_new_template($scope.menu_node, current_node);
                    var new_node = structure_library.add_new_node_to_container(node, current_node, root_node, d3_group, callbacks);
                    update_d3(current_node);
                    structureFactory.update(structure_library.get_add_object(new_node)).then(function(data){
                        new_node['_id'] = data[0]['_id'];
                    });
                    break;
                case 'update':
                    var node = structure_library.get_template_changes(node_copy, $scope.menu_node);
                    var parent_node = current_node['parent'];
                    if (node['changed']){
                      var updates = structure_library.get_field_updates(root_node, current_node, node['changes'], parent_node, 'update');
                      structure_library.update_ui_node(current_node, parent_node, node);
                      update_d3(current_node);
                      updates.push(structure_library.get_update_object(current_node, _.keys(node['changes'])));
                      updates.push(structure_library.get_update_object(current_node.parent, ['templates']));
                      structureFactory.update(updates);
                    }
                    break;
                default:
                    break;
            }
            hide();
        };

        $scope.asides.template.cancel = function(hide){
            hide();
        };

        $scope.asides.field = {};

        $scope.asides.field.change_type_name = function(){
        };

        $scope.asides.field.change_type_class = function(method){
            structure_library.update_type_structures(root_node, $scope.menu_node, current_node, method);
        };

        $scope.asides.field.change_type_structure = function(){
            structure_library.update_type_templates($scope.menu_node);
        };

        $scope.asides.field.change_type_template = function(){
        };

        $scope.asides.field.change_order = function(){
        };

        $scope.asides.field.change_type_count = function(){
            var e = document.getElementById("field_inspector_field_type_count");
            if ($scope.menu_node.type_collection) {
                e.innerHTML = "Collection";
            } else {
                e.innerHTML = "Single";
            }
        };

        $scope.asides.field.change_field_required = function(){
            var e = document.getElementById("field_inspector_field_required");
            if ($scope.menu_node.field_required) {
                e.innerHTML = "True";
            } else {
                e.innerHTML = "False";
            }
        };

        $scope.asides.field.save = function(method, hide){
            switch(method){
                case 'add':
                    var node = structure_library.get_new_field($scope.menu_node, current_node);
                    structure_library.add_new_node_to_container(node, current_node, root_node, d3_group, callbacks);
                    update_d3(current_node);
                    structureFactory.update(structure_library.get_update_object(current_node, ['fields']));
                    break;
                case 'update':
                    var node = structure_library.get_field_changes(node_copy, $scope.menu_node);
                   if (node['changed']){
                       structure_library.update_ui_node(current_node, current_node.parent, node);
                       update_d3(current_node);
                       structureFactory.update(structure_library.get_update_object(current_node.parent, ['fields']));
                   }
                    break;
                default:
                    break;
            }
            hide();
        };

        $scope.asides.field.cancel = function(hide){
            hide();
        };

        $scope.dropdowns = structure_library.dropdowns;

        $scope.$on('rootScope:broadcast', function (event, data) {
            container = data;
            adjust_sizes();
          });


          $scope.$on('rootScope:change_tab', function (event, data) {
              if (data == 'structures'){
                  if (first_look){
                      first_look = false;
                      if (loaded){
                          tree_library.center_tree(current_node, container, callbacks.zoom_listener);
                      } else {
                          get_structures(true);
                      }
                  }
              }
            });


        var adjust_sizes = function(){
            d3_canvas.attr('height', container.height);
            d3_canvas.attr('width', container.width);
            d3_tree = d3_tree.size([container.height, container.width])
        };


    var callbacks = {};

    callbacks.node_type = 'standard';

    callbacks.node_types = ['root', 'group', 'structure', 'template', 'field'];

    callbacks.drag_callback = function(drag_target, action){
        move_action = action;
        drop_node = drag_target;
        $scope.$apply();
    }

    callbacks.zoom = function(){
        d3_group.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        return;
    };

    callbacks.zoom_listener = d3.behavior.zoom().scaleExtent([0.1, 5]).on("zoom", callbacks.zoom);

    callbacks.child_single_click = function(node) {
        if (d3.event.defaultPrevented) {
            return;
        }
        current_node = node;
        tree_library.toggle_direct_children(current_node);
        update_d3(current_node);
        adjust_sizes();
    };

    callbacks.menu_click = function(node) {
        if (d3.event.defaultPrevented) {
            return;
        }
        current_node = node;
        node_copy = _.cloneDeep(node);
        structure_library.process_node(node_copy, root_node);
        $scope.menu_node = _.cloneDeep(node_copy);
    };

    callbacks.pan_click = function(node) {
        if (d3.event.defaultPrevented) {
            return;
        }
        current_node = node;
        coordinates = tree_library.center_node(current_node,
            callbacks.zoom_listener.scale(), container.height, container.width);
        callbacks.zoom_listener.translate(coordinates);
        tree_library.toggle_menu(node);
        adjust_sizes();
    };

    callbacks.compile = function(element){
      var el = angular.element(this);
      $scope = el.scope();
        $injector = el.injector();
        $injector.invoke(function($compile){
           $compile(el)($scope)
        })
    };

    callbacks.drag_listener = d3.behavior.drag()
        .on("dragstart", function(node) {
            if (node.type == 'root') {
                return;
            }
            d3.event.sourceEvent.stopPropagation();
        })
        .on("drag", function(node) {
            current_node = node;
            drag_node = node;
            pan_boundary = 20;
            if (node.type == 'root') {
                return;
            }
            if (!dragging){
                dragging = true;
                node_clone = tree_library.get_cloned_node(d3_group, d3_tree, root_node, this, callbacks);
                tree_library.initiate_drag(d3_group, d3_tree, root_node, node, node_clone, structure_library.drop_target_evaluation);
            }
            relative_coordinates = d3.mouse($('svg').get(0));
            node.x0 += d3.event.dy;
            node.y0 += d3.event.dx;
            var update_node = d3.select(this);
            update_node.attr("transform", "translate(" + node.y0 + "," + node.x0 + ")");
        }).on("dragend", function(node) {
            var dragend = function(target){
                dragging = false;
                if (node.type == 'project') {
                    return;
                }
                switch (move_action) {
                    case 'clone':
                        var current_parent = tree_library.get_parent(drag_node);
                        switch (node_clone.type){
                            case 'root':
                            case 'group':
                            case 'structure':
                                tree_library.keep_clone(d3_group, node_clone, current_parent);
                                break;
                            case 'template':
                                if (drop_node.type == 'template'){
                                    current_node = structure_library.keep_template_field_clone(d3_group, node_clone, drop_node, callbacks);
                                    structureFactory.update(structure_library.get_update_object(drop_node, ['fields']));
                                } else if (drop_node.type == 'structure') {
                                    var database_clone = structure_library.keep_template_clone(d3_group, node_clone, drop_node);
                                    var add_object = structure_library.get_add_object(database_clone);
                                    structureFactory.update(add_object).then(function(data){
                                        structure_library.merge_new_node_properties(node_clone, data[0]);
                                    });
                                }
                                break;
                            default:
                                structure_library.keep_field_clone(d3_group, node_clone, drop_node);
                                structureFactory.update(structure_library.get_update_object(drop_node, ['fields']));
                                break;
                        }
                        break;
                    case 'move':
                        switch (drag_node['type']){
                            case 'root':
                            case 'group':
                            case 'structure':
                            case 'template':
                                var update = structure_library.move_node(root_node, drag_node, drop_node);
                                structureFactory.update(update);
                                break;
                            default:
                                var template = drag_node.parent;
                                current_node = structure_library.move_field_node(drag_node, template, drop_node);
                                var update = [];
                                update.push(structure_library.get_update_object(template, ['fields']));
                                update.push(structure_library.get_update_object(drop_node, ['fields']));
                                structureFactory.update(update);
                                break;
                        }
                        break;
                    default:
                        break;
                }
                tree_library.end_drag(target);
                update_d3(current_node);

            };
            if (dragging){
                dragend(this);
            }
        });

    var get_structures = function(translate){
        root_node = structureFactory.get_structures().then(function(root){
            loaded = true;
            root_node = root;
            current_node = root_node;
            update_d3(current_node);
            if (translate){
                tree_library.center_tree(current_node, container, callbacks.zoom_listener);
            }
        });
    };

    var initialize = function(){
        d3_tree = tree_library.create_tree(container, structure_library.child_accessor);
        d3_canvas = tree_library.create_tree_canvas(structure_div);
        d3_group = tree_library.create_tree_group(d3_canvas);
        tree_library.add_callbacks(d3_canvas, [callbacks.zoom_listener]);
        loaded = get_structures(false);
    };


    initialize();

}]);
