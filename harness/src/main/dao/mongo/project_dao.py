from python_commons import db_utils
from collections import OrderedDict


def get_project_collection(database="project"):
    """Connects to the project admin database (defaults to project) and returns a pointer
    to the project collection.
    """
    connection = db_utils.mongo_get_connection(database)
    collection = db_utils.mongo_get_collection(connection, "project")
    return collection


def remove_project_collection():
    """Completely blows away the project collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_project_collection()
    status = db_utils.mongo_remove_collection(collection)
    return status


def remove_project_record_by_id(project_id):
    """Removes a single record from the project database with the specified project id.
    """
    collection = get_project_collection()
    argument = db_utils.make_single_field_argument("_id", project_id)
    removal = db_utils.mongo_remove_one(collection, argument)
    return removal


def remove_project_record_by_name(project_name):
    """Removes a single record from the project database with the specified project name.
    """
    collection = get_project_collection()
    argument = db_utils.make_single_field_argument("name", project_name)
    removal = db_utils.mongo_remove_one(collection, argument)
    return removal


def remove_project_database(database_name):
    """Completely removes the project storage database with the given name.
    """
    removal_result = db_utils.mongo_remove_database(database_name)
    return removal_result


def get_all_projects():
    """Returns all the project objects as a list as they currently exist in the
    program storage.
    """
    collection = get_project_collection()
    cursor = db_utils.mongo_find_records(collection, named_tuple=False)
    return db_utils.unload_cursor(cursor)


def get_project_by_id(project_id):
    """Returns the project object with the matching passed project_id.
    """
    collection = get_project_collection()
    argument = db_utils.make_single_field_argument("_id", project_id)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    project_list = db_utils.unload_cursor(cursor)
    try:
        return project_list[0]
    except:
        return None


def get_project_by_name(project_name):
    """Returns the project object with the matching passed name.
    """
    collection = get_project_collection()
    argument = db_utils.make_single_field_argument("name", project_name)
    cursor = db_utils.mongo_find_records(collection, argument=argument,
                                         named_tuple=False)
    project_list = db_utils.unload_cursor(cursor)
    try:
        return project_list[0]
    except:
        return None


def validate_project_name(project_name):
    """Returns True if the name is not yet used as a project or returns False
    if the project is already in use.
    """
    existing_record = get_project_by_name(project_name)
    if existing_record:
        return False
    return True


def validate_project_database(database_name):
    """Creates a new database to hold data (components, evaluations, comparisons,
    parameters, etc) relating to a specified project. If the method succeeds, returns
    the name of the newly created database. Otherwise, returns false.
    """
    connection = db_utils.mongo_get_connection(database_name)
    if connection:
        collections = connection.collection_names()
        if not collections:
            return database_name
    return False


def replace_project_by_id(project_id, project):
    """Replaces a project matching the given id with the new project object.
    Returns the new project object.
    """
    collection = get_project_collection()
    argument = db_utils.make_single_field_argument("_id", project_id)
    cursor = db_utils.mongo_replace_one(collection, project, argument)
    if cursor.matched_count == 1:
        cursor = db_utils.mongo_find_records(collection, argument=argument,
                                             named_tuple=False)
        project_list = db_utils.unload_cursor(cursor)
        try:
            return project_list[0]
        except:
            return None
    return None


def create_new_project(project=None):
    """Attempts to create a new project from the passed dictionary project object.
    If it is successful, returns the new project object. If it fails, returns None.
    """
    collection = get_project_collection()
    if type(project) in [dict, OrderedDict]:
        result = db_utils.mongo_insert_one(collection, project)
        return result
    else:
        if len(project) == 1:
            result = db_utils.mongo_insert_one(collection, project[0])
            return result
        else:
            result = db_utils.mongo_insert_many(collection, project)
            return result
    return None


if __name__ == '__main__':
    print("Project dao module. Please use as method package.")
