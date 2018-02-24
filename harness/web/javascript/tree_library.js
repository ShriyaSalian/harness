tree_library = {}


tree_library.create_tree = function(container, child_accessor){
    var tree = d3.layout.tree().size([container.height,
        container.width]).children(child_accessor);
    return tree;
};


tree_library.create_tree_canvas = function(element){
    var canvas = d3.select(element).append("svg").attr("class", "overlay");
    return canvas;
};


tree_library.create_tree_group = function(canvas){
    var group = canvas.append('g');
    return group;
};


tree_library.add_callbacks = function(canvas, callbacks){
    /* Accepts an array of callbacks, adding each in turn to the canvas object.
    */
    _.forEach(callbacks, function(callback){
        canvas.call(callback);
    });
    return;
};


tree_library.center_tree = function(node, container, zoom){
    var coordinates = tree_library.center_node(node, zoom.scale(), container.height, container.width);
    zoom.translate(coordinates);
    return;
};

tree_library.ensure_valid_name = function(child, container, key, function_library){
    /* When adding a new child to a container, ensure the child has a valid name.
    If the child name is not unique (if it is a duplicate), the child will get
    an additional underscore and a number until the child name is unique.
    Valid names also must be non empty.
    */
    var child_type = function_library.get_child_type_singular(container);

    if (!child[key]){
        child[key] = 'new_' + child_type;
    }
    var counter = 0;
    var recursive_look = function(child, container, collection, counter){
        var duplicate = false;
        _.forEach(container[collection], function(node){
            if (node[key] == child[key]){
                if (counter == 0){
                    child[key] += '_';
                }
                child[key] += counter;
                counter++;
                duplicate = true;
            }
        })
        if (duplicate){
            recursive_look(child, container, collection, counter);
        }
        return;
    }
    var collection = function_library.get_child_type(container);
    if (tree_library.has_hidden_children(container)){
        var collection = '_' + collection;
    }
    recursive_look(child, container, collection, counter);
    return child[key];
};

tree_library.center_node = function (node, scale, pixel_height, pixel_width) {
    var duration = 750;
    x = -node.y0;
    y = -node.x0;
    height = tree_library.pixel_to_value(pixel_height);
    width = tree_library.pixel_to_value(pixel_width);
    x = x * scale + width / 5;
    y = y * scale + height / 2;
    d3.select('g').transition().duration(duration)
        .attr("transform", "translate(" + x + "," + y + ")scale(" + scale + ")");
    return [x,y];
};


tree_library.collapse_all = function(node) {
    if (node.structures) {
        node._structures = node.structures;
        node._structures.forEach(tree_library.collapse_all);
        node.structures = null;
    } else if (node.templates){
        node._templates = node.templates;
        node._templates.forEach(tree_library.collapse_all);
        node.templates = null;
    } else if (node.fields){
        node._fields = node.fields;
        node._fields.forEach(tree_library.collapse_all);
        node.fields = null;
    } else if (node.groups) {
        node._groups = node.groups;
        node._groups.forEach(tree_library.collapse_all);
        node.groups = null;
    }
};


tree_library.collapse_one = function(node){
    if (node.structures) {
        node._structures = node.structures;
        node.structures = null;
    } else if (node.templates){
        node._templates = node.templates;
        node.templates = null;
    } else if (node.fields){
        node._fields = node.fields;
        node.fields = null;
    } else if (node.groups){
        node._groups = node.groups;
        node.groups = null;
    }

};


tree_library.diagonal = d3.svg.diagonal().projection(function(node){
    return [node.y, node.x];
});


tree_library.end_drag = function(dom_node) {
    d3.selectAll('.move_circle').attr('class', 'move_circle');
    d3.selectAll('.clone_circle').attr('class', 'clone_circle');
    d3.select(dom_node).attr('class', 'node');
    d3.select(dom_node).select('.move_circle').attr('pointer-events', '');
    d3.select(dom_node).select('.clone_circle').attr('pointer-events', '');
};


tree_library.expand_all = function(node) {
    if (node._structures) {
        node.structures = node._structures;
        node.structures.forEach(tree_library.expand_all);
        node._structures = null;
    } else if (node._templates){
        node.templates = node._templates;
        node.templates.forEach(tree_library.expand_all);
        node._templates = null;
    } else if (node._fields){
        node.fields = node._fields;
        node.fields.forEach(tree_library.expand_all);
        node._fields = null;
    } else if (node._groups){
        node.groups = node._groups;
        node.groups.forEach(tree_library.expand_all);
        node._groups = null;
    }
};


tree_library.expand_one = function(node) {
    if (node._structures) {
        node.structures = node._structures;
        node._structures = null;
    } else if (node._templates){
        node.templates = node._templates;
        node._templates = null;
    } else if (node._fields){
        node.fields = node._fields;
        node._fields = null;
    } else if (node._groups){
        node.groups = node._groups;
        node._groups = null;
    }
};


tree_library.get_levels = function(width_array){
    var self = this;
    this.widths = width_array;
    this.get_child_count = function(level, node){
        if (node.structures && node.structures.length > 0) {
            if (this.widths.length <= level + 1) {
                this.widths.push(0);
            }
            this.widths[level + 1] += node.structures.length;
            node.structures.forEach(function(child) {
                self.get_child_count(level + 1, child);
            });
        } else if (node.templates && node.templates.length > 0){
            if (this.widths.length <= level + 1) {
                this.widths.push(0);
            }
            this.widths[level + 1] += node.templates.length;
            node.templates.forEach(function(child) {
                self.get_child_count(level + 1, child);
            });
        } else if (node.fields && node.fields.length > 0){
            if (this.widths.length <= level + 1) {
                this.widths.push(0);
            }
            this.widths[level + 1] += node.fields.length;
            node.fields.forEach(function(child) {
                self.get_child_count(level + 1, child);
            });
        } else if (node.groups && node.groups.length > 0){
            if (this.widths.length <= level + 1) {
                this.widths.push(0);
            }
            this.widths[level + 1] += node.groups.length;
            node.groups.forEach(function(child) {
                self.get_child_count(level + 1, child);
            });
        }
    };
};


tree_library.leave_drop_zone = function(target_node) {
    return null;
};


tree_library.enter_drop_zone = function(target_node) {
    return target_node;
};


tree_library.pan = function(group, dom_node, direction, pan_timer) {
    var speed = 200;
    if (pan_timer) {
        clearTimeout(pan_timer);
        translate_coordinates = d3.transform(group.attr("transform"));
        if (direction == 'left' || direction == 'right') {
            translate_x = direction == 'left' ? translate_coordinates.translate[0] + speed : translate_coordinates.translate[0] - speed;
            translate_y = translate_coordinates.translate[1];
        } else if (direction == 'up' || direction == 'down') {
            translate_x = translate_coordinates.translate[0];
            translate_y = direction == 'up' ? translate_coordinates.translate[1] + speed : translate_coordinates.translate[1] - speed;
        }
        scale_x = translate_coordinates.scale[0];
        scale_y = translate_coordinates.scale[1];
        scale = zoomListener.scale();
        svgGroup.transition().attr("transform", "translate(" + translateX + "," + translateY + ")scale(" + scale + ")");
        d3.select(domNode).select('g.node').attr("transform", "translate(" + translateX + "," + translateY + ")");
        zoomListener.scale(zoomListener.scale());
        zoomListener.translate([translateX, translateY]);
        panTimer = setTimeout(function() {
            pan(domNode, speed, direction);
        }, 50);
    }
};


tree_library.pixel_to_value = function(pixel){
    if (pixel){
        return Number(pixel.replace('px', ''));
    } else {
        return 0;
    }
};


tree_library.sort_nodes = function(nodes, sort_key) {
        nodes.sort(function(a, b) {
            return b[sort_key] < a[sort_key] ? 1 : -1;
        });
        return nodes;
};


tree_library.toggle_all_children = function(node){
    if (node.groups || node.structures || node.templates || node.fields) {
        tree_library.collapse_all(node);
    } else if (node._groups || node._structures || node._templates || node._fields) {
        tree_library.expand_all(node);
    }
    return node;
};


tree_library.toggle_direct_children = function(node){
    if (node.groups || node.structures || node.templates || node.fields) {
        tree_library.collapse_one(node);
    } else if (node._groups || node._structures || node._templates || node._fields) {
        tree_library.expand_one(node);
    }
    return node;
};



tree_library.toggle_menu = function(node){
    return;
};


tree_library.has_children = function(node){
    if (tree_library.has_visible_children(node) ||
        tree_library.has_hidden_children(node)){
            return true;
        }
    return false;
};


tree_library.has_visible_children = function(node){
    if (node.groups || node.structures || node.templates || node.fields){
        return true;
    }
    return false;
};


tree_library.has_hidden_children = function(node){
    if (node._groups || node._structures || node._templates || node._fields){
        return true;
    }
    return false;
};


tree_library.get_non_empty_element = function(elements){
    for (element of elements){
        if (element){
            return element;
        }
    }
};


tree_library.store_node_positions = function(nodes){
    nodes.forEach(function(node) {
        node.x0 = node.x;
        node.y0 = node.y;
    });
}


tree_library.update = function(group, tree, root_node, focus_node, node_count, callbacks) {
    var duration = 750;
    var levels = new tree_library.get_levels([1]);
    levels.get_child_count(0, root_node);
    var tree_height = d3.max(levels.widths) * 20;
    var tree_width = tree_library.pixel_to_value(group.attr('width'));
    var tree = tree.size([tree_height, tree_width]);

    var nodes = tree.nodes(root_node).reverse();
    var links = tree.links(nodes);

    var label_length = tree_library.setup(root_node).longest_label_goal;

    var target_node = group.selectAll("g.node")
        .data(nodes, function(node) {
            return node.id || (node.id = ++node_count);
        });

    var link = group.selectAll("path.link")
        .data(links, function(node) {
            return node.target.id;
        });


    nodes.forEach(function(node) {
        node.y = (node.depth * (label_length * 5));
    });

    tree_library.create_node_enter(target_node, focus_node, callbacks);
    tree_library.update_node_styles(target_node);
    tree_library.create_node_exit(target_node, focus_node);
    tree_library.create_node_transition(target_node);
    tree_library.create_link_enter(link, focus_node);
    tree_library.create_link_transition(link);
    tree_library.create_link_exit(link, focus_node);
    tree_library.store_node_positions(nodes);
    tree_library.add_dropdowns(callbacks);
};


tree_library.add_dropdowns = function(callbacks){
        d3.selectAll('.node_name').filter("*:not(.has_dropdown)")
      .classed('has_dropdown', true).each(callbacks.compile);
};


tree_library.create_link_enter = function(link, focus_node){
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(link) {
            if (focus_node){
                var o = {
                    x: focus_node.x0,
                    y: focus_node.y0
                };
                return tree_library.diagonal({
                    source: o,
                    target: o
                });
            } else {
                var i = {
                    x: link.source.x0,
                    y: link.source.y0
                };
                var f = {
                    x: link.target.x0,
                    y: link.target.y0
                }
                return tree_library.diagonal({
                    source: i,
                    target: f
                });
            }
        });
};

tree_library.create_link_exit = function(link, focus_node){
    var duration = 750;
    link.exit().transition()
        .duration(duration)
        .attr("d", function(node) {
            var o = {
                x: focus_node.x,
                y: focus_node.y
            };
            return tree_library.diagonal({
                source: o,
                target: o
            });
        })
        .remove();
};


tree_library.create_link_transition = function(link){
    var duration = 750;
    link.transition()
        .duration(duration)
        .attr("d", tree_library.diagonal);
};


tree_library.create_node_enter = function(target_node, focus_node, callbacks, styles){
    var enter = target_node.enter().append("g")
        .call(callbacks.drag_listener)
        .attr("id", function(node){
            return 'dom_' + node.id;
        })
        .attr("transform", function(node) {
            if (callbacks.node_type == 'standard'){
                return "translate(" + focus_node.y0 + "," + focus_node.x0 + ")";
            } else {
                return "translate(" + node.y0 + "," + node.x0 + ")";
            }
        });

    if (styles){
        enter.attr('class', styles.node_class);
    } else {
        enter.attr('class', 'node');
    }

    enter.append("circle")
        .attr('class', 'nodeCircle')
        .attr("r", 0)
        .style("fill", function(node) {
            if (tree_library.has_hidden_children(node)){
                return 'lightsteelblue';
            } else {
                return '#fff';
                }
            })
        .on('click', callbacks.child_single_click)

    enter.append("text")
        .attr('id', function(node){
            return 'name_' + node.id.toString();
        })
        .attr("x", function(node) {
            if (tree_library.has_children(node)){
                var node_type_length = node.type.length;
                return -10 + -(node_type_length*6);
            } else {
                return 10;
            }
        })
        .attr("dy", ".35em")
        .attr('class', 'node_name')
        .attr('bs-dropdown', function(node){
            if (_.indexOf(callbacks.node_types, node.type) > -1){
                return 'dropdowns.' + node.type;
            }
            return 'dropdowns.default';
        })
        .attr('aria-haspopup', 'true')
        .attr('aria-expanded', 'false')
        .attr("text-anchor", function(node) {
            if (tree_library.has_children(node)){
                return 'end';
            } else {
                return 'start';
            }
        })
        .text(function(node) {
            return node.name;
        })
        .style("fill-opacity", 0)
        .on('click', callbacks.menu_click);


    enter.append("text")
    .attr('id', function(node){
        return 'type_' + node.id.toString();
    })
        .attr("x", function(node) {
            if (tree_library.has_children(node)){
                return -10;
            } else {
                var node_name_length = node.name.length;
                return 10 + (node_name_length*6);
            }
        })
        .attr("dy", ".35em")
        .attr('class', 'node_type')
        .attr("text-anchor", function(node) {
            if (tree_library.has_children(node)){
                return 'end';
            } else {
                return 'start';
            }
        })
        .text(function(node) {
            return '(' + node.type + ')';
        })
        .style("fill-opacity", 0)
        .on('click', callbacks.pan_click);


    enter.append("circle")
        .attr('id', function(node){
            return 'move_circle_' + node.id.toString();
        })
        .attr('class', 'move_circle')
        .attr("r", 10)
        .attr('cx', 10)
        .attr("opacity", 0.3) // change this to zero to hide the target area
        .style("fill", "#4747AB")
        .attr('pointer-events', 'mouseover')
        .on("mouseover", function(node) {
            var select_circle = tree_library.get_non_empty_element(
                target_node.select('#move_circle_' + node.id.toString())[0]);
            select_circle.style.fill = '#53E709';
            drag_target = tree_library.enter_drop_zone(node);
            callbacks.drag_callback(drag_target, 'move');
        })
        .on("mouseout", function(node) {
            var select_circle = tree_library.get_non_empty_element(
                target_node.select('#move_circle_' + node.id.toString())[0]);
            select_circle.style.fill = '#4747AB';
            drag_target = tree_library.leave_drop_zone(node);
            callbacks.drag_callback(drag_target, null);
        });


    enter.append("circle")
        .attr('id', function(node){
            return 'clone_circle_' + node.id.toString();
        })
        .attr('class', 'clone_circle')
        .attr("r", 10)
        .attr('cx', -10)
        .attr("opacity", 0.3) // change this to zero to hide the target area
        .style("fill", "#FF9999")
        .attr('pointer-events', 'mouseover')
        .on("mouseover", function(node) {
            var select_circle = tree_library.get_non_empty_element(
                target_node.select('#clone_circle_' + node.id.toString())[0]);
            select_circle.style.fill = '#53E709';
            drag_target = tree_library.enter_drop_zone(node);
            callbacks.drag_callback(drag_target, 'clone');
        })
        .on("mouseout", function(node) {
            var select_circle = tree_library.get_non_empty_element(
                target_node.select('#clone_circle_' + node.id.toString())[0]);
            select_circle.style.fill = '#FF9999';
            drag_target = tree_library.leave_drop_zone(node);
            callbacks.drag_callback(drag_target, null);
        });

    return;

};


tree_library.update_node_styles = function(target_node){
    target_node.select('.node_name')
        .attr("x", function(node) {
            if (tree_library.has_children(node)){
                var node_type_length = tree_library.get_non_empty_element(
                    target_node.select('#type_' + node.id.toString())[0]).getComputedTextLength();
                return -12 + -(node_type_length);
            } else {
                return 10;
            }
        })
        .attr("text-anchor", function(node) {
            if (tree_library.has_children(node)){
                return 'end';
            } else {
                return 'start';
            }
        })
        .text(function(node) {
            return node.name;
        });

    target_node.select('.node_type')
        .attr("x", function(node) {
            if (tree_library.has_children(node)){
                return -10;
            } else {
                var node_name_length = tree_library.get_non_empty_element(
                    target_node.select('#name_' + node.id.toString())[0]).getComputedTextLength();
                return 12 + node_name_length;
            }
        })
        .attr("text-anchor", function(node) {
            if (tree_library.has_children(node)){
                return 'end';
            } else {
                return 'start';
            }
        })
        .text(function(node) {
            return '(' + node.type + ')';
        });

    target_node.select("circle.nodeCircle")
        .attr("r", 4.5)
        .style("fill", function(node) {
            if (tree_library.has_hidden_children(node)){
                return 'lightsteelblue';
            } else {
                return '#fff';
            }
        });

    return;
};


tree_library.create_node_transition = function(target_node){
    var duration = 750;
    var transition = target_node.transition()
        .duration(duration)
        .attr("transform", function(node) {
            return "translate(" + node.y + "," + node.x + ")";
        });

    transition.selectAll("text")
        .style("fill-opacity", 1);

    return;

};


tree_library.create_node_exit = function(target_node, focus_node){
    var duration = 750;
    var exit = target_node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) {
            d.y0 = focus_node.y;
            d.x0 = focus_node.x;
            return "translate(" + focus_node.y + "," + focus_node.x + ")";
        })
        .remove();

    exit.select("circle")
        .attr("r", 0);

    exit.selectAll("text")
        .style("fill-opacity", 0);

    return;
};


tree_library.set_style_node_drag = function(node){
    node.select('.move_circle').attr('pointer-events', 'none');
    node.select('.clone_circle').attr('pointer-events', 'none');
    node.attr('class', 'node activeDrag');
};


tree_library.set_style_circle_visible = function(type){
    switch (type) {
        case 'move':
            return 'move_circle show';
        case 'clone':
            return 'clone_circle show';
    }
};


tree_library.set_style_circle_invisible = function(type){
    switch (type) {
        case 'move':
            return 'move_circle';
        case 'clone':
            return 'clone_circle';
    }
};


tree_library.set_drop_targets = function(root, node_id, clone_node, callbacks){
    var dom = d3.select(node_id);
    var drag_node_dom = dom.node();
    var drag_node = tree_library.get_data_content(drag_node_dom);
    tree_library.set_style_node_drag(dom);
    d3.selectAll('.move_circle').attr('class', function(node){
        if (callbacks.evaluate_drop_target_move(root, drag_node, node)){
            return tree_library.set_style_circle_visible('move');
        } else {
            return tree_library.set_style_circle_invisible('move');
        }
    });
    d3.selectAll('.clone_circle').attr('class', function(node){
        if (callbacks.evaluate_drop_target_clone(root, drag_node, node, clone_node)){
            return tree_library.set_style_circle_visible('clone');
        } else {
            return tree_library.set_style_circle_invisible('clone');
        }
    });

};


tree_library.initiate_drag = function(group, tree, root, drag_node, clone_node, callbacks) {
    var dom_id = '#dom_'+ drag_node.id.toString();
    tree_library.set_drop_targets(root, dom_id, clone_node, callbacks);

    group.selectAll("g.node").sort(function(a, b) {
        if (a.id != drag_node.id) return 1;
        else return -1;
    });

    var nodes = tree.nodes(drag_node).reverse();

    if (nodes.length > 1) {
        var links = tree.links(nodes);

        var node_paths = group.selectAll("path.link")
            .data(links, function(link) {
                return link.target.id;
            }).remove();

        var node_exit = group.selectAll("g.node")
            .data(nodes, function(node) {
                return node.id;
            }).filter(function(node) {
                if (node.id == drag_node.id) {
                    return false;
                }
                return true;
            }).remove();
    }

    group.selectAll('path.link').filter(function(link, i) {
        if (link.target.id == drag_node.id) {
            return true;
        }
        return false;
    }).remove();
};


tree_library.visit_nodes = function(target, goals){
    if (!target){
        return;
    }
    if (Array.isArray(goals)){
        for (goal of goals){
            goal.operation(target);
        }
    } else if (goals){
        var goal = goals;
        if (goal.stop){
            return;
        }
        goal.operation(target);
    }
    var children = tree_library.get_children(target);
    if (children){
        for (child of children){
            tree_library.visit_nodes(child, goals);
        }
    }
};


tree_library.push_child = function(node, type, target){
    var shown = type;
    var hidden = '_' + type;
    if (Array.isArray(target[shown]) || Array.isArray(target[hidden])) {
        if (Array.isArray(target[shown])) {
            target[shown].push(node);
        } else {
            target[hidden].push(node);
        }
    } else {
        target[shown] = [];
        target[shown].push(node);
    }
    return target;

};


tree_library.get_parent = function(node){
    var parent = node.parent;
    return parent;
};


tree_library.push_child_switch = function(source_node, target_node){
    switch (target_node.type) {
        case 'root':
            target_node = tree_library.push_child(source_node, 'groups', target_node);
            break;
        case 'group':
            target_node = tree_library.push_child(source_node, 'structures', target_node);
            break;
        case 'structure':
            target_node = tree_library.push_child(source_node, 'templates', target_node);
            break;
        case 'template':
            target_node = tree_library.push_child(source_node, 'fields', target_node);
            break;
        case 'field':
            target_node = target_node;
            break;
    }
    return target_node;
};


tree_library.keep_clone = function(group, clone, target_node){
    target_node = tree_library.push_child_switch(clone, target_node);
    var clone_node = group.selectAll(".clone");
    clone_node.attr('class', 'node');
    tree_library.set_style_node_standard(clone_node);
    return target_node;
};


tree_library.move_node = function(node, target_node){
    var current_index = node.parent.children.indexOf(node);
    if (current_index > -1) {
        node.parent.children.splice(current_index, 1);
    }
    tree_library.push_child_switch(node, target_node);
    return target_node;
};


tree_library.get_node_clone = function(node, group){
    var node_clone = _.cloneDeep(node);
    node_clone = tree_library.assign_unique_node_id(node_clone, group);
    node_clone = tree_library.update_descendant_ids(node_clone);
    return node_clone;
};


tree_library.update_descendant_ids = function(node){
    var goal = new tree_library.update_id_goal(node.id);
    tree_library.visit_nodes(node, goal);
    return node;
}


tree_library.assign_unique_node_id = function(node, root){
    var goal = new tree_library.largest_node_id_goal();
    tree_library.visit_nodes(root, goal);
    node.id = goal.value+1;
    return node;
}


tree_library.get_dom_node_copy = function(dom_node){
    return dom_node.cloneNode(true);
};


tree_library.get_data_content = function(dom){
    try{
        return dom.__data__;
    } catch(err) {
        return null;
    }

};


tree_library.set_style_node_standard = function(node){
    node.selectAll('text').style('fill', 'black').style('fill-opacity', 1);
};


tree_library.set_style_node_clone = function(node){
    node.selectAll('text').style('fill', 'grey').style("fill-opacity", .5);
};


tree_library.set_style_link_clone = function(link){
    d3.select(link).style('fill', 'grey');
};


tree_library.make_link = function(parent, child){
    var link = {
        source: parent,
        target: child
    };
    return link;
};

tree_library.get_parent_link = function(links, child_id, clone){
    for (link of links){
        if (link.target.id == child_id){
            var new_link = _.cloneDeep(link);
            new_link.target = clone;
            return new_link;
        }
    }
};


tree_library.get_cloned_node = function(group, tree, root, dom, callbacks){
    var node = tree_library.get_data_content(dom);
    var parent = node.parent;
    var clone = tree_library.get_node_clone(node, root);
    var clones = tree.nodes(clone).reverse();
    var links = tree.links(clones);
    var parent_links = tree.links(tree.nodes(parent));
    var parent_link = tree_library.get_parent_link(parent_links, node.id, clone);

    var target_clone = group.selectAll(".clone").data(clones);
    var clone_links = group.selectAll(".clone.path.link").data(links);
    var parent_clone_link = group.selectAll(".parent.clone.path.link").data(parent_link);

    var styles = {
        node_class: 'node clone'
    };

    callbacks.node_type = 'clone';

    tree_library.create_node_enter(target_clone, target_clone, callbacks, styles);
    tree_library.update_node_styles(target_clone);
    tree_library.set_style_node_clone(target_clone);
    tree_library.create_node_exit(target_clone, target_clone);
    tree_library.create_link_enter(clone_links, null);
    tree_library.create_link_enter(parent_clone_link, null);

    callbacks.node_type = 'standard';

    return clone;
};


tree_library.remove_node = function(group, tree, root_node, drag_node, target_node, node_count){
    return;
};


tree_library.get_children = function(target){
    if (target.type) {
        switch (target.type) {
            case "root":
                if (tree_library.has_visible_children(target)){
                    return target['groups'];
                } else if (tree_library.has_hidden_children(target)) {
                    return target['_groups'];
                }
                return null;
                break;
            case "group":
                if (tree_library.has_visible_children(target)){
                    return target['structures'];
                } else if (tree_library.has_hidden_children(target)) {
                    return target['_structures'];
                }
                return null;
                break;
            case "structure":
                if (tree_library.has_visible_children(target)){
                    return target['templates'];
                } else if (tree_library.has_hidden_children(target)) {
                    return target['_templates'];
                }
                return null;
                break;
            case "template":
                if (tree_library.has_visible_children(target)){
                    return target['fields'];
                } else if (tree_library.has_hidden_children(target)) {
                    return target['_fields'];
                }
                return null;
                break;
            default:
                return null;
                break;
        }
    }
    else {
        return null;
    }
};

tree_library.setup = function(json){
    var setup_dictionary = {};
    var longest_label = new tree_library.longest_label_goal(0);
    var total_nodes = new tree_library.node_adder_goal(0);
    goals = [longest_label, total_nodes];
    tree_library.visit_nodes(json, goals);
    for (goal of goals){
        setup_dictionary[goal.name] = goal.value;
    }
    return setup_dictionary;
};


tree_library.assign_parents = function(json){
    var goal = new tree_library.assign_parent_goal();
    tree_library.visit_nodes(json, goal);
    return json;
};


tree_library.update_id_goal = function(initial_id){
    this.name = 'update_id_goal';
    this.description = 'Updates the id of the passed target and increments a counter.';
    this.value = initial_id;
    this.stop = false;
    this.operation = function(target){
        if (target.id && target.id != this.value) {
            this.value = this.value + 1;
            target.id = this.value;
        }
        return;
    };
};


tree_library.get_node_array_goal = function(){
    this.name = 'get_node_array_goal';
    this.description = 'Walks the tree, grabbing all the nodes and pushing them to an array.';
    this.value = [];
    this.stop = false;
    this.operation = function(target){
        this.value.push(target);
        return;
    };
}


tree_library.largest_node_id_goal = function(){
    this.name = 'largest_node_id_goal';
    this.description = 'Compares two node ids, returning the larger of the id.';
    this.value = 0;
    this.stop = false;
    this.operation = function(target){
        if (target.id) {
            this.value = Math.max(target.id, this.value);
        }
        return;
    };
};


tree_library.assign_parent_goal = function(){
    this.name = 'assign_parent_goal';
    this.description = 'Assigns the id of the targets parent to the target as a parent property.';
    this.value = 0;
    this.stop = false;
    this.operation = function(target){
        target.parent_id = target.parent.id;
        return;
    };
};


tree_library.longest_label_goal = function(minimum_label_length){
    this.name = 'longest_label_goal';
    this.description = 'Compares two label lengths, returning the longer value.';
    this.value = minimum_label_length;
    this.stop = false;
    this.operation = function(target){
        var test_value = 0;
        if (target.type) {
            switch (target.type) {
                case "group":
                    var type_string = '(group)';
                    test_value = target.name.length + type_string.length;
                    break;
                case "structure":
                case "template":
                default:
                    test_value = target.name.length + target.type.length + 2;
                    break;
            }
        }
        this.value = Math.max(test_value, this.value);
        return;
    };
};


tree_library.node_adder_goal = function(initial_count) {
    this.name = 'node_adder_goal';
    this.description = 'Increments a node counter if the node is an acceptable node type.';
    this.value = initial_count;
    this.stop = false;
    this.operation = function(target){
        var increment = false;
        if (target.type) {
            switch (target.type) {
                case "group":
                case "structure":
                case "template":
                default:
                    increment = true;
                    break;
            }
        }
        if (increment){
            this.value++;
        }
        return;
    };

};
