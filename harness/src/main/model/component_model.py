from python_commons import utils
import copy


def add_functions_to_component(component, functions):
    if 'functions' in list(component.keys()):
        component['functions'] += functions
    else:
        component['functions'] = functions
    component['functions'] = list(set(functions))
    return component


def add_vcs_to_component_closure(vcs_dictionaries):

    def add_vcs_results_to_component(component):
        for vcs_info in vcs_dictionaries:
            if 'name' in list(vcs_info.keys()) and vcs_info['name'] == component['name']:
                add_vcs(component, vcs_info)
                return component

    def add_vcs(component, vcs_target):
        remove_component_keys = ['repository', 'repository_type']
        remove_vcs_keys = ['name', 'success']
        if not vcs_target['success']:
            vcs_target['vcs_type'] = None
        utils.remove_dictionary_keys(vcs_target, remove_vcs_keys)
        component['vcs'] = vcs_target
        component = update_component_status(component)
        component = update_component_vcs_status(component)
        utils.remove_dictionary_keys(component, remove_component_keys)

    return add_vcs_results_to_component


def change_vcs_date_closure(timestamp):

    def change_vcs_date(component):
        if component['add_date']:
            set_vcs_remove_date(component)
        else:
            set_vcs_add_date(component)
        return component

    def set_vcs_add_date(component):
        component['add_date'] = timestamp

    def set_vcs_remove_date(component):
        component['remove_date'] = timestamp

    return change_vcs_date


def named_tuple_to_component_closure(add_date):

    def named_tuple_to_component(component_tuple):
        component = component_tuple._asdict()
        add_dates(component)
        remove_identifiers(component)
        del component_tuple
        return component

    def remove_identifiers(component):
        remove_identifiers = ['project']
        utils.remove_dictionary_keys(component, remove_identifiers)

    def add_dates(component):
        component['add_date'] = add_date
        component['remove_date'] = None

    return named_tuple_to_component


def remove_database_artifacts(component):
    """This method exists to remove any artifacts from database storage from the
    passed component (such as database identifiers) and return the updated component
    dictionary object.
    """
    new_component = copy.deepcopy(component)
    identifiers = ['project', '_id']
    utils.remove_dictionary_keys(new_component, identifiers)
    return new_component


def reset_component_dates(component):
    """Resets the dates attached to the component to default dates. Returns the updated
    component object.
    """
    new_component = copy.deepcopy(component)
    new_component['add_date'] = utils.get_timestamp()
    new_component['remove_date'] = None
    return new_component


def update_component_status(component, status='enabled'):
    """Updates the status of the passed component with the specified status.
    The default status is enabled. Returns the updated component object.
    """
    try:
        component['status'] = status
    except KeyError:
        return component
    return component


def update_component_vcs_closure(component):

    def update_component_vcs(new_vcs):
        """Makes a deep copy of the current component, overwriting it with a new vcs.
        """
        component_copy = copy.deepcopy(component)
        component_copy['vcs'] = new_vcs
        update_component_vcs_status(component_copy, component['vcs']['status'])
        remove_vcs_keys = ['name', 'success']
        remove_component_keys = ['_id']
        utils.remove_dictionary_keys(component_copy['vcs'], remove_vcs_keys)
        utils.remove_dictionary_keys(component_copy, remove_component_keys)
        add_dates(component_copy)
        return component_copy

    def add_dates(component):
        component['add_date'] = None
        component['remove_date'] = None

    return update_component_vcs


def update_component_vcs_status(component, status='enabled'):
    """Updates the status of the vcs of the passed component with the specified status.
    The default status is enabled. Returns the updated component object.
    """
    try:
        vcs = component['vcs']
        vcs['status'] = status
        component['vcs'] = vcs
    except KeyError:
        return component
    return component


def update_component_location(component, project):
    """Updates a component dictionary objects location based on a project database.
    Returns the updated component dictionary object.
    """
    component['location'] = "{project}/components/{name}".format(project=project['location'],
                                                                 name=component['name'])
    return component


if __name__ == '__main__':
    print("Please use component model module as method package.")
