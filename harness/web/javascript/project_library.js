project_library = {}


project_library.template_dictionary = {};


project_library.basic_types = ['string', 'integer', 'decimal', 'collection(string)', 'collection(decimal)', 'collection(integer)'];


project_library.child_accessor = function(node){
    return node.users || node.projects;
};


project_library.update_template_dictionary = function(node, dictionary){
    var goal = new project_library.get_template_ids_goal(dictionary);
    tree_library.visit_nodes(node, goal);
    project_library.template_dictionary = goal.value;
    return goal.value;

};

project_library.get_template_node_goal = function(node_id){
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



project_library.get_template_ids_goal = function(dictionary){
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


project_library.drop_target_evaluation = {};


project_library.drop_target_evaluation.evaluate_drop_target_clone = function(root, drag_node, node, clone_node){
    switch (drag_node.type) {
        case 'root':
            return project_library.evaluate_root_target_clone(drag_node, node);
        case 'group':
            return project_library.evaluate_group_target_clone(drag_node, node);
        case 'structure':
            return project_library.evaluate_structure_target_clone(drag_node, node);
        case 'template':
            return project_library.evaluate_template_target_clone(root, drag_node, node, clone_node);
        default:
            return project_library.evaluate_field_target(root, drag_node, node);
    }
};


project_library.evaluate_root_target_clone = function(drag_node, node){
    return false;
};

project_library.evaluate_group_target_clone = function(drag_node, node){
    return false;
};

project_library.evaluate_structure_target_clone = function(drag_node, node){
    if (node.type == 'group'){
        return true;
    }
    return false;
};

project_library.evaluate_template_target_clone = function(root, drag_node, node, clone_node){
    if (node.type == 'structure'){
        return true;
    }
    if (node.type == 'template'){
        var custom_fields = project_library.get_custom_fields(root, drag_node, {});
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

project_library.evaluate_field_target = function(root, drag_node, node){
    if (node.type == 'template'){
        if (project_library.basic_types.indexOf(drag_node.type) != -1){
            return true;
        }
        var node_type = project_library.trim_collection(drag_node);
        var node_id = project_library.template_dictionary[node_type];
        var goal = new project_library.get_template_node_goal(node_id);
        tree_library.visit_nodes(root, goal);
        var template_node = goal.value;
        if (template_node){
            var custom_fields = project_library.get_custom_fields(root, template_node, {});
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


project_library.trim_collection = function(node){
    var node_type = node.type;
    if (_.startsWith(node_type, 'collection(') && _.endsWith(node_type, ')')){
        node_type = _.trimStart(node_type, 'collection(');
        node_type = _.trimEnd(node_type, ')');
    }
    return node_type;
};


project_library.get_custom_descendants = function(root, node){
    var descendants = project_library.get_custom_fields(root, node, {});
};


project_library.get_custom_fields = function(root, node, custom_fields){
    var temp_fields = {};
    for (child of tree_library.get_children(node)){
        if (project_library.basic_types.indexOf(child.type) == -1){
            var field_type = project_library.trim_collection(child);
            temp_fields[field_type] = project_library.template_dictionary[field_type];
            custom_fields[field_type] = project_library.template_dictionary[field_type];
        }
    }
    _.forIn(temp_fields, function(node_id, structure_template){
        var goal = new project_library.get_template_node_goal(node_id);
        tree_library.visit_nodes(root, goal);
        var node = goal.value;
        if (node){
            project_library.get_custom_fields(root, node, custom_fields);
        }
    });
    return custom_fields;
};


project_library.drop_target_evaluation.evaluate_drop_target_move = function(root, drag_node, node){
    switch (drag_node.type) {
        case 'root':
            return project_library.evaluate_root_target_move(drag_node, node);
        case 'group':
            return project_library.evaluate_group_target_move(drag_node, node);
        case 'structure':
            return project_library.evaluate_structure_target_move(drag_node, node);
        case 'template':
            return project_library.evaluate_template_target_move(drag_node, node);
        default:
            if (drag_node.parent.type == 'template'){
                if (drag_node.parent == node){
                    return false;
                }
            }
            return project_library.evaluate_field_target(root, drag_node, node);
    }
};



project_library.evaluate_root_target_move = function(drag_node, node){
    return false;
};

project_library.evaluate_group_target_move = function(drag_node, node){
    if (node.type == 'root'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

project_library.evaluate_structure_target_move = function(drag_node, node){
    if (node.type == 'group'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

project_library.evaluate_template_target_move = function(drag_node, node){
    if (node.type == 'structure'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};

project_library.evaluate_field_target_move = function(drag_node, node){
    if (node.type == 'template'){
        if (node == drag_node.parent){
            return false;
        }
        return true;
    }
    return false;
};


project_library.evaluate_field_target_children_move = function(drag_node, node){
    return false;
};
