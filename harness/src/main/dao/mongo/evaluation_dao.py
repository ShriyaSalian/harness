from pythoncommons import mongo_utils, utils


def get_evaluation_collection(project):
    """Connects to the specified project and returns a pointer
    to the evaluations collection.
    """
    connection = mongo_utils.mongo_get_connection(project)
    collection = mongo_utils.mongo_get_collection(connection, 'evaluations')
    return collection


def create_evaluation_collection(project, evaluations=None):
    """Inserts all the given evaluations into the evaluations collection.
    Will automatically create the stations collection if it does not exist.
    Returns the status of effort.
    """
    collection = get_evaluation_collection(project)
    status = False
    if evaluations:
        if type(evaluations) is dict:
            status = mongo_utils.mongo_insert_one(collection, evaluations)
        else:
            if len(evaluations) == 1:
                status = mongo_utils.mongo_insert_one(collection, evaluations[0])
            else:
                status = mongo_utils.mongo_insert_many(collection, evaluations)
    return status


def add_evaluations(project, evaluations):
    """Adds  multiple evaluations to the evaluation collection and returns the complete
    evaluation object.
    """
    collection = get_evaluation_collection(project)
    results = mongo_utils.mongo_insert_many(collection, evaluations)
    return results


def add_evaluation(project, evaluation):
    """Adds a single evaluation to the evaluation collection and returns the complete
    evaluation object.
    """
    collection = get_evaluation_collection(project)
    result = mongo_utils.mongo_insert_one(collection, evaluation)
    return get_evaluation_by_id(project, result)


def remove_evaluation_collection(project):
    """Completely blows away the evaluation collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_evaluation_collection(project)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def get_all_current_evaluations(project):
    """Returns all evaluations that are current (no removal date) in the current
    project.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('remove_date', None)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_all_evaluations(project, current_only=False):
    """ Returns all evaluations as a list of evaluation dictionary objects.
    Optionally can specify current_only to retrieve only the most current record
    for each evaluation.
    """
    collection = get_evaluation_collection(project)
    cursor = mongo_utils.mongo_find_records(collection, named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_removed_evaluations(project):
    """Returns evaluations that have been removed from the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('status', 'removed')
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_evaluation_by_id(project, evaluation_id):
    """Returns the evaluation by the given id.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', evaluation_id)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    evaluation_list = mongo_utils.unload_cursor(cursor)
    try:
        return evaluation_list[0]
    except IndexError:
        return None


def get_evaluations_by_workflow(project, workflow):
    """Returns all evaluations for the given workflow.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('workflow', workflow)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    evaluation_list = mongo_utils.unload_cursor(cursor)
    try:
        return evaluation_list
    except IndexError:
        return None


def get_workflow_evaluations_by_name(project, workflow, name):
    """Returns all evaluations in the given workflow with the given name.
    """
    collection = get_evaluation_collection(project)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('workflow', workflow))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    evaluation_list = mongo_utils.unload_cursor(cursor)
    try:
        return evaluation_list
    except IndexError:
        return None


def get_evaluations_by_name(project, name):
    """ Returns all the evaluations by name, if it exists, otherwise returns False
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('name', name)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return mongo_utils.unload_cursor(cursor)


def get_current_evaluation_by_name(project, name):
    """Returns the current evaluation by name.
    """
    collection = get_evaluation_collection(project)
    arguments = []
    arguments.append(mongo_utils.make_single_field_argument('name', name))
    arguments.append(mongo_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    evaluation_list = mongo_utils.unload_cursor(cursor)
    try:
        return evaluation_list[0]
    except IndexError:
        return None


def replace_evaluation_by_id(project, evaluation_id, evaluation):
    """Replaces the current evaluation with the new evaluation. Returns the new evaluation.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', evaluation_id)
    cursor = mongo_utils.mongo_replace_one(collection, evaluation, argument)
    if cursor.matched_count == 1:
        cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                             named_tuple=False)
        evaluation_list = mongo_utils.unload_cursor(cursor)
        try:
            return evaluation_list[0]
        except IndexError:
            return None


def update_evaluation(project, evaluation, changes):
    """Updates the given evaluation by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_evaluation_collection(project)
    evaluation_id = evaluation['_id']
    argument = mongo_utils.make_single_field_argument('_id', evaluation_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'evaluation'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(mongo_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(mongo_utils.make_update_argument(change, evaluation[change]))
    update = mongo_utils.merge_update_args(updates)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_evaluation_by_id(project, evaluation_id)
    return None


def update_evaluation_status_by_id(project, evaluation_id, status):
    """Updates the status of the evaluation with the given id to the given status.
    """
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', evaluation_id)
    update = mongo_utils.make_update_argument('status', status)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


def remove_evaluation_by_id(project, evaluation_id, timestamp):
    """Updates the evaluation with the given id to have a removal datetime of the given
    datetime and sets the evaluation status to removed.
    """
    update_evaluation_status_by_id(project, evaluation_id, 'removed')
    collection = get_evaluation_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', evaluation_id)
    update = mongo_utils.make_update_argument('remove_date', timestamp)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    return cursor


if __name__ == '__main__':
    print("Please use evaluation dao module as method package.")
