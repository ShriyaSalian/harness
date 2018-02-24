import harness.src.main.dao.filesystem.filesystem_dao as file_dao
import harness.src.main.dao.mongo.component_dao as mongo_dao
import harness.src.main.model.component_model as component_model
import harness.src.main.processor.function_processor as function_processor
from pythoncommons import utils
from collections import OrderedDict
from . import generic_processor


def enable_components(database, components, parameter='id'):
    """The plural method of enable component. Will enable every component that
    is passed in the components list for the given database.
    """
    component_enabler = enable_component_closure(database, parameter=parameter)
    enabled_components = list(map(component_enabler, components))
    return enabled_components


def enable_component_closure(database, parameter='id'):
    """Enables a component for a specified project by creating a new component
    record based on the previous record in the collection. Updates the local storage
    from the repository.
    """

    def enable_component(component):
        """Enables a component for a specified project by creating a new component
        record based on the previous record in the collection. Updates the local storage
        from the repository.
        """
        try:
            component_id = component['_id']
            component = enable_component_by_id(component_id)
        except KeyError:
            return component
        return component

    def enable_component_by_id(component_id):
        """Uses the given id to enable the component. Returns the new component.
        """
        status = 'enabled'
        component = mongo_dao.update_component_status_by_id(database, component_id,
                                                            status)
        return component

    def enable_component_by_name(component_name):
        """Uses the given name to enable the component. Returns the new component.
        """
        status = 'enabled'
        component = mongo_dao.get_current_component_by_name(database, component_name)
        component_id = component['_id']
        component = mongo_dao.update_component_status_by_id(database, component_id,
                                                            status)
        return component

    if parameter == 'id':
        return enable_component_by_id
    elif parameter == 'name':
        return enable_component_by_name
    return enable_component


def remove_components(database, components, parameter='id', remove_storage=True):
    """The plural method for remove_component. Will remove every component that is
    passed in the components list for the given database.
    """
    component_remover = remove_component_closure(database, parameter=parameter,
                                                 remove_storage=remove_storage)
    removed_components = list(map(component_remover, components))
    return removed_components


def remove_component_closure(database, parameter='id', remove_storage=True):
    """Removes a specified component for the specified project by setting the removal date
     and removing the local storage for the component. Returns True if successful.
    """

    def remove_component(component):
        """Removes a specified component for the specified project by setting the removal date
         and removing the local storage for the component. Returns True if successful.
        """
        try:
            component_id = component['_id']
            component = remove_component_by_id(component_id)
        except KeyError:
            return component
        return component

    def remove_component_by_id(component_id):
        """Uses the given id to remove the component. Returns the removed component.
        """
        timestamp = utils.get_timestamp()
        component = mongo_dao.remove_component_by_id(database, component_id, timestamp)
        if remove_storage:
            storage_location = component['location']
            remove_component_storage(storage_location)
        return component

    def remove_component_by_name(component_name):
        """Uses the given name to remove the component. Returns the removed component.
        """
        timestamp = utils.get_timestamp()
        component = mongo_dao.get_current_component_by_name(database, component_name)
        component_id = component['_id']
        component = mongo_dao.remove_component_by_id(database, component_id, timestamp)
        if remove_storage:
            storage_location = component['location']
            remove_component_storage(storage_location)
        return component

    if parameter == 'id':
        return remove_component_by_id
    elif parameter == 'name':
        return remove_component_by_name
    return remove_component


def remove_component_storage(storage_location):
    """Removes the component storage at the specified directory. Returns True if
    the method succeeds.
    """
    file_dao.remove_directory(storage_location)


def add_components_to_project(project, components, parameter=None, add_local_storage=True):
    """The plural method for add_component. Adds all the components in the passed
    components list. Optionally allows for not loading local content if desired.
    """
    component_adder = add_component_closure(project, parameter=None,
                                            add_local_storage=add_local_storage)
    added_components = list(map(component_adder, components))
    return added_components


def add_component_closure(project, parameter=None, add_local_storage=True):
    """Adds a single component to the component collection.
    If parameter is specified (id) then the component is added by that parameter.
    Optionally adds component storage locally if specified (defaults to True).
    Returns the inserted component object.
    """

    def add_component(component):
        """Adds a single component to the component collection.
        Optionally adds component storage locally if specified (defaults to True).
        Returns the inserted component object.
        """
        try:
            component = add_component_location(component)
            database = project['database']
            if add_local_storage:
                component = checkout_and_add_local_component_files(component)
            component = mongo_dao.add_component(database, component)
        except:
            return None
        return component

    def add_component_by_id(component_id):
        """Adds a component by first retrieving the component with the given id.
        Optionally adds component storage locally if specified (defaults to True).
        Returns the newly added component.
        """
        try:
            database = project['database']
            component = mongo_dao.get_component_by_id(database, component_id)
            component = component_model.update_component_location(component, project)
            component = component_model.remove_database_artifacts(component)
            component = component_model.reset_component_dates(component)
            component = component_model.update_component_status(component)
            if add_local_storage:
                component = checkout_and_add_local_component_files(component)
            component = mongo_dao.add_component(database, component)
        except:
            return None
        return component

    def add_component_location(component):
        component = component_model.update_component_location(component, project)
        return component

    def checkout_and_add_local_component_files(component):
        """Adds local storage for the given component.
        """
        storage_exists = check_component_storage(component)
        if storage_exists:
            remove_component_storage(component['location'])
        new_vcs = clone_component_from_repository(component)
        vcs_adder = component_model.add_vcs_to_component_closure([new_vcs])
        component = vcs_adder(component)
        return component

    if parameter == 'id':
        return add_component_by_id
    return add_component


def disable_components(database, components, parameter='id'):
    """The plural method of deactivate_component. Will disable every component
    that is passed in the components list for the given database.
    """
    component_disabler = disable_component_closure(database, parameter=parameter)
    disabled_components = list(map(component_disabler, components))
    return disabled_components


def disable_component_closure(database, parameter='id'):
    """Disables a component for a specified project database by adding a removal
    date to the component record. Does not remove local storage. Returns the updated
    component record. This is the functional for the function.
    """

    def disable_component(component):
        """Disables a component for a specified project database by adding a removal
        date to the component record. Does not remove local storage. Returns the updated
        component record.
        """
        try:
            component_id = component['_id']
            component = disable_component_by_id(component_id)
        except KeyError:
            return component
        return component

    def disable_component_by_id(component_id):
        """Uses the given id to disable the component. Returns the new component.
        """
        status = 'disabled'
        component = mongo_dao.update_component_status_by_id(database, component_id,
                                                            status)
        return component

    def disable_component_by_name(component_name):
        """Uses the given name to disable the component. Returns the new component.
        """
        component = mongo_dao.get_current_component_by_name(database, component_name)
        component = disable_component(component)
        return component

    if parameter == 'id':
        return disable_component_by_id
    elif parameter == 'name':
        return disable_component_by_name
    return disable_component


def disable_components_vcs(database, components, parameter='id'):
    """The plural method of disable_component_vcs. This method disables the vcs
    of every component in the passed components list.
    """
    vcs_disabler = disable_vcs_closure(database, parameter=parameter)
    components = list(map(vcs_disabler, components))
    return components


def disable_vcs_closure(database, parameter='id'):
    """Disables vcs updates for the specified component. Components with a disabled
    vcs will not be updated from vcs.
    """

    def disable_vcs(component):
        """Disables vcs updates for the specified component. Components with a disabled
        vcs will not be updated from vcs.
        """
        component = component_model.update_component_vcs_status(component, status='disabled')
        component = mongo_dao.update_component_vcs_status_by_id(database,
                                                                component['_id'],
                                                                component['vcs']['status'])
        return component

    def disable_vcs_by_id(component_id):
        component = mongo_dao.get_component_by_id(database, component_id)
        component = disable_vcs(component)
        return component

    def disable_vcs_by_name(component_name):
        component = mongo_dao.get_current_component_by_name(database, component_name)
        component = disable_vcs(component)
        return component

    if parameter == 'id':
        return disable_vcs_by_id
    elif parameter == 'name':
        return disable_vcs_by_name
    return disable_vcs


def enable_components_vcs(database, components, parameter='id'):
    """The plural version of the enable_component_vcs method.
    Enables vcs updates for every component in the passed components list.
    """
    vcs_enabler = enable_vcs_closure(database, parameter=parameter)
    components = list(map(vcs_enabler, components))
    return components


def enable_vcs_closure(database, parameter='id'):
    """Enables vcs updates for the specified component. Components with enabled
    vcs will be updated from vcs.
    """

    def enable_vcs(component):
        """Enables vcs updates for the specified component. Components with enabled
        vcs will be updated from vcs.
        """
        component = component_model.update_component_vcs_status(component, status='enabled')
        component = mongo_dao.update_component_vcs_status_by_id(database,
                                                                component['_id'],
                                                                component['vcs']['status'])
        return component

    def enable_vcs_by_id(component_id):
        component = mongo_dao.get_component_by_id(database, component_id)
        component = enable_vcs(component)
        return component

    def enable_vcs_by_name(component_name):
        component = mongo_dao.get_current_component_by_name(database, component_name)
        component = enable_vcs(component)
        return component

    if parameter == 'id':
        return enable_vcs_by_id
    elif parameter == 'name':
        return enable_vcs_by_name
    return enable_vcs


def check_component_storage(component):
    """Checks for local storage of the given component for the given project.
    Returns True if the storage is found, and False if the storage is not found.
    """
    expected_location = component['location']
    directory_exists = file_dao.get_directory_exists(expected_location)
    return directory_exists


def update_component_functions(project, component):
    """Updates a component in the database for the specified project by
    updating the component functions. Returns the updated component record.
    Does not create a new component record.
    """
    component_id = component['_id']
    functions = component['functions']
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    component = mongo_dao.update_component_functions_by_id(project, component_id, functions)
    return component


def add_functions_to_component_closure(project, source='filesystem', profile=None):

    def add_functions_to_component(component):
        """This function takes a list of component dictionary objects and calls a method
        in the function_processor to get the function objects for each. The source
        determines how the functions are assembled, the default is to load complete
        functions from the filesystem, but also handles loading from the database.
        Once the functions are retrieved, the component record is either added to or
        updated within the database, depending on if it already exists (has an _id).
        """
        function_getter = function_processor.get_functions_for_component_closure(project,
                                                                                 source=source,
                                                                                 profile=profile)
        functions = function_getter(component)
        component = component_model.add_functions_to_component(component, functions)
        if '_id' in list(component.keys()):
            component = update_component_functions(project, component)
        else:
            component_adder = add_component_closure(project)
            component = component_adder(component)
        return component
    return add_functions_to_component


def get_components_from_filesystem(profile, project):
    """Returns components from filesystem for the given profile that match the given project.
    First makes component tuples from a filesystem source (specified by the profile),
    filters the tuples by the specified project, and then turns the tuples into
    component dictionary objects. Returns the completed dictionary objects.
    """
    component_tuples = get_component_tuples_from_filesystem(profile)
    component_filter = filter_component_tuples_by_project_closure(project['name'])
    component_tuples = list(filter(component_filter, component_tuples))
    components = make_components_from_tuples(component_tuples)
    return components


def clone_component_from_repository(component):
    """Clones a component from a vcs system into a local project directory, specified
    by target.
    Both parameters should be properties of the component object that is passed.
    The component object should be a component dictionary object..
    """
    clone_status = file_dao.clone_repository(component)
    return clone_status


def clone_components_from_repository(components):
    """Clones a list of component dictionary objects. Calls clone_component_from_repository
    for each component dictionary passed.
    """
    clone_result_dictionary = list(map(clone_component_from_repository, components))
    return clone_result_dictionary


def create_component_collection(database, components):
    """Creates a new component collection in the mongo database and returns
    a pointer to the collection.
    """
    collection_pointer = mongo_dao.create_component_collection(database, components)
    return collection_pointer


def filter_component_tuples_by_project_closure(project_name):
    """Filter method that only returns matching tuple records with the specified
    project.
    """
    def filter_component_tuples_by_project(component_tuple):
        if component_tuple.project == project_name:
            return component_tuple

    return filter_component_tuples_by_project


def get_all_components(project):
    """Returns all components in the mongo component collection as a list of
    dictionary objects.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    components = mongo_dao.get_all_components(project)
    return components


def get_enabled_components(database):
    """Returns enabled components from a given database.
    """
    components = mongo_dao.get_enabled_components(database)
    return components


def get_disabled_components(database):
    """Returns disabled components for the given project.
    """
    components = mongo_dao.get_disabled_components(database)
    return components


def get_vcs_enabled_components(database):
    """Returns components with the vcs enabled (turned on) for a given database.
    """
    components = mongo_dao.get_vcs_enabled_components(database)
    return components


def get_vcs_disabled_components(database):
    """Returns components with the vcs disabled (turned off) for a given database.
    """
    components = mongo_dao.get_vcs_disabled_components(database)
    return components


def get_removed_components(database):
    """Returns components that have been removed from the database.
    """
    components = mongo_dao.get_removed_components(database)
    return components


def get_all_current_components(database):
    """Returns all components in the mongo component collection that are current, i.e.
    they have no removal date.
    """
    current_components = mongo_dao.get_all_current_components(database)
    return current_components


def get_components_by_name(database, name):
    """Retrieves the entire component object by passing the name of the component.
    """
    components = mongo_dao.get_components_by_name(database, name)
    return components


def get_component_tuples_from_filesystem(profile):
    """Grabs the component definition, then uses the definition to make records
    from the component records file.
    Uses a specified profile to change keywords into absolute paths.
    Returns a 1D array of Component named tuples.
    """
    component_tuples = generic_processor.get_records_from_filesystem("component",
                                                                     "metadata",
                                                                     profile=profile)
    return component_tuples


def get_current_component_by_name(database, name):
    """Retrieves the current component object by specifiy the component name.
    """
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    try:
        component = mongo_dao.get_current_component_by_name(database, name)
        return component
    except IndexError:
        return None


def make_components_from_metadata(profile, database=None):
    """Uses a system profile to load the entire component collection from filesystem
    inputs. Used in initial setup and system development.
    """
    component_tuples = get_component_tuples_from_filesystem(profile)
    components = make_components_from_tuples(component_tuples)
    vcs_dictionaries = clone_components_from_repository(components)
    component_vcs_tool = component_model.add_vcs_to_component_closure(vcs_dictionaries)
    components = list(map(component_vcs_tool, components))
    component_function_tool = add_functions_to_component_closure(database, profile=profile)
    components = list(map(component_function_tool, components))
    mongo_dao.remove_component_collection(database)
    create_component_collection(database, components)
    return True


def make_components_from_tuples(component_tuples):
    """Takes component named tuples and returns them as a list of dictionaries.
    Additionally, uses an add date to indicate when the component was added.
    """
    add_date = utils.get_timestamp()
    component_maker = component_model.named_tuple_to_component_closure(add_date)
    components = list(map(component_maker, component_tuples))
    return components


def poll_component_by_name(database, component_name):
    """Polls a given component (by name) and
    returns the component (if it has changed) or
    False (if it is the same)
    """
    component = get_current_component_by_name(database, component_name)
    vcs_location = "{directory}/{name}".format(directory=component['location'], name=component['name'])
    remote_hash = file_dao.get_remote_repository_state(vcs_location,
                                                       component["vcs"]["repository"],
                                                       component["vcs"]["branch"])
    if component["vcs"]["hash"] == remote_hash:
        return False
    return component


def remove_component_collection(database):
    """Removes all components from the given database.
    """
    remove_status = mongo_dao.remove_component_collection(database)
    return remove_status


def remove_project_id_from_component(component):
    """Removes a project identifier field from the passed component. Returns
    the updated component dictionary object.
    """
    component = component_model.remove_project_identifier(component)
    return component


def replace_component(database, component):
    """Replaces a single component with the passed component object. Uses the
    internal mongo _id field to identify and replace the component.
    """
    component_id = component["_id"]
    component = mongo_dao.replace_component_by_id(database, component_id, component)
    return component


def update_components_from_repository(project):
    """Updates all components within the mongo component collection.
    """
    database = project['database']
    components = get_vcs_enabled_components(database)
    component_names = [component['name'] for component in components]
    component_names = list(set(component_names))
    component_repository_updater = update_component_from_repository_closure(project)
    current_components = list(map(component_repository_updater, component_names))
    return current_components


def update_component_from_repository_closure(project):
    """The closure for the update_component_from_repository method. Accepts a database
    object.
    """
    def update_component_from_repository(component_name):
        """Updates the component from the repository from a given component_name
        """
        database = project['database']
        component = poll_component_by_name(database, component_name)
        if component:
            new_vcs = file_dao.pull_remote_repository(component['name'],
                                                      component['vcs']['repository'],
                                                      component['location'],
                                                      component['vcs']['branch'])
            component_vcs_updater = component_model.update_component_vcs_closure(component)
            new_component = component_vcs_updater(new_vcs)
            change_date = utils.get_timestamp()
            component_date_changer = component_model.change_vcs_date_closure(change_date)
            component = component_date_changer(component)
            replace_component(database, component)
            new_component = component_date_changer(new_component)
            component_adder = add_component_closure(project, add_local_storage=False)
            current_component = component_adder(new_component)
            return current_component
        else:
            return None

    return update_component_from_repository


def update_component_location_closure(project):
    """Updates the component location by using the containing project to determine
    where the component is stored on disk.
    """
    def update_component_location(component):
        component = component_model.update_component_location(component, project)
        return component

    return update_component_location


if __name__ == '__main__':
    print('Please use component processor module as method package.')
