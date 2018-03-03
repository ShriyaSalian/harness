import harness.src.main.dao.mongo.language_dao as language_dao
import harness.src.main.drivers.python_3 as python_3
import harness.src.main.drivers.python_2 as python_2


def route_function(project, function):
    """Routes functions to the proper scope router (internal or external).
    Returns the output of each function.
    """
    project = project['database']
    if function['scope'] == 'internal':
        return route_internal_function(project, function)
    elif function['scope'] == 'external':
        return route_external_function(project, function)


def route_internal_function(project, function):
    """Routes internal functions to the proper language driver.
    Returns the ouptut of each function.
    """
    function = serialize_function(project, function)
    function = evaluate_function(project, function)
    return function['result']


def get_driver(language, version):
    """Returns the proper executable for a given language and version.
    """
    if language == 'python':
        if version == '2':
            return python_2
        elif version == '3':
            return python_3
    return None


def evaluate_function(project, function):
    """
    """
    driver = get_driver(function['language'], function['language_version'])
    evaluation = driver.apply(project, str(function['_id']))
    return evaluation


def route_external_function(project, function, profile="standard"):
    pass


def serialize_function(project, function):
    """Adds the function to the language collection in database.
    Returns the identifier as a string.
    """
    function['id'] = str(function['id'])
    function['project'] = project
    function['result'] = None
    function['hold_output'] = function['output']
    includes = []
    output = 'output'
    if 'inputs' not in list(function.keys()):
        function['inputs'] = []
    if 'includes' not in list(function.keys()):
        function['includes'] = includes
    if 'output' not in list(function.keys()):
        function['output'] = output
        function['hold_output'] = {'output': None}
    else:
        function['hold_output'] = function['output']
        function['output'] = function['output']['name']
    function = language_dao.serialize_function(project, function)
    return function


if __name__ == '__main__':
    print('Please use language router module as method package.')
