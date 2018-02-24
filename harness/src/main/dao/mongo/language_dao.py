from python_commons import db_utils


def get_language_collection(project):
    """Connects to the specified project and returns a pointer
    to the functions collection.
    """
    connection = db_utils.mongo_get_connection(project)
    collection = db_utils.mongo_get_collection(connection, 'language')
    return collection


def serialize_functions(project, functions):
    """Adds  multiple functions to the language collection and
    returns a list of function objects.
    """
    collection = get_language_collection(project)
    results = db_utils.mongo_insert_many(collection, functions)
    return results


def serialize_function(project, function):
    """Adds a single function to the language collection and returns the complete
    function object.
    """
    collection = get_language_collection(project)
    result = db_utils.mongo_insert_one(collection, function)
    return get_function_by_id(project, result)


def remove_language_collection(project):
    """Completely blows away the language collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_language_collection(project)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_all_current_functions(project):
    """Returns all functions that are current (no removal date) in the current
    project.
    """
    collection = get_language_collection(project)
    argument = db_utils.make_single_field_argument('remove_date', None)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_all_functions(project, current_only=False):
    """ Returns all functions as a list of function dictionary objects.
    Optionally can specify current_only to retrieve only the most current record
    for each function.
    """
    collection = get_language_collection(project)
    cursor = db_utils.mongo_find_records(collection, named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_removed_functions(project):
    """Returns parameter sets that have been removed from the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_language_collection(project)
    argument = db_utils.make_single_field_argument('status', 'removed')
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_function_by_id(project, function_id):
    """Returns the function by the given id.
    """
    collection = get_language_collection(project)
    argument = db_utils.make_single_field_argument('_id', function_id)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    function_list = db_utils.unload_cursor(cursor)
    try:
        return function_list[0]
    except IndexError:
        return None


def update_function(project, function, changes):
    """Updates the given parameter set by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_language_collection(project)
    function_id = function['_id']
    argument = db_utils.make_single_field_argument('_id', function_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'workflow'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(db_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(db_utils.make_update_argument(change, function[change]))
    update = db_utils.merge_update_args(updates)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_function_by_id(project, function_id)
    return None


if __name__ == '__main__':
    print("Please use language dao module as method package.")
