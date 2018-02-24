def set_parameter_source(parameter, source):
    """Updates the parameter source to the specified source.
    Returns the updated parameter.
    """
    parameter['source'] = source
    return parameter


def get_parameter_target(parameter):
    """Returns the target object for the given parameter.
    """
    return parameter['target']


def get_parameter_source(parameter):
    """Returns the source object for the given parameter.
    """
    return parameter['source']


def set_parameter_target(parameter, target):
    """Updates the parameter target to the specified target.
    Returns the updated parameter.
    """
    parameter['target'] = target
    return parameter


def update_parameter_target(target, new_target):
    for key in list(new_target.keys()):
        target[key] = new_target[key]


def update_parameter_source(source, new_source):
    for key in list(new_source.keys()):
        source[key] = new_source[key]


def make_new_workflow_parameter_target():
    """Returns a new workflow parameter target.
    """
    parameter_target = {}
    parameter_target['type'] = None
    parameter_target['translator'] = None
    parameter_target['name'] = None
    return parameter_target


def make_new_workflow_parameter_source():
    """Returns a new workflow parameter source.
    """
    parameter_source = {}
    parameter_source['type'] = None
    parameter_source['value'] = None
    return parameter_source

if __name__ == '__main__':
    print('Please use workflow parameter model module as method package.')
