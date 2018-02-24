import harness.src.main.processor.parameter_processor as parameter_processor


def get_groups(database):
    """Returns all parameter groups for the specified databse.
    """
    parameter_groups = parameter_processor.get_current_parameter_groups(database)
    return parameter_groups


def get_all_parameters(database):
    """
    """
    parameter_tree = parameter_processor.get_parameter_tree(database)
    return parameter_tree


def modify_parameters(database, updates):
    """Modifies parameters using a router.
    """
    router = modification_closure(database)
    update_result = list(map(router, updates))
    return update_result


def modification_closure(database):
    """ Closure method for the parameter update router.
    """

    def modification_router(update):
        """Returns the correct router based on the update action key.
        """
        if update['action'] == 'update':
            return parameter_update_router(update)
        elif update['action'] == 'add':
            return parameter_add_router(update)
        elif update['action'] == 'remove':
            return parameter_remove_router(update)
        elif update['action'] == 'move':
            return parameter_move_router(update)

    def parameter_update_router(update):
        """Routes the given parameter update to the proper processor method.
        Returns the updated object.
        """
        update['update']['_id'] = update['_id']
        if update['type'] == 'group':
            return parameter_processor.update_group(database, update['update'], update['changes'])
        elif update['type'] == 'structure':
            return parameter_processor.update_structure(database, update['update'], update['changes'])
        elif update['type'] == 'template':
            return parameter_processor.update_template(database, update['update'], update['changes'])

    def parameter_add_router(add):
        """Routes the given parameter add to the proper processor method.
        Returns the newly added object.
        """
        order = None
        if 'order' in list(add.keys()):
            order = int(add['order'])
        if add['type'] == 'group':
            return parameter_processor.add_group(database, add['update'], add['parent'], order=order)
        elif add['type'] == 'structure':
            return parameter_processor.add_structure(database, add['update'], add['parent'], order=order)
        elif add['type'] == 'template':
            return parameter_processor.add_template(database, add['update'], add['parent'], order=order)

    def parameter_remove_router(remove):
        """Routes the given parameter remove to the proper processor method.
        Returns the updated parent object.
        """
        remove['update'] = {}
        remove['update']['_id'] = remove['_id']
        if remove['type'] == 'group':
            return parameter_processor.remove_group(database, remove['update'])
        elif remove['type'] == 'structure':
            return parameter_processor.remove_structure(database, remove['update'], remove['parent'])
        elif remove['type'] == 'template':
            return parameter_processor.remove_template(database, remove['update'], remove['parent'])

    def parameter_move_router(move):
        move['update'] = {}
        move['update']['_id'] = move['_id']
        move['update']['old_parent'] = move['old_parent']
        move['update']['old_name'] = move['old_name']
        move['update']['new_parent'] = move['new_parent']
        move['update']['new_name'] = move['new_name']
        if move['type'] == 'structure':
            return parameter_processor.move_structure(database, move['update'])
        elif move['type'] == 'template':
            return parameter_processor.move_template(database, move['update'])

    return modification_router


if __name__ == '__main__':
    print('Please use parameter router module as method package.')
