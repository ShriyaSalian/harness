structure_library = {}


structure_library.template_dictionary = {};

structure_library.get_field_types = function(){
    var field_types = ['fundamental', 'custom'];
    return field_types;
};

structure_library.get_fundamental_field_types = function(){
    var fundamental_types = ['string', 'integer', 'decimal'];
    return fundamental_types;
};

structure_library.is_fundamental_field = function(field){
    var copy = _.cloneDeep(field);
    var collection_regex = new RegExp("^collection(.*)$");
    if (collection_regex.test(copy.type)){
        copy.type = copy.type.replace("collection(", "").replace(")", "");
    }
    if (_.includes(structure_library.get_fundamental_field_types(), copy.type)){
        return true;
    }
    return false;
};

structure_library.child_accessor = function(node){
    return node.groups || node.structures || node.templates || node.fields;
};


structure_library.get_child_type = function(node){
    switch(node.type){
        case 'root':
            return 'groups';
        case 'group':
            return 'structures';
        case 'structure':
            return 'templates';
        case 'template':
            return 'fields';
        default:
            return null;
    }
};


structure_library.get_child_type_singular = function(node){
    switch(node.type){
        case 'root':
            return 'group';
        case 'group':
            return 'structure';
        case 'structure':
            return 'template';
        case 'template':
            return 'field';
        default:
            return null;
    }
};


structure_library.fields_hidden = function(node){
    if (node['fields']){
        return false;
    } else if (node['_fields']) {
        return true;
    }
    return null;
};


structure_library.templates_hidden = function(node){
    if (node['templates']){
        return false;
    } else if (node['_templates']) {
        return true;
    }
    return null;
};


structure_library.structures_hidden = function(node){
    if (node['structures']){
        return false;
    } else if (node['_structures']) {
        return true;
    }
    return null;
};


structure_library.groups_hidden = function(node){
    if (node['groups']){
        return false;
    } else if (node['_groups']) {
        return true;
    }
    return null;
};


structure_library.update_template_dictionary = function(node, dictionary){
    var goal = new structure_library.get_template_ids_goal({});
    tree_library.visit_nodes(node, goal);
    structure_library.template_dictionary = goal.value;
    return goal.value;

};

structure_library.get_template_node_goal = function(node_id){
    this.name = 'get_template_node_goal';
    this.description = 'Walks a tree, looking for the node with the matching id.';
    this.value = null;
    this.stop = false;
    this.operation = function(target){
        if (target.id == node_id) {
            this.value = target;
            this.stop = true;
        }
        return;
    };
};

structure_library.get_nodes_by_ids_goal = function(id_array){
    this.name = 'get_nodes_by_ids_goal';
    this.description = 'Walks a tree, if the node id is in the id_array, grabs that id.';
    this.value = [];
    this.id_array = id_array;
    this.stop = false;
    this.operation = function(node){
        if (this.id_array.indexOf(node.id) != -1){
            this.value.push(node);
        }
    };
};

structure_library.get_matching_types_goal = function(node_types){
    /* Used with tree walking recursion to look for a specified type,
    assembling a list of any node that has that specified type and maintaining an array
    of altered parents. Ignores changes to the root node.
    */
    this.name = 'get_matching_types_goal';
    this.description = 'Get nodes with matching type, maintaining array of altered nodes and parent nodes.';
    this.altered_parents = [];
    this.altered_nodes = [];
    this.stop = false;
    var node_types = node_types;
    this.operation = function(node){
        if (node['type'] != 'root'){
            var parent = node['parent'];
            if (_.includes(node_types, node['type'])){
                if (!_.includes(this.altered_nodes, node)){
                    this.altered_nodes.push(node);
                }
                if (!_.includes(this.altered_parents, parent.id)){
                    this.altered_parents.push(parent.id);
                }
            }
        }
    }
}

structure_library.update_types_goal = function(type_pairs){
    this.name = 'update_types_goal';
    this.description = 'Change field type to new_type if old_type, return array of changed templates.';
    var field_updates = [];
    this.value = [];
    this.stop = false;
    this.type_pairs = type_pairs;
    this.operation = function(node){
        if (node.type != 'root'){
            var parent = node.parent;
            _.forEach(this.type_pairs, function(type_pair){
                if (node['type'] == type_pair['key']){
                    node['type'] = type_pair['value'];
                    if (field_updates.indexOf(parent.id) == -1){
                        field_updates.push(parent.id);
                    }
                }
            });
        }
        this.value = field_updates;
    };
};

structure_library.get_template_ids_goal = function(dictionary){
    this.name = 'get_template_id_goal';
    this.description = 'Walks a tree, building a dictionary of (Structure.template, template_id) key value pairs.';
    this.value = dictionary;
    this.stop = false;
    this.operation = function(target){
        if (target.type == 'template') {
            var parent = target.parent.name;
            var self = target.name;
            var key = parent + '.' + self;
            if (!(_.has(this.value, key))){
                this.value[key] = target.id;
            }
        }
        return;
    };
};


structure_library.drop_target_evaluation = {};


structure_library.drop_target_evaluation.evaluate_drop_target_clone = function(root, drag_node, node, clone_node){
    switch (drag_node.type) {
        case 'root':
            return structure_library.evaluate_root_target_clone(drag_node, node);
        case 'group':
            return structure_library.evaluate_group_target_clone(drag_node, node);
        case 'structure':
            return structure_library.evaluate_structure_target_clone(drag_node, node);
        case 'template':
            return structure_library.evaluate_template_target_clone(root, drag_node, node, clone_node);
        default:
            return structure_library.evaluate_field_target(root, drag_node, node);
    }
};


structure_library.evaluate_root_target_clone = function(drag_node, node){
    return false;
};

structure_library.evaluate_group_target_clone = function(drag_node, node){
    if (node.type == 'root'){
        return true;
    }
    return false;
};

structure_library.evaluate_structure_target_clone = function(drag_node, node){
    if (node.type == 'group'){
        return true;
    }
    return false;
};

structure_library.evaluate_template_target_clone = function(root, drag_node, node, clone_node){
    if (node.type == 'structure'){
        return true;
    }
    if (node.type == 'template'){
        if (node.id == drag_node.id){
            return false;
        }
        var custom_fields = structure_library.get_custom_fields(root, drag_node, {});
        var parent = drag_node.parent.name;
        var self = drag_node.name;
        var key = parent + '.' + self;
        if (!(_.has(custom_fields, key))){
            custom_fields[key] = clone_node.id;
        }
        if (_.values(custom_fields).indexOf(node.id) == -1){
            return true;
        }
        return false;
    }
    return false;
};

structure_library.evaluate_field_target = function(root, drag_node, node){
    if (node.type == 'template'){
        if (structure_library.is_fundamental_field(drag_node)){
            return true;
        }
        var node_type = structure_library.trim_collection(drag_node);
        var node_id = structure_library.template_dictionary[node_type];
        var goal = new structure_library.get_template_node_goal(node_id);
        tree_library.visit_nodes(root, goal);
        var template_node = goal.value;
        if (template_node){
            var custom_fields = structure_library.get_custom_fields(root, template_node, {});
            var parent = template_node.parent.name;
            var self = template_node.name;
            var key = parent + '.' + self;
            if (!(_.has(custom_fields, key))){
                custom_fields[key] = template_node.id;
            }
            if (_.values(custom_fields).indexOf(node.id) == -1){
                return true;
            }
            return false;
        }
    }
    return false;
};


structure_library.evaluate_field_source = function(root, structure, template, test_node){
    /*Evaluates a test node to determine if it can be added as a field type to the
    target node. To do this, it gathers all descendants of the test_node, verifies
    that the target node Structure.template is not in that list of descendants.
    */
    if (test_node.type == 'template'){
        var node_type = test_node.parent.name + '.' + test_node.name;
        var node_id = structure_library.template_dictionary[node_type];
        var goal = new structure_library.get_template_node_goal(node_id);
        tree_library.visit_nodes(root, goal);
        var template_node = goal.value;
        if (template_node){
            var custom_fields = structure_library.get_custom_fields(root, template_node, {});
            var parent = structure.name;
            var self = template.name;
            var key = parent + '.' + self;
            if (!(_.has(custom_fields, key))){
                return true;
            }
            return false;
        }
    }
    return false;
}


structure_library.trim_collection = function(node){
    var node_type = node.type;
    if (_.startsWith(node_type, 'collection(') && _.endsWith(node_type, ')')){
        node_type = _.trimStart(node_type, 'collection(');
        node_type = _.trimEnd(node_type, ')');
    }
    return node_type;
};


structure_library.get_custom_descendants = function(root, node){
    var descendants = structure_library.get_custom_fields(root, node, {});
};


structure_library.get_custom_fields = function(root, node, custom_fields){
    var temp_fields = {};
    for (child of tree_library.get_children(node)){
        if (!structure_library.is_fundamental_field(child)){
            var field_type = structure_library.trim_collection(child);
            temp_fields[field_type] = structure_library.template_dictionary[field_type];
            custom_fields[field_type] = structure_library.template_dictionary[field_type];
        }
    }
    _.forIn(temp_fields, function(node_id, structure_template){
        var goal = new structure_library.get_template_node_goal(node_id);
        tree_library.visit_nodes(root, goal);
        var node = goal.value;
        if (node){
            structure_library.get_custom_fields(root, node, custom_fields);
        }
    });
    return custom_fields;
};


structure_library.drop_target_evaluation.evaluate_drop_target_move = function(root, drag_node, node){
    switch (drag_node.type) {
        case 'root':
            return structure_library.evaluate_root_target_move(drag_node, node);
        case 'group':
            return structure_library.evaluate_group_target_move(drag_node, node);
        case 'structure':
            return structure_library.evaluate_structure_target_move(drag_node, node);
        case 'template':
            return structure_library.evaluate_template_target_move(drag_node, node);
        default:
            if (drag_node.parent.type == 'template'){
                if (drag_node.parent == node){
                    return false;
                }
            }
            return structure_library.evaluate_field_target(root, drag_node, node);
    }
};



structure_library.evaluate_root_target_move = function(drag_node, node){
    return false;
};

structure_library.evaluate_group_target_move = function(drag_node, node){
    if (node.type == 'root'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

structure_library.evaluate_structure_target_move = function(drag_node, node){
    if (node.type == 'group'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

structure_library.evaluate_template_target_move = function(drag_node, node){
    if (node.type == 'structure'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

structure_library.evaluate_field_target_move = function(drag_node, node){
    if (node.type == 'template'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};


structure_library.evaluate_field_target_children_move = function(drag_node, node){
    return false;
};


structure_library.dropdowns = {};

structure_library.dropdowns.structure = [
  {
    text: "Inspect",
    click: "asides.action('inspect', 'structure')"
  },
  {
    text: "Remove",
    click: "modals.remove()"
  },
  {
    text: "New Template",
    click: "asides.action('add', 'template')"
  }
];

structure_library.dropdowns.template = [
  {
    text: "Inspect",
    click: "asides.action('inspect', 'template')"
  },
  {
    text: "Remove",
    click: "asides.action('remove', 'template')"
  },
  {
    text: "New Field",
    click: "asides.action('add', 'field')"
  }
];

structure_library.dropdowns.group = [
  {
    text: "Inspect",
    click: "asides.action('inspect', 'group')"
  },
  {
    text: "Remove",
    click: "modals.remove()"
  },
  {
    text: "New Structure",
    click: "asides.action('add', 'structure')"
  }
];

structure_library.dropdowns.root = [
  {
    text: "New Group",
    click: "asides.action('add', 'group')"
  }
];

structure_library.dropdowns.default = [
    {
      text: "Inspect",
      click: "asides.action('inspect', 'field')"
    },
    {
      text: "Remove",
      click: "asides.action('remove', 'field')"
    }
]

structure_library.process_node = function(node, root){
    /* This function should take a node, clean it up depending on what type
    of node it is (root/group/structure/template/field), adding or assigning
    necessary properties used for the UI.
    */
    switch (node.type) {
        case 'root':
            break;
        case 'group':
            break;
        case 'structure':
            break;
        case 'template':
            structure_library.process_template_node(node, root);
            break;
        default:
            structure_library.process_field_node(node, root);
            break;
    }
}

structure_library.flatten_properties = function(list, property){
    /* Extracts the property from the given list of objects, returning
    a list of just the properties for each object. If an object in the list
    doesn't have the given property, the method adds null to maintain true order.
    */
    var properties = [];
    for (item of list){
        if (_.has(item, property)){
            properties.push(item[property]);
        } else {
            properties.push(null);
        }
    }
    return properties;
};

structure_library.get_all_nodes = function(node){
    /* Walks the specified node, recursively collecting all nodes, whether
    the children are open or closed.
    */
    var node_array = null;
    var goal = new tree_library.get_node_array_goal();
    tree_library.visit_nodes(node, goal);
    node_array = goal.value;
    return node_array;

}

structure_library.update_type_structures = function(root, target, current, method){
    if (method == 'add'){
        var template = current;
    } else if (method == 'update') {
        var template = target['parent'];
    }
    var structure = template['parent'];
    var all_nodes = structure_library.get_all_nodes(root);
    _.forEach(all_nodes, function(test_node){
        if (structure_library.evaluate_field_source(root, structure, template, test_node)){
            if (!(test_node['parent']['name'] == structure['name'] && test_node['name'] == template['name'])){
                var structure_index = structure_library.flatten_properties(target['type_structures'], 'name').indexOf(test_node['parent']['name']);
                if (structure_index == -1){
                    var new_structure = {};
                    new_structure['name'] = test_node['parent']['name'];
                    new_structure['templates'] = [];
                    new_structure['templates'].push(test_node['name']);
                    target['type_structures'].push(new_structure);
                } else {
                    if (target['type_structures'][structure_index]['templates'].indexOf(test_node['name']) == -1){
                        target['type_structures'][structure_index]['templates'].push(test_node['name']);
                    }
                }
            }
        }
    });
};

structure_library.update_type_templates = function(target){
    var structure_index = structure_library.flatten_properties(target.type_structures, 'name').indexOf(target.type_structure);
    target.type_templates = target['type_structures'][structure_index]['templates'];
};


structure_library.update_order = function(node, container){
    /* Creates a child order array, adding it to the node for possible
    child ordering, and also sets the current child order. Works with both a node
    or a parent node (if using with a node only, pass null in for parent).
    */
    if (container){
        var child_type = structure_library.get_child_type(container);
        if (tree_library.has_hidden_children(container)){
            var children = container['_' + child_type];
        } else {
            var children = container[child_type];
        }
    } else {
        var child_type = structure_library.get_child_type(node.parent);
        if (tree_library.has_hidden_children(node.parent)){
            var children = node.parent['_' + child_type];
        } else {
            var children = node.parent[child_type];
        }
    }
    var orders = [];
    for (var i = 0; i < children.length; i++){
        orders.push(i.toString());
    }
    if (container){
        var new_order = children.length.toString();
        orders.push(new_order);
        node.order = new_order;
    } else {
        node.order = children.indexOf(node).toString();
        node.original_order = new_order;
    }
    node.orders = orders;
};

structure_library.make_update_key = function(key, value){
    update = {};
    update['key'] = key;
    update['value'] = value;
    return update;
};

structure_library.get_type_pairs = function(action, original, node, parent){
    var type_pairs = [];
    switch (action){
        case 'update':
            if (original['type'] == 'template'){
                if (node['name']){
                    var old_type = parent['name'] + '.' + original['name'];
                    var old_type_collection = 'collection(' + old_type + ')';
                    var new_type = parent['name'] + '.' + node['name'];
                    var new_type_collection = 'collection(' + new_type + ')';
                    type_pairs.push(structure_library.make_update_key(old_type, new_type));
                    type_pairs.push(structure_library.make_update_key(old_type_collection, new_type_collection));
                }
            }
            break;
        case 'move':
            if (original['type'] == 'template'){
                var old_type = node['old_parent'] + '.' + node['old_name'];
                var old_type_collection = 'collection(' + old_type + ')';
                var new_type = parent['name'] + '.' + node['name'];
                var new_type_collection = 'collection(' + new_type + ')';
                type_pairs.push(structure_library.make_update_key(old_type, new_type));
                type_pairs.push(structure_library.make_update_key(old_type_collection, new_type_collection));
            }
            break;
    };

    return type_pairs;
};

structure_library.get_field_updates = function(root, original, update, parent, action){
    /* When updating a template or structure name, fields that may have this template as
    a type must also change their type to reflect the template change.
    This function creates an update object for every field that may have been altered
    as a result of this change.
    */
    var type_pairs = structure_library.get_type_pairs(action, original, update, parent);
    var goal = new structure_library.update_types_goal(type_pairs);
    tree_library.visit_nodes(root, goal);
    var changed_ids = goal.value;
    var updates = [];
    if (changed_ids.length){
        var get_changes = new structure_library.get_nodes_by_ids_goal(changed_ids);
        tree_library.visit_nodes(root, get_changes);
        var changes = get_changes.value;
        if (changes.length){
            _.forEach(changes, function(change){
                updates.push(structure_library.get_update_object(change, [structure_library.get_child_type(change)]));
            });
        }
    }
    return updates;
};

structure_library.update_ui_node = function(node, parent, update){
    _.forEach(update['changes'], function(value, key){
            node[key] = value;
        });
        if (_.has(update, 'new_order')){
            structure_library.reorder_child_node(parent, node, update['original_order'], update['new_order']);
        }
};

structure_library.reorder_child_node = function(parent, node, original_order, new_order){
    child_type = structure_library.get_child_type(parent);
    parent[child_type].splice(original_order, 1);
    parent[child_type].splice(new_order, 0, node);
};

structure_library.get_new_template = function(new_node, structure){
    var node = {};
    node['structure_id'] = structure['_id'];
    node['name'] = new_node['template_name'];
    node['description'] = new_node['template_description'];
    node['order'] = new_node['order'];
    node['type'] = new_node['type'];
    node['fields'] = new_node['fields'];
    return node;
};

structure_library.get_new_field = function(new_node, template){
    node = {};
    node['template_id'] = template['_id'];
    node['name'] = new_node['field_name'];
    if (new_node['field_required']){
        node['required'] = 'True';
    } else {
        node['required'] = 'False';
    }
    if (new_node['type_class'] == 'fundamental'){
        node['type'] = structure_library.make_field_type(new_node, 'fundamental');
        if (new_node['field_default']){
            node['default'] = new_node['field_default'];
        } else {
            node['default'] = "None";
        }
    } else if (new_node['type_class'] == 'custom'){
        node['type'] = structure_library.make_field_type(new_node, 'custom');
    }
    node['order'] = new_node['order'];
    return node;
};

structure_library.prepare_move_node = function(node, new_parent){
    /* Preparing a node for moving to another parent.
    */
    node['old_name'] = node['name'];
    node['old_parent'] = node['parent']['name'];
    tree_library.ensure_valid_name(node, new_parent, 'name', structure_library);
    return;
};

structure_library.add_new_node_to_container = function(node, container, root, group, callbacks){
    /* A generic method to be used for adding the given node as a child to the given container
    in the given root node. The node is added to the view using the group and given the passed
    callbacks.
    */
    node = tree_library.assign_unique_node_id(node, root);
    node = tree_library.update_descendant_ids(node);
    node.parent = container;
    tree_library.ensure_valid_name(node, container, 'name', structure_library);
    var child_type = structure_library.get_child_type(container);
    var hidden_child_type = '_' + child_type;
    if (tree_library.has_hidden_children(container)){
        container[hidden_child_type].splice(parseInt(node['order']), 0, node);
    } else {
        container[child_type].splice(parseInt(node['order']), 0, node);
        var target_node = group.selectAll(".node_add").data(node);

        var styles = {
            node_class: 'node node_add'
        };

        tree_library.create_node_enter(target_node, target_node, callbacks, styles);
        tree_library.update_node_styles(target_node);
        tree_library.create_node_exit(target_node, target_node);
        target_node.attr('class', 'node');
    }
    return node;

};

structure_library.get_field_change_types = function(){
    /* Returns a dictionary object containing base change types and change types
    that are dependent on base types.
    */
    var change_dictionary = {};
    change_dictionary['changes'] = {
        field_name: 'name'
    };
    return change_dictionary;
};


structure_library.get_field_changes = function(original, clone){
    /* Compares two field node objects, returning an object with a sub object
    containing all changes as key value pairs as well as a true/false changed key.
    */
    var node = {};
    node['template_id'] = clone.parent['_id'];
    var changes = structure_library.get_field_change_types();
    node['changed'] = false;
    node['changes'] = {};
    _.forEach(changes['changes'], function(value, key){
        if (original[key] != clone[key]){
            node['changed'] = true;
            node['changes'][value] = clone[key];
            tree_library.ensure_valid_name(node['changes'], original.parent, 'name', structure_library);
        }
    });
    if (original['field_required'] != clone['field_required']){
        node['changed'] = true;
        if (clone['field_required']){
            node['changes']['required'] = 'True';
        } else {
            node['changes']['required'] = 'False';
        }
    }
    switch (clone['type_class']) {
        case 'custom':
            switch (original['type_class']) {
                case 'custom':
                    if (original['type_structure'] != clone['type_structure'] ||
                        original['type_template'] != clone['type_template'] ||
                        original['type_collection'] != clone['type_collection']){
                            node['changes']['type'] = structure_library.make_field_type(clone, 'custom');
                            node['changed'] = true;
                        }
                    break;
                case 'fundamental':
                    node['changes']['type'] = structure_library.make_field_type(clone, 'custom');
                    node['changed'] = true;
                    break;
            }
            break;
        case 'fundamental':
            switch (original['type_class']) {
                case 'fundamental':
                    if (original['type_base'] != clone['type_base'] ||
                        original['type_collection'] != clone['type_collection']){
                        node['changes']['type'] = structure_library.make_field_type(clone, 'fundamental');
                        node['changed'] = true;
                    }
                    if (original['field_default'] != clone['field_default']){
                        node['changes']['default'] = clone['field_default'];
                        node['changed'] = true;
                    }
                    break;
                case 'custom':
                    node['changes']['type'] = structure_library.make_field_type(clone, 'fundamental');
                    node['changes']['default'] = clone['field_default'];
                    node['changed'] = true;
                    break;
            }
            break;
    }
    if (original['order'] != clone['order']){
        node['new_order'] = clone['order'];
        node['original_order'] = original['order'];
        node['changed'] = true;
    }
    return node;
};

structure_library.remove_fields_by_node_type = function(node, root){
    var node_type = node['parent']['name'] + '.' + node['name'];
    var node_types = [node_type, 'collection(' + node_type + ')'];
    var goal = new structure_library.get_matching_types_goal(node_types);
    tree_library.visit_nodes(root, goal);
    var changed_nodes = goal['altered_nodes'];
    var changed_parents = goal['altered_parents'];
    _.forEach(changed_nodes, structure_library.remove_node);
    var updates = [];
    if (changed_parents.length){
        var get_changes = new structure_library.get_nodes_by_ids_goal(changed_parents);
        tree_library.visit_nodes(root, get_changes);
        var changes = get_changes.value;
        if (changes.length){
            _.forEach(changes, function(change){
                updates.push(structure_library.get_update_object(change, [structure_library.get_child_type(change)]));
            });
        }
    }
    return updates;
};

structure_library.remove_node = function(node){
    /* Removes the specified node from its parent.
    Works with hidden (collapsed) nodes as well as visible (expanded) nodes.
    */
    var parent = node['parent'];
    var child_type = structure_library.get_child_type(parent);
    var hidden_child_type = '_' + child_type;
    if (tree_library.has_hidden_children(parent)){
        var order = parent[hidden_child_type].indexOf(node);
        parent[hidden_child_type].splice(order, 1);
    } else {
        var order = parent[child_type].indexOf(node);
        parent[child_type].splice(order, 1);
    }
};

structure_library.move_node = function(root, node, new_parent){
    structure_library.prepare_move_node(node, new_parent);
    tree_library.move_node(node, new_parent);
    var updates = structure_library.get_field_updates(root, node, node, new_parent, 'move');
    updates.push(structure_library.get_move_object(node, new_parent));
    return updates;

};

structure_library.move_field_node = function(field, old_template, new_template){
    var collection = 'fields';
    if (tree_library.has_hidden_children(old_template)){
        var collection = '_fields';
    }
    var old_index = old_template[collection].indexOf(field);
    if (old_index > -1) {
        old_template[collection].splice(old_index, 1);
    }
    tree_library.ensure_valid_name(field, new_template, 'name', structure_library);
    tree_library.push_child_switch(field, new_template);
    return new_template;
};


structure_library.make_field_from_template = function(node, target){
    var field = {};
    field['name'] = 'new_' + node.parent.name;
    field['type'] = node.parent.name + '.' + node.name;
    field['required'] = "False";
    field['default'] = 'None';
    structure_library.update_order(field, target);
    return field;
};

structure_library.keep_template_field_clone = function(group, node, template, callbacks){
    var field = structure_library.make_field_from_template(node, template);
    structure_library.add_new_node_to_container(field, template, node, group, callbacks);
    return template;
};

structure_library.keep_field_clone = function(group, clone, template){
    tree_library.ensure_valid_name(clone, template, 'name', structure_library);
    template = tree_library.push_child_switch(clone, template);
    var clone_node = group.selectAll(".clone");
    clone_node.attr('class', 'node');
    tree_library.set_style_node_standard(clone_node);
    return template;
};


structure_library.keep_template_clone = function(group, clone, structure){
    /* Prepares a template clone for keeping on the view. Returns the
    template clone.
    */
    tree_library.ensure_valid_name(clone, structure, 'name', structure_library);
    structure = tree_library.push_child_switch(clone, structure);
    var clone_node = group.selectAll(".clone");
    clone_node.attr('class', 'node');
    tree_library.set_style_node_standard(clone_node);
    var database_clone = _.cloneDeep(clone);
    var goal = new structure_library.sanitize_node_for_database_goal();
    tree_library.visit_nodes(database_clone, goal);
    structure_library.set_new_parent(database_clone, structure);
    return database_clone;
};


structure_library.set_new_parent = function(node, new_parent){
    node['parent'] = new_parent;
};


structure_library.merge_new_node_properties = function(old_node, new_node){
    var whitelist_keys = structure_library.get_node_property_whitelist(old_node['type']);
    var blacklist_keys = structure_library.get_node_property_blacklist(old_node['type']);
    var old_keys = _.keys(old_node);
    var new_keys = _.keys(new_node);
    var all_keys = _.union(old_keys, new_keys);
    _.forEach(all_keys, function(key){
        if (_.has(old_node, key)){
            if (_.includes(blacklist_keys, key)){
                delete old_node[key];
            } else if (!_.includes(whitelist_keys, key)){
                if (_.has(new_node, key)){
                    old_node[key] = new_node[key];
                }
            }
        } else if (_.has(new_node, key)) {
            old_node[key] = new_node[key];
        }
    });
};


structure_library.make_field_type = function(source, type){
    var field_type = null;
    switch (type){
        case 'custom':
            field_type = source['type_structure'] + '.' + source['type_template'];
            break;
        case 'fundamental':
            field_type = source['type_base'];
            break;
    }
    if (field_type && source['type_collection']){
        field_type = 'collection(' + field_type + ')';
    }
    return field_type;
}
var get_new_node_dictionary = function(){
    var new_node_dictionary = {};
    new_node_dictionary['field'] = {};
    new_node_dictionary['field']['new_node'] = true;
    new_node_dictionary['field']['name'] = '';
    new_node_dictionary['field']['type'] = 'string';
    new_node_dictionary['field']['required'] = "False";
    new_node_dictionary['field']['default'] = 'None';
    new_node_dictionary['template'] = {};
    new_node_dictionary['template']['new_node'] = true;
    new_node_dictionary['template']['name'] = '';
    new_node_dictionary['template']['type'] = 'template';
    new_node_dictionary['template']['description'] = '';
    new_node_dictionary['template']['fields'] = [];
    new_node_dictionary['structure'] = {};
    new_node_dictionary['structure']['new_node'] = true;
    new_node_dictionary['structure']['name'] = 'None';
    new_node_dictionary['structure']['description'] = 'None';
    new_node_dictionary['structure']['type'] = 'structure';
    new_node_dictionary['structure']['templates'] = [];
    return new_node_dictionary;
};

structure_library.make_new_menu_node = function(node, root){
    var new_node = {};
    var child_type = structure_library.get_child_type_singular(node);
    var new_node_dictionary = get_new_node_dictionary();
    _.forEach(new_node_dictionary[child_type], function(value, key){
        new_node[key] = value;
    });
    var process_string = 'process_' + child_type + '_node';
    structure_library[process_string](new_node, root);
    structure_library.update_order(new_node, node);
    return new_node;
};

structure_library.get_template_changes = function(original, clone){
    /* Compares two template node objects, returning an object with a sub-object
    containing all changes as key value pairs as well as a true/false change key.
    */
    var node = {};
    node['structure_id'] = clone.parent['_id'];
    node['changed'] = false;
    node['changes'] = {};
    if (original['name'] != clone['template_name']){
        node['changes']['name'] = clone['template_name'];
        tree_library.ensure_valid_name(node['changes'], original.parent, 'name', structure_library);
        node['changed'] = true;
    }
    if (original['description'] != clone['template_description']){
        node['changes']['description'] = clone['template_description']
        node['changed'] = true;
    }
    if (original['order'] != clone['order']){
        node['new_order'] = clone['order'];
        node['original_order'] = original['order'];
        node['changed'] = true;
    }
    return node;

};

structure_library.get_update_object = function(node, changes){
    var update = {};
    update['node'] = node;
    update['changes'] = changes;
    update['action'] = 'update';
    return update;
};

structure_library.get_remove_object = function(node){
    var remove = {};
    remove['node'] = node;
    remove['action'] = 'remove';
    remove['parent'] = node['parent']['name'];
    return remove;
};

structure_library.get_move_object = function(node, new_parent){
    var move = {};
    move['node'] = node;
    move['new_parent'] = new_parent['name'];
    move['old_parent'] = node['old_parent'];
    move['old_name'] = node['old_name'];
    move['action'] = 'move';
    return move;
};

structure_library.get_add_object = function(node){
    var add = {};
    add['node'] = node;
    add['action'] = 'add';
    add['parent'] = node['parent']['name'];
    add['order'] = node['order'];
    return add;
};

structure_library.get_node_property_whitelist = function(node_type){
    var properties = {};
    properties['field'] = ['default', 'required', 'type', 'name'];
    properties['template'] = ['name','description','type', 'fields', '_fields', 'structure', 'parent'];
    properties['structure'] = ['name','description','type', 'templates', '_templates','group', 'parent'];
    properties['group'] = ['name','description','type', 'structures', '_structures', 'parent'];
    switch(node_type){
        case 'root':
        case 'group':
        case 'structure':
        case 'template':
            return properties[node_type];
        default:
            return properties['field'];
    }
};

structure_library.get_node_property_blacklist = function(node_type){
    var properties = {};
    properties['field'] = [];
    properties['template'] = ['setup'];
    properties['structure'] = [];
    properties['group'] = [];
    switch(node_type){
        case 'root':
        case 'group':
        case 'structure':
        case 'template':
            return properties[node_type];
        default:
            return properties['field'];
    }
};


structure_library.sanitize_node_for_database_goal = function(node, parent) {
    /* This method takes a node tree and prepares it for entry into a
    database by removing, or sanitizing, each node of properties not on
    a whitelist of properties for that specific node type.
    */
    var name = 'sanitize_node_for_database_goal';
    var description = 'Retrieves a whitelist of properties, removing any node property that is not on the whitelist.';
    this.value = null;
    var stop = false;
    var parent = parent;
    var node = node;
    this.operation = function(target){
        var whitelist = structure_library.get_node_property_whitelist(target.type);
        _.forEach(target, function(value, key){
            if (!_.includes(whitelist, key)){
                delete target[key];
            }
        });
    };
};

structure_library.process_template_node = function(node, root){
    /* Adds properties necessary for modeling in the graphical UI,
    connected to various angular components.
    */
    node.template_name = node.name;
    node.template_description = node.description;
    node.order = 0;
    node.orders = [];
    node.template_translators = [];
    node.template_indeces = [];
    if (!(_.has(node, 'new_node'))){
        structure_library.update_order(node, null);
    }
};

structure_library.process_field_node = function(node, root){
    /* Adds type_class, type_collection, type_base and others to field nodes
    for use by the UI update menu.
    */
    node.field_name = node.name;
    node.type_structures = [];
    node.type_structure = null;
    node.type_template = null;
    node.type_class = 'custom';
    node.type_collection = false;
    node.type_base = node.type;
    node.field_default = null;
    node.field_required = false;
    node.order = 0;
    node.orders = [];
    if (structure_library.is_fundamental_field(node)){
        node.type_class = 'fundamental';
    }
    var collection_regex = new RegExp("^collection(.*)$");
    if (collection_regex.test(node.type)){
        node.type_collection = true;
        node.type_base = node.type.replace("collection(", "").replace(")", "");
    }
    if (node.type_class == 'custom'){
        var type_split = node.type_base.split(".", 2);
        node.type_structure = type_split[0];
        node.type_template = type_split[1];
    }
    if (node.type_class == 'fundamental'){
        if (node.default.toLowerCase() != 'none'){
            node.field_default = node.default;
        }
    }
    if (node.required == "True"){
        node.field_required = true;
    }
    if (node.type_class == 'custom'){
        structure_library.update_type_structures(root, node, null, 'update');
        structure_library.update_type_templates(node);
    }
    if (!(_.has(node, 'new_node'))){
        structure_library.update_order(node, null);
    }
};
