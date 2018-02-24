from pythoncommons import db_utils, utils


def get_workflow_collection(project):
    """Connects to the specified project and returns a pointer
    to the workflows collection.
    """
    connection = db_utils.mongo_get_connection(project)
    collection = db_utils.mongo_get_collection(connection, 'workflows')
    return collection


def create_workflow_collection(project, workflows=None):
    """Inserts all the given workflows into the workflows collection.
    Will automatically create the stations collection if it does not exist.
    Returns the status of effort.
    """
    collection = get_workflow_collection(project)
    status = False
    if workflows:
        if type(workflows) is dict:
            status = db_utils.mongo_insert_one(collection, workflows)
        else:
            if len(workflows) == 1:
                status = db_utils.mongo_insert_one(collection, workflows[0])
            else:
                status = db_utils.mongo_insert_many(collection, workflows)
    return status


def add_workflows(project, workflows):
    """Adds  multiple workflows to the workflow collection and returns the complete
    workflow object.
    """
    collection = get_workflow_collection(project)
    results = db_utils.mongo_insert_many(collection, workflows)
    return results


def add_workflow(project, workflow):
    """Adds a single workflow to the workflow collection and returns the complete
    workflow object.
    """
    collection = get_workflow_collection(project)
    result = db_utils.mongo_insert_one(collection, workflow)
    return get_workflow_by_id(project, result)


def remove_workflow_collection(project):
    """Completely blows away the workflow collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_workflow_collection(project)
    status = db_utils.mongo_remove_collection(collection)
    return status


def get_all_current_workflows(project):
    """Returns all workflows that are current (no removal date) in the current
    project.
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('remove_date', None)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_all_workflows(project, current_only=False):
    """ Returns all workflows as a list of workflow dictionary objects.
    Optionally can specify current_only to retrieve only the most current record
    for each workflow.
    """
    collection = get_workflow_collection(project)
    cursor = db_utils.mongo_find_records(collection, named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_removed_workflows(project):
    """Returns workflows that have been removed from the specified project.
    Optionally can return all records (including older) if current_only is set to False.
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('status', 'removed')
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_workflow_by_id(project, workflow_id):
    """Returns the workflow by the given id.
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('_id', workflow_id)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    workflow_list = db_utils.unload_cursor(cursor)
    try:
        return workflow_list[0]
    except IndexError:
        return None


def get_workflows_by_name(project, name):
    """ Returns all the workflows by name, if it exists, otherwise returns False
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('name', name)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_current_workflow_by_name(project, name):
    """Returns the current workflow by name.
    """
    collection = get_workflow_collection(project)
    arguments = []
    arguments.append(db_utils.make_single_field_argument('name', name))
    arguments.append(db_utils.make_single_field_argument('remove_date', None))
    argument = utils.merge_list_of_dicts(arguments)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    workflow_list = db_utils.unload_cursor(cursor)
    try:
        return workflow_list[0]
    except IndexError:
        return None


def replace_workflow_by_id(project, workflow_id, workflow):
    """Replaces the current workflow with the new workflow. Returns the new workflow.
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('_id', workflow_id)
    cursor = db_utils.mongo_replace_one(collection, workflow, argument)
    if cursor.matched_count == 1:
        cursor = db_utils.mongo_find_records(collection, argument=argument,
                                             named_tuple=False)
        workflow_list = db_utils.unload_cursor(cursor)
        try:
            return workflow_list[0]
        except IndexError:
            return None


def update_workflow(project, workflow, changes):
    """Updates the given workflow by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_workflow_collection(project)
    workflow_id = workflow['_id']
    argument = db_utils.make_single_field_argument('_id', workflow_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'workflow'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(db_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(db_utils.make_update_argument(change, workflow[change]))
    update = db_utils.merge_update_args(updates)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_workflow_by_id(project, workflow_id)
    return None


def update_workflow_status_by_id(project, workflow_id, status):
    """Updates the status of the workflow with the given id to the given status.
    """
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('_id', workflow_id)
    update = db_utils.make_update_argument('status', status)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    return cursor


def remove_workflow_by_id(project, workflow_id, timestamp):
    """Updates the workflow with the given id to have a removal datetime of the given
    datetime and sets the workflow status to removed.
    """
    update_workflow_status_by_id(project, workflow_id, 'removed')
    collection = get_workflow_collection(project)
    argument = db_utils.make_single_field_argument('_id', workflow_id)
    update = db_utils.make_update_argument('remove_date', timestamp)
    cursor = db_utils.mongo_update_one(collection, argument, update)
    return cursor


if __name__ == '__main__':
    print("Please use workflow dao module as method package.")
