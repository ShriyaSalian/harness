import sys
import imp
import time
from collections import OrderedDict


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
        length = len(list(inputs.keys()))
    for i in range(0, length):
        input_list.append('inputs[{0}]'.format(i))
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


def evaluate_python_function(function, inputs=None, output=None, includes=None):
    """Evaluates the passed python function which is located at the given location.
    If the function requires inputs, they are added using the inputs dictionary.
    Paths that need to be imported for the module to run may be passed in the
    includes parameter as an array of strings or single string.
    """
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
        except:
            results['info']['success'] = False
        end = time.time()
        if method_result:
            results['output'][output] = method_result
        results['info']['runtime'] = end - start
        return results
    return None


def evaluate_python_module(module_path, inputs=None, includes=None):
    """Evaluates a python module using an operating system call. Returns
    the output.
    """
    pass


if __name__ == '__main__':
    print('Please use python language processor module as method package.')
