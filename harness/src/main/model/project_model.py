def named_tuple_to_project_closure(add_date):
    """The basic model manipulation method for changing a named tuple into a dictionary
    object (actually returns an OrderedDict).
    """

    def named_tuple_to_project(project_tuple):
        project = project_tuple._asdict()
        add_dates(project)
        update_empty_properties(project)
        del project_tuple
        return project

    def add_dates(component):
        component['add_date'] = add_date
        component['remove_date'] = None

    def update_empty_properties(project):
        empty_properties = ['users', 'capabilities', 'parameters', 'components',
                            'evaluations', 'comparisons']
        for empty_property in empty_properties:
            if empty_property in list(project.keys()):
                if not project[empty_property]:
                    project[empty_property] = []
        return project

    return named_tuple_to_project


def add_components_to_project(project, components):
    """Adds a set of components to a given project. Returns the updated project object.
    """
    project['components'] = components
    return project


def add_project_database(project, database):
    """Adds a database record (string) to the passed project.
    """
    project = add_parameter_to_project(project, 'database', database)
    return project


def update_project_location(project, database):
    """Adds a local storage parameter to the passed project.
    """
    project['location'] = project['location'] + '/' + database
    return project


def add_parameter_to_project(project, parameter, value):
    """Generic method to add a parameter with the given value to a passed project
    dictionary object. If the parameter already exists, updated the parameter.
    Returns the updated project.
    """
    project[parameter] = value
    return project


if __name__ == '__main__':
    print("Project model module. Please use as method package.")
