import sys
import imp
import time
from collections import OrderedDict
from pythoncommons import mongo_utils
from bson.objectid import ObjectId


def get_function_by_id(project, function_id):
    """Returns the function by the given id.
    """
    function_id = ObjectId(function_id)
    collection = get_language_collection(project)
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    cursor = mongo_utils.mongo_find_records(collection, argument=argument,
                                            named_tuple=False)
    function_list = mongo_utils.unload_cursor(cursor)
    try:
        return function_list[0]
    except IndexError:
        return None


def update_function(project, function, changes):
    """Updates the given parameter set by adding changes for the given changed
    parameters to the current record.
    """
    collection = get_language_collection(project)
    if type(function) in [dict, OrderedDict]:
        function_id = function['_id']
    else:
        function_id = function
    argument = mongo_utils.make_single_field_argument('_id', function_id)
    updates = []
    for change in changes:
        if '.' in change:
            nested_changes = change.split('.')
            nested_value_string = 'workflow'
            for nested_change in nested_changes:
                nested_value_string += '["'"{0}"'"]'.format(nested_change)
            updates.append(mongo_utils.make_update_argument(change, eval(nested_value_string)))
        else:
            updates.append(mongo_utils.make_update_argument(change, function[change]))
    update = mongo_utils.merge_update_args(updates)
    cursor = mongo_utils.mongo_update_one(collection, argument, update)
    if cursor.matched_count == 1:
        return get_function_by_id(project, function_id)
    return None


def get_language_collection(project):
    """Connects to the specified project and returns a pointer
    to the functions collection.
    """
    connection = mongo_utils.mongo_get_connection(project)
    collection = mongo_utils.mongo_get_collection(connection, 'language')
    return collection


def evaluate_python_3_code(project, code_id):
    """ The main entry point for evaluation of python_3 code.
    Uses a code id to first find and load the function, subsequently processing it.
    Once the function is processed, the function record is updated in the database
    and control of the program should be returned to the caller.
    """
    function = get_function_by_id(project, code_id)
    if function['type'] == 'method':
        result = evaluate_python_function(function)
        function['result'] = result
        function = update_function(project, function, changes=['result'])
    elif function['type'] == 'module':
        evaluate_python_module(function)
    return function


def add_system_paths(paths):
    """Adds all passed paths to the system path for handling required imports.
    """
    if type(paths) in [list]:
        for path in paths:
            sys.path.append(path)
    else:
        sys.path.append(paths)
    return


def get_input_string(inputs):
    """Creates and returns an input string for use in an eval from an input array
    or dictionary.
    """
    input_list = []
    if type(inputs) in [list]:
        length = len(inputs)
    elif type(inputs) in [dict, OrderedDict]:
        length = len(inputs.keys())
    for i in range(0, length):
        input_list.append('inputs["'"{0}"'"]'.format(i))
    input_string = ','.join(input_list)
    return input_string


def get_module(module_name, module_path):
    """Dynamically loads a module from source for use by the system. Assembles the
    module path if the path is incomplete.
    """
    if not module_path.endswith('.py'):
        if not module_path.endswith(module_name):
            if not module_path.endswith('/'):
                module_path += '/'
            module_path += module_name
        module_path += '.py'
    return imp.load_source(module_name, module_path)


def evaluate_python_function(function):
    """Evaluates the passed python function which is located at the given location.
    If the function requires inputs, they are added using the inputs dictionary.
    Paths that need to be imported for the module to run may be passed in the
    includes parameter as an array of strings or single string.
    """
    method_result = None
    inputs = function['inputs']
    output = function['output']
    includes = function['includes']
    results = {}
    results['info'] = {}
    results['info']['success'] = False
    results['output'] = {}
    if output:
        results['output'][output] = None
    if includes:
        add_system_paths(includes)
    module = get_module(function['module'], function['location'])
    method = getattr(module, function['function'])
    if method:
        input_string = get_input_string(inputs)
        eval_string = 'method({0})'.format(input_string)
        start = time.time()
        try:
            method_result = eval(eval_string)
            results['info']['success'] = True
        except (KeyError, ValueError):
            print('Python3 Function Evaluation Driver Failure.')
            results['info']['success'] = False
        end = time.time()
        if method_result:
            results['output'][output] = method_result
        results['info']['runtime'] = end - start
        return results
    return None


def evaluate_python_module(module_path, inputs=None, includes=None):
    """Evaluates a python module using an operating system call. Returns
    the output. (Not currently implemented)
    """
    return None


def apply(project, function):
    """Applies the python3 function in the given project.
    """
    return evaluate_python_3_code(project, function)


if __name__ == '__main__':
    evaluate_python_3_code(sys.argv[1], sys.argv[2])
