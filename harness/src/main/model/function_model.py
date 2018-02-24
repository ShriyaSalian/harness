from pythoncommons import utils


def add_unique_id(function):
    """Adds a unique id for the function when it is added to a workflow
    to support multiple copies of the same function.
    """
    function['unique_id'] = utils.get_random_string()
    return function


def get_unique_id(function):
    """Returns a unique workflow id for the given function.
    """
    if 'unique_id' in list(function.keys()):
        return function['unique_id']
    else:
        return None


def get_function_id(function):
    """Returns the id for the given function.
    """
    if '_id' in list(function.keys()):
        return function['_id']
    else:
        return None


def get_function_parameters(function):
    """Gets the parameters object for the given function.
    """
    if 'parameters' in list(function.keys()):
        return function['parameters']
    else:
        return None


def named_tuple_to_function_closure(add_date):
    """Takes a named tuple function object and transforms it into the dictionary
    version, removing extraneous identifiers and including metadata.
    """

    def named_tuple_to_function(function_tuple):
        function = function_tuple._asdict()
        add_dates(function)
#        add_classification(function)
        remove_identifiers(function)
        del function_tuple
        return function

    def function_type_to_complexity(function_type):
        type_complexity_dictionary = {'external': 'fundamental',
                                      'internal': 'fundamental',
                                      'compound': 'unknown'}
        return type_complexity_dictionary[function_type]

    def add_dates(function):
        function['add_date'] = add_date
        function['remove_date'] = None

    def add_classification(function):
        function['class'] = {}
        function['class']['type'] = function['type']
        function['class']['complexity'] = function_type_to_complexity(function['type'])

    def remove_identifiers(function):
        identifiers = ['project']
        utils.remove_dictionary_keys(function, identifiers)

    return named_tuple_to_function


def add_parameter_set(function, parameter_set):
    """Adds a parameter set to the passed function.
    Returns the updated function.
    """
    function['parameters'] = parameter_set
    return function


def update_function_parameters(function, parameter_object):
    """Splits a parameter object and adds the components to a function.
    """
    parameters = {}
    if type(parameter_object) is dict:
        if 'outputs' in list(parameter_object.keys()):
            parameters['outputs'] = parameter_object['outputs']
        else:
            parameters['outputs'] = None
        if 'inputs' in list(parameter_object.keys()):
            parameters['inputs'] = parameter_object['inputs']
        else:
            parameters['inputs'] = None
        if 'intermediates' in list(parameter_object.keys()):
            parameters['intermediates'] = parameter_object['intermediates']
        else:
            parameters['intermediates'] = None
    else:
        parameters['outputs'] = None
        parameters['inputs'] = None
        parameters['intermediates'] = None
    function['parameters'] = parameters
    return function


if __name__ == '__main__':
    print("Please use this module as a method package.")
