from pythoncommons import general_utils


def get_inputs(parameter):
    """Returns the inputs for the given parameter.
    """
    return parameter['inputs']


def get_outputs(parameter):
    """Returns the outputs for the given parameter.
    """
    return parameter['outputs']


def remove_identifiers(parameter):
    """Removes the identifiers (extraneous information) that should not be stored
    with the other information about the parameter.
    """
    identifiers = ['project', 'component', 'function', 'type']
    general_utils.remove_dictionary_keys(parameter, identifiers)
    return parameter


def assemble_function_object(inputs, outputs):
    """Creates a new dictionary object for attachment on a function object.
    """
    parameter_set = {}
    parameter_set['inputs'] = []
    parameter_set['outputs'] = []
    if inputs:
        list(map(remove_identifiers, inputs))
        parameter_set['inputs'] = inputs
    if outputs:
        list(map(remove_identifiers, outputs))
        parameter_set['outputs'] = outputs
    return parameter_set


def remove_scope_identifier(function_parameter):
    """Removes the scope identifier (input or output) from the function parameter object.
    """
    identifiers = ['type']
    general_utils.remove_dictionary_keys(function_parameter, identifiers)
    return function_parameter


def remove_function_identifier(function_parameter):
    """Removes the function identifier from the function_parameter object.
    """
    identifiers = ['function']
    general_utils.remove_dictionary_keys(function_parameter, identifiers)
    return function_parameter


def named_tuple_to_function_parameter_closure():
    """Takes a named tuple function parameter object and transforms it into the dictionary
    version, removing extraneous identifiers and including metadata.
    """

    def named_tuple_to_function_parameter(named_tuple):
        function_parameter = named_tuple._asdict()
        del named_tuple
        return function_parameter

    return named_tuple_to_function_parameter

if __name__ == '__main__':
    print('Please use function parameter model module as method package.')
