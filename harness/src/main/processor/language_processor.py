import harness.src.main.dao.mongo.language_dao as language_dao
from pythoncommons import subprocess_utils
import os


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
    evaluate_function(project, function)
    function_id = function['_id']
    updated_function = language_dao.get_function_by_id(project, function_id)
    return updated_function['result']


def evaluate_function(project, function):
    """
    """
    evaluation_string = get_evaluation_string(project, function)
    evaluation = subprocess_utils.get_Popen_output(evaluation_string)
    #subprocess_utils.run_subprocess(evaluation_string)
    return


def get_evaluation_string(project, function):
    """Assembles an evaluation string for the given function. Based on
    language, language type, and function object id.
    """
    identifier = str(function['_id'])
    current_directory = os.getcwd()
    driver_directory = current_directory.rsplit('/harness/', 1)[0]
    driver_directory += '/harness/drivers/'
    if function['language'] == 'python':
        if function['language_version'] == '2':
            program = 'python'
            driver_directory += 'python_2'
        elif function['language_version'] == '3':
            program = 'python3'
            driver_directory += 'python_3'
        driver = driver_directory + '.py'
    evaluation_string = '{program} {driver} {project} {identifier}'.format(program=program,
                                                                           driver=driver,
                                                                           project=project,
                                                                           identifier=identifier)
    return evaluation_string


def route_external_function(function):
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
