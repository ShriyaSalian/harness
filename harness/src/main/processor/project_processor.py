import harness.src.main.dao.mongo.project_dao as mongo_dao
import harness.src.main.dao.filesystem.filesystem_dao as file_dao
import harness.src.main.model.project_model as project_model
import harness.src.main.processor.component_processor as component_processor
from pythoncommons import general_utils
from . import generic_processor


def add_components_to_project_closure(source='filesystem', profile=None, components=None):
    """This closure returns a method to add components to the specified project.
    the closure must pass a source (where to build the components from).
    if the source equals 'filesystem', the method must take a profile (string).
    If the source equals 'memory', the method must accept an array of components or
    a single component.
    """
    def add_components_to_project_from_filesystem(project):
        """This method updates a project record from a filesystem (initial setup).
        It handles loading components from the filesystem.
        """
        components = component_processor.get_components_from_filesystem(profile,
                                                                        project)
        components = component_processor.add_components_to_project(project, components)
        components = component_processor.get_all_components(project['database'])
        return components

    def add_components_to_project_from_memory(project):
        """This method updates a project record in storage, adds components to the
        project storage database, and returns the updated project record.
        NOT CURRENTLY IMPLEMENTED
        """
        pass

    if source == 'filesystem':
        return add_components_to_project_from_filesystem
    elif source == 'memory':
        return add_components_to_project_from_memory
    return None


def create_new_project(project):
    """Attempts to create a new project in storage by registering the project with
    the project database and creating a new database to store the project in. Returns
    the project if successful. If it fails for any reason, returns None.
    """
    existing_project = get_project_by_name(project['name'])
    if not existing_project:
        database_name = get_available_project_database(project['name'])
        project = project_model.add_project_database(project, database_name)
        project = project_model.update_project_location(project, database_name)
        project_id = mongo_dao.create_new_project(project)
        project = mongo_dao.get_project_by_id(project_id)
        return project
    return None


def create_new_projects(projects):
    """The plural version of create new project method. Maps the create_new_projects
    call to a list of projects passed.
    """
    projects = list(map(create_new_project, projects))
    return projects


def filter_components_by_project_closure(project_name):
    """Filter method that returns a component if it belongs to the specified project.
    The project is specified by name.
    """
    def filter_components_by_project(component):
        try:
            if component['project'] == project_name:
                return component
        except KeyError:
            return None
    return filter_components_by_project


def get_all_components(project=None, project_id=None, project_name=None, database=None):
    """Returns all the components for the specified project id that are currently in the
    project storage.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        if not database:
            database = project['database']
    except KeyError:
        return None
    try:
        all_components = component_processor.get_all_components(database)
        return all_components
    except:
        return None


def get_all_projects():
    """Returns all project objects currently registered on the system as a list.
    If there are none available, returns an empty list.
    """
    projects = mongo_dao.get_all_projects()
    if not projects:
        projects = []
    return projects


def get_available_project_database(name):
    """Finds an available database name and returns the available name.
    """
    valid_name = False
    while not valid_name:
        check_name = make_project_database_name(name)
        valid_name = mongo_dao.validate_project_database(check_name)
    return valid_name


def get_current_components(project=None, project_id=None, project_name=None):
    """Returns all the current components for a specified project.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        database = project['database']
    except KeyError:
        return None
    try:
        current_components = component_processor.get_all_current_components(database)
        return current_components
    except:
        return None


def get_project_by_name(project_name):
    """Returns the project with the specified name. If the project does not exist,
    the method returns None.
    """
    try:
        project = mongo_dao.get_project_by_name(project_name)
    except IndexError:
        project = None
    return project


def get_project_id(project):
    """Returns the project id for the passed project.
    """
    try:
        return project['_id']
    except KeyError:
        return None
    return None


def get_projects_from_filesystem(profile):
    """Grabs the project definition, then uses the definition to make records
    from the project records file.
    Uses a specified profile to change keywords into absolute paths.
    Returns a 1D array of Project named tuples.
    """
    project_tuples = generic_processor.get_records_from_filesystem("project",
                                                                   "metadata",
                                                                   profile=profile)
    return project_tuples


def make_project_database_name(name):
    """Small utility function that creates a unique name for a project database.
    Returns the name.
    """
    random_string = general_utils.get_random_string(length=5)
    database_name = name + '_' + random_string + '_' + 'project'
    return database_name


def make_projects_from_metadata(profile=None):
    """Uses a system profile to load projects from filesystem
    inputs. Used in initial setup and system development.
    """
    project_tuples = get_projects_from_filesystem(profile)
    projects = make_projects_from_tuples(project_tuples)
    projects = create_new_projects(projects)
    component_adder = add_components_to_project_closure(profile=profile)
    project_content = list(map(component_adder, projects))
    return project_content


def make_projects_from_tuples(project_tuples):
    """Makes project records from an array of named tuples. Returns the new list
    of project dictionary objects.
    """
    add_date = general_utils.get_timestamp()
    project_maker = project_model.named_tuple_to_project_closure(add_date)
    projects = list(map(project_maker, project_tuples))
    return projects


def remove_all_projects():
    """Removes all projects in the project collection.
    """
    projects = get_all_projects()
    try:
        project_ids = list(map(get_project_id, projects))
        list(map(remove_project_by_id, project_ids))
        return True
    except:
        return False


def remove_project(project=None, project_name=None, project_id=None, database=None):
    """Completely removes a project, all references, and its data from storage by
    specifying the project record, the project id, or the project name.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        if not database:
            database = project['database']
        if not project_id:
            project_id = project['_id']
    except KeyError:
        return None
    try:
        remove_local_vcs_storage(project_id=project_id)
        mongo_dao.remove_project_database(database)
        removal = mongo_dao.remove_project_record_by_id(project_id)
        return removal
    except:
        return None


def remove_project_by_id(project_id):
    """Completely removes a project, all references, and its data from storage by
    specifying the project id.
    """
    remove_project(project_id=project_id)


def remove_project_components(project=None, project_name=None, project_id=None, database=None):
    """Removes all components from a given project. Accepts a project dictionary object,
    a project name, or a project id.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        if not database:
            database = project['database']
    except KeyError:
        return None
    try:
        removal = component_processor.remove_component_collection(database)
        return removal
    except:
        return None


def remove_local_vcs_storage(project=None, project_id=None, project_name=None, project_path=None):
    """Removes local version control storage for a given project. Accepts a project
    object, a project_id, a project_name, or a project_path.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        if not project_path:
            project_path = project['location']
    except KeyError:
        return None
    try:
        file_dao.remove_directory(project_path)
        return True
    except:
        return None


def update_project_components_from_vcs(project=None, project_id=None, project_name=None):
    """Updates all project components in local storage from their specified
    vcs (version control system). Uses a passed project. Can specify a project,
    a project name, or a project id. If it is successful, returns the new components.
    Otherwise, it will return None.
    """
    if project_id:
        project = mongo_dao.get_project_by_id(project_id)
    elif project_name:
        project = mongo_dao.get_project_by_name(project_name)
    try:
        new_components = component_processor.update_components_from_repository(project)
        return new_components
    except:
        return None


if __name__ == '__main__':
    print('Please use the project processor module as a method package.')
