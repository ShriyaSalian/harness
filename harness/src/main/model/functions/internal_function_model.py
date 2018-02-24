from pythoncommons import general_utils


def named_tuple_to_function_closure(add_date):
    """Takes a named tuple function object and transforms it into the dictionary
    version, removing extraneous identifiers and including metadata.
    """

    def named_tuple_to_function(function_tuple):
        function = function_tuple._asdict()
        add_dates(function)
        add_classification(function)
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
        general_utils.remove_dictionary_keys(function, identifiers)

    return named_tuple_to_function


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
