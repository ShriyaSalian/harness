from pythoncommons import mongo_utils


def get_group_collection(database):
    """Connects to the project database and returns a pointer to the group collection.
    """
    connection = mongo_utils.mongo_get_connection(database)
    collection = mongo_utils.mongo_get_collection(connection, "mars_groups")
    return collection


def remove_group_collection(database):
    """Completely blows away the group collection. Returns the status of effort.
    Caveat emptor.
    """
    collection = get_group_collection(database)
    status = mongo_utils.mongo_remove_collection(collection)
    return status


def create_group_collection(database, groups=None):
    """Inserts all the given groups into the groups collection.
    Returns the status of effort.
    """
    collection = get_group_collection(database)
    status = False
    if groups:
        if type(groups) is dict:
            status = mongo_utils.mongo_insert_one(collection, groups)
        else:
            if len(groups) == 1:
                status = mongo_utils.mongo_insert_one(collection, groups[0])
            else:
                status = mongo_utils.mongo_insert_many(collection, groups)
    return status


def add_group(database, group):
    """Adds a single group to the component collection and returns the complete
    group object.
    """
    collection = get_group_collection(database)
    result = mongo_utils.mongo_insert_one(collection, group)
    result_id = result.inserted_id
    return get_group_by_id(database, result_id)


def get_all_current_groups(database):
    """Returns all groups that are current (no removal date) in the current
    database.
    """
    collection = get_group_collection(database)
    argument = mongo_utils.make_single_field_argument('remove_date', None)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    return mongo_utils.unload_cursor(cursor)


def get_group_by_id(database, group_id):
    """Returns the group by the given id.
    """
    collection = get_group_collection(database)
    argument = mongo_utils.make_single_field_argument('_id', group_id)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument)
    group_list = mongo_utils.unload_cursor(cursor)
    try:
        return group_list[0]
    except IndexError:
        return None
