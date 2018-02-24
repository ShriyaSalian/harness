from pythoncommons import utils


def remove_workflow_identifier(workflow_function):
    """Simple filter to remove the workflow identifer from the passed function.
    """
    identifiers = ['workflow']
    utils.remove_dictionary_keys(workflow_function, identifiers)
    return workflow_function


def named_tuple_to_workflow_function_closure():
    """Takes a named tuple workflow function object and transforms it into the dictionary
    version, removing extraneous identifiers and including metadata.
    """

    def named_tuple_to_workflow_function(workflow_function_tuple):
        workflow_function = workflow_function_tuple._asdict()
#        add_unique_id(workflow_function)
        remove_identifiers(workflow_function)
        del workflow_function_tuple
        return workflow_function

    def add_unique_id(workflow_function):
        workflow_function['unique_id'] = utils.get_random_string()

    def remove_identifiers(workflow_function):
        identifiers = ['project']
        utils.remove_dictionary_keys(workflow_function, identifiers)

    return named_tuple_to_workflow_function
