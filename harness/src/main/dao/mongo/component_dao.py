from pythoncommons import mongo_utils, general_utils


def get_component_collection(database):
    """Connects to the specified database and returns a pointer
    to the components collection.
    """
    connection = mongo_utils.mongo_get_connection(database)
    collection = mongo_utils.mongo_get_collection(connection, 'components')
    return collection


def create_component_collection(database, components=None):
    """Inserts all the given components into the components collection.
    Returns the status of effort.
    """
    collection = get_component_collection(database)
    status = False
    if components:
        if type(components) is dict:
            status = mongo_utils.mongo_insert_one(collection, components)
        else:
            if len(components) == 1:
                status = mongo_utils.mongo_insert_one(collection, components[0])
            else:
                status = mongo_utils.mongo_insert_many(collection, components)
    return status


def add_component(database, component):
    """Adds a single component to the component collection and returns the complete
    component object.
    """
    collection = get_component_collection(database)
    result = mongo_utils.mongo_insert_one(collection, component)
    result_id = result.inserted_id
    return get_component_by_id(database, result_id)


def remove_component_collection(database):
    """Completely blows away the component collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_component_collection(database)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_all_current_components(database):
    """Returns all components that are current (no removal date) in the current
    database.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('remove_date', None)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_all_components(database, current_only=False):
    """ Returns all components as a list of component dictionary objects.
    Optionally can specify current_only to retrieve only the most current record
    for each component.
    """
    collection = get_component_collection(database)
    cursor = mongo_utils.mongo_find_records(collection, named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_enabled_components(database, current_only=True):
    """Returns the enabled components for the specified database.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_component_collection(database)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('status', 'enabled'))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    return component_list


def get_disabled_components(database, current_only=True):
    """Returns the disabled components for the specified database.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_component_collection(database)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('status', 'disabled'))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    return component_list


def get_vcs_enabled_components(database, current_only=True):
    """Returns components with their vcs enabled (turned on) for the specified
    database.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_component_collection(database)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('vcs.status', 'enabled'))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    return component_list


def get_vcs_disabled_components(database, current_only=True):
    """Returns components with their vcs disabled (turned off) for the specified
    database.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_component_collection(database)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('vcs.status', 'disabled'))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    return component_list


def get_removed_components(database):
    """Returns components that have been removed from the specified database.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('status', 'removed')
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_component_by_id(database, component_id):
    """Returns the component by the given id.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    try:
        return component_list[0]
    except IndexError:
        return None


def get_components_by_name(database, name):
    """ Returns all the components by name, if it exists, otherwise returns False
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('name', name)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_current_component_by_name(database, name):
    """Returns the current component by name.
    """
    collection = get_component_collection(database)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = general_utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    component_list = mongo_utils.unload_cursor(cursor)
    try:
        return component_list[0]
    except IndexError:
        return None


def replace_component_by_id(database, component_id, component):
    """Replaces the current component with the new component. Returns the new component.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    cursor = mongo_utils.mongo_replace_one(collection, component, argument)
    if cursor.matched_count == 1:
        cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                             named_tuple=False)
        component_list = mongo_utils.unload_cursor(cursor)
        try:
            return component_list[0]
        except IndexError:
            return None


def update_component_status_by_id(database, component_id, status):
    """Updates the status of the component with the given id to the given status.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    update = mongo_utils.make_update_argument('status', status)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


def update_component_functions_by_id(database, component_id, functions):
    """Updates the status of the component with the given id to the given status.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    update = mongo_utils.make_update_argument('functions', functions)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    updated_component = None
    if cursor.modified_count == 1:
        updated_component = get_component_by_id(database, component_id)
    return updated_component


def remove_component_by_id(database, component_id, timestamp):
    """Updates the component with the given id to have a removal datetime of the given
    datetime and sets the component status to removed.
    """
    update_component_status_by_id(database, component_id, 'removed')
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    update = mongo_utils.make_update_argument('remove_date', timestamp)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


def update_component_vcs_status_by_id(database, component_id, status):
    """Updates the vcs status of the given component with the specified status.
    """
    collection = get_component_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', component_id)
    update = mongo_utils.make_update_argument('vcs.status', status)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


if __name__ == '__main__':
    print("Please use as method package.")
