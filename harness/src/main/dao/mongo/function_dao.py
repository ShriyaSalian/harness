from pythoncommons import mongo_utils, utils


def get_function_collection(project):
    """Connects to the specified project and returns a pointer
    to the functions collection.
    """
    connection = mongo_utils.mongo_get_connection(project)
    collection = mongo_utils.mongo_get_collection(connection, 'functions')
    return collection


def create_function_collection(project, functions=None):
    """Inserts all the given functions into the functions collection.
    Returns the status of effort.
    """
    collection = get_function_collection(project)
    status = False
    if functions:
        if type(functions) is dict:
            status = mongo_utils.mongo_insert_one(collection, functions)
        else:
            if len(functions) == 1:
                status = mongo_utils.mongo_insert_one(collection, functions[0])
            else:
                status = mongo_utils.mongo_insert_many(collection, functions)
    return status


def add_functions(project, functions):
    """Adds  multiple functions to the function collection and returns the complete
    function object.
    """
    collection = get_function_collection(project)
    results = mongo_utils.mongo_insert_many(collection, functions)
    return results


def add_function(project, function):
    """Adds a single function to the function collection and returns the complete
    function object.
    """
    collection = get_function_collection(project)
    result = mongo_utils.mongo_insert_one(collection, function)
    result_id = result.inserted_id
    return get_function_by_id(project, result_id)


def remove_function_collection(project):
    """Completely blows away the function collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_function_collection(project)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_all_current_functions(project):
    """Returns all functions that are current (no removal date) in the current
    project.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('remove_date', None)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_functions_for_component(project, component, current=True):
    """Returns  functions for the given component for the given project.
    Optional parameter allows user to return current or all functions.
    """
    collection = get_function_collection(project)
    arguments = []
    if current:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('component', component))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    return function_list


def get_all_functions(project, current_only=False):
    """ Returns all functions as a list of function dictionary objects.
    Optionally can specify current_only to retrieve only the most current record
    for each function.
    """
    collection = get_function_collection(project)
    cursor = mongo_utils.mongo_find_records(collection, named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_enabled_functions(project, current_only=True):
    """Returns the enabled functions for the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_function_collection(project)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('status', 'enabled'))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    return function_list


def get_disabled_functions(project, current_only=True):
    """Returns the disabled functions for the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_function_collection(project)
    arguments = []
    if current_only:
        arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    arguments.append(mongo_utils.make_single_field_argument('status', 'disabled'))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    return function_list


def get_removed_functions(project):
    """Returns functions that have been removed from the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('status', 'removed')
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_function_by_id(project, function_id):
    """Returns the function by the given id.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    try:
        return function_list[0]
    except IndexError:
        return None


def get_functions_by_name(project, name):
    """ Returns all the functions by name, if it exists, otherwise returns False
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('name', name)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_current_function_by_name(project, name):
    """Returns the current function by name.
    """
    collection = get_function_collection(project)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    try:
        return function_list[0]
    except IndexError:
        return None


def replace_function_by_id(project, function_id, function):
    """Replaces the current function with the new function. Returns the new function.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    cursor = mongo_utils.mongo_replace_one(collection, function, argument)
    if cursor.matched_count == 1:
        cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                             named_tuple=False)
        function_list = mongo_utils.unload_cursor(cursor)
        try:
            return function_list[0]
        except IndexError:
            return None


def update_function_status_by_id(project, function_id, status):
    """Updates the status of the function with the given id to the given status.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    update = mongo_utils.make_update_argument('status', status)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


def remove_function_by_id(project, function_id, timestamp):
    """Updates the function with the given id to have a removal datetime of the given
    datetime and sets the function status to removed.
    """
    update_function_status_by_id(project, function_id, 'removed')
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    update = mongo_utils.make_update_argument('remove_date', timestamp)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


def update_function_vcs_status_by_id(project, function_id, status):
    """Updates the vcs status of the given function with the specified status.
    """
    collection = get_function_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    update = mongo_utils.make_update_argument('vcs.status', status)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


if __name__ == '__main__':
    print("Please use function dao module as method package.")
