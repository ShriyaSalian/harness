import harness.src.main.processor.generic_processor as generic_processor
import harness.src.main.model.functions.compound_function_model as compound_model
from collections import deque, OrderedDict
from pythoncommons import general_utils


def get_empty_parameters():
    """Returns an empty parameters object for use in other methods.
    """
    empty_parameters = {'inputs': [],
                        'intermediates': [],
                        'outputs': []}
    return empty_parameters


def get_subfunctions_for_component(component, source='filesystem', profile=None):
    """This method takes an component name, source, and profile and returns
    a list of complete compound functions for that component, acquired from the specified
    source. If source is filesystem, profile is required to overwrite relative path keywords.
    """
    if source == 'filesystem':
        subfunction_tuples = get_compound_functions_from_filesystem(profile)
        subfunctions = make_compound_functions_from_tuples(subfunction_tuples)
    component_filter = subfunction_component_filter_closure(component)
    subfunctions = list(filter(component_filter, subfunctions))
    return subfunctions


def add_subfunctions_to_compound_functions(compound_functions, subfunctions):
    """The main call method for adding subfunctions to a passed list of compound_function
    dictionary objects.
    """
    subfunction_adder = add_subfunctions_to_function_closure(subfunctions)
    compound_functions = list(map(subfunction_adder, compound_functions))
    compound_functions = list(map(compound_model.remove_all_subfunction_identifiers, compound_functions))
    return compound_functions


def assign_complexity_to_compound_functions(compound_functions):
    """Takes a list of compound functions with an unassigned complexity and assigns
    a complexity to each element in the list, returning the updated list of functions.
    """
    compound_function_complexity_assigner = complexity_assignment_utility_closure([])
    compound_functions = compound_function_complexity_assigner(compound_functions)
    return compound_functions


def complexity_assignment_utility_closure(assigned_functions):
    """This is the closure function for assigning complexity to a compound function. It is
    used to test each subfunction to ensure that it is not a recursive function. If the subfunctions
    are all either fundamental or simple, the parent function is also a simple function. If
    any of the children is a recursive function, the parent function is assigned a
    recursive complexity.
    """

    def complexity_assignment_utility(compound_functions, assigned_functions=assigned_functions):
        change_flag = False
        if compound_functions:
            for function in compound_functions:
                if all_subfunctions_evaluated(function['subfunctions']):
                    if all_subfunctions_evaluatable(function['subfunctions']):
                        compound_model.make_complexity_simple(function)
                    else:
                        compound_model.make_complexity_recursive(function)
                    change_flag = True
                    assigned_functions.append(compound_functions.pop(compound_functions.index(function)))
                    break
            if change_flag:
                complexity_assignment_utility(compound_functions, assigned_functions)
            else:
                list(map(compound_model.make_complexity_recursive, compound_functions))
                assigned_functions += compound_functions
                return assigned_functions
        return assigned_functions

    def all_subfunctions_evaluated(subfunctions):
        subfunctions_evaluated_list = list(map(subfunction_evaluated, subfunctions))
        if False in subfunctions_evaluated_list:
            return False
        return True

    def subfunction_evaluated(subfunction):
        if subfunction['name'] in get_evaluated_function_names(assigned_functions):
            return True
        elif subfunction['class']['type'] in ['external', 'internal']:
            return True
        return False

    def all_subfunctions_evaluatable(subfunctions):
        subfunctions_evaluatable_list = list(map(subfunction_evaluatable, subfunctions))
        if False in subfunctions_evaluatable_list:
            return False
        return True

    def subfunction_evaluatable(subfunction):
        assigned_function = [function for function in assigned_functions if function['name'] == subfunction['name']]
        if assigned_function:
            assigned_function = assigned_function[0]
            if assigned_function['class']['complexity'] in ['simple']:
                subfunction['class']['complexity'] = assigned_function['class']['complexity']
                return True
        elif subfunction['class']['type'] in ['external', 'internal']:
            if subfunction['class']['complexity'] in ['simple', 'fundamental']:
                return True
        return False

    def get_evaluated_function_names(function_list):
        function_names = list(map(get_evaluated_function_name, function_list))
        return function_names

    def get_evaluated_function_name(function):
        function_name = function['name']
        return function_name

    return complexity_assignment_utility


def add_subfunctions_to_function_closure(compound_functions):
    """Handles adding subfunctions to a compound function. Takes a list of compound_function
    dictionary objects, filters them based on function matching, removes extraneous identifier
    information and returns the function with the completed compound function object.
    """

    def add_subfunctions_to_function(function):
        filter_function = subfunction_filter_closure(function['name'])
        filtered_compound_functions = list(filter(filter_function, compound_functions))
        function['subfunctions'] = filtered_compound_functions
        return function

    def subfunction_filter_closure(function_name):

        def subfunction_filter(subfunction):
            if subfunction['function'] == function_name:
                return subfunction

        return subfunction_filter

    return add_subfunctions_to_function


def add_parameters_to_compound_functions(compound_functions, source='filesystem', component=None,
                                         external_functions=None, internal_functions=None):
    """The list version of the add_parameters_to_compound_function method.
    For every compound function in the list, calls add_parameters_to_compound_function.
    Returns a list of updated compound_functions objects with inputs/intermediates/outputs
    added to a parameters object.
    """
    parameter_adder = add_parameters_to_compound_function_closure(source=source,
                                                                  component=component,
                                                                  compound_functions=compound_functions,
                                                                  external_functions=external_functions,
                                                                  internal_functions=internal_functions)
    compound_functions = list(map(parameter_adder, compound_functions))
    return compound_functions


def add_parameters_to_compound_function_closure(source='filesystem', component=None,
                                                compound_functions=None, external_functions=None,
                                                internal_functions=None):
    """Takes a compound_function dictionary object and assembles a parameters object
    containing the following lists: inputs/outputs/intermediates for the entire compound
    function. Handles nested compound functions. Returns the updated compound function
    dictionary object.
    """
    def add_parameters_to_compound_function(compound_function):
        if parameters_available(compound_function):
            subfunction_parameters = [get_subfunction_parameters(subfunction) for subfunction in
                                      compound_function['subfunctions']]
        else:
            subfunction_parameters = [get_empty_parameters()]
        compound_function['parameters'] = flatten_compound_function_parameters(subfunction_parameters)
        return compound_function

    def parameters_available(function):
        if function['class']['complexity'] in ['recursive']:
            return False
        if not function['subfunctions']:
            return False
        return True

    def get_all_subfunction_parameters(compound_function):
        subfunction_parameters = [get_subfunction_parameters(subfunction) for subfunction in
                                  compound_function['subfunctions']]
        return subfunction_parameters

    def get_subfunction_parameters(subfunction):
        parameters = get_empty_parameters()
        if subfunction['class']['type'] == 'compound':
            parameters = assemble_compound_function(subfunction, parameters)
        elif subfunction['class']['type'] == 'external':
            parameters = assemble_external_function(subfunction, parameters)
        elif subfunction['class']['type'] == 'internal':
            parameters = assemble_internal_function(subfunction, parameters)
        return parameters

    def assemble_compound_function(subfunction, parameters):
        if compound_functions:
            function_match = list(filter(lambda function: function['name'] == subfunction['name'],
                                  compound_functions))[0]
            if function_match:
                parameters = get_all_subfunction_parameters(function_match)
        return parameters

    def assemble_external_function(subfunction, parameters):
        if external_functions:
            function_match = list(filter(lambda function: function['name'] == subfunction['name'],
                                  external_functions))[0]
            if function_match:
                parameters = function_match['parameters']
        return parameters

    def assemble_internal_function(subfunction, parameters):
        if internal_functions:
            function_match = list(filter(lambda function: function['name'] == subfunction['name'],
                                  internal_functions))[0]
            if function_match:
                return parameters
#                parameters = function_match['parameters']
        return parameters

    return add_parameters_to_compound_function


def flatten_compound_function_parameters(subfunction_parameters):
    """Recursively flattens a list of arbitrarily nested compound function parameter
    objects, returning the reduced parameter object.
    """
    flattened_parameters = list(flatten_parameters(subfunction_parameters))
    flattened_parameters = list(map(restructure_parameter_elements, flattened_parameters))
    reduced_parameter_object = get_empty_parameters()
    flattened_parameter_deque = deque(flattened_parameters)
    reduced_parameters = reduce_parameters(flattened_parameter_deque, reduced_parameter_object)
    return reduced_parameters


def reduce_parameters(parameter_object_deque, reduced_parameter_object):
    """Takes a flat list of parameter dictionary objects and turns them into a single
    parameter dictionary object by sequentially combining them.
    """
    if parameter_object_deque:
        parameter_object = parameter_object_deque.popleft()
        reduced_parameter_object = update_reduced_parameter_object(parameter_object,
                                                                   parameter_object_deque,
                                                                   reduced_parameter_object)
        reduce_parameters(parameter_object_deque, reduced_parameter_object)
    return reduced_parameter_object


def update_reduced_parameter_object(target_object, future_objects, final_object):
    """Used in the reduce parameters method. Passes a target object and the future objects
    (subfunctions that come later in the order of evaluation) and evaluates the inputs
    and outputs of the target object to update the final object of the compound function.
    Returns the updated compound function parameter object.
    """
    if target_object['inputs']:
        final_object = update_parameter_object_inputs(target_object['inputs'], final_object)
    if target_object['outputs']:
        future_inputs = combine_parameter_inputs(future_objects)
        final_object = update_parameter_object_outputs(target_object['outputs'],
                                                       future_inputs, final_object)
    return final_object


def update_parameter_object_outputs(test_outputs, future_inputs, final_object):
    """Used in the parameter reduction algorithm, checks a set of test outputs against
    future inputs in the same compound function. If the outputs are used by a future
    subfunction, the output is added to the final reduced object as an intermediate parameter.
    If it is not, it is added as an output parameter. This method returns the updated final
    object.
    """
    for test_output in test_outputs:
        if test_output in future_inputs:
            final_object['intermediates'].append(test_output)
        else:
            final_object['outputs'].append(test_output)
    final_object['intermediates'] = list(set(final_object['intermediates']))
    final_object['outputs'] = list(set(final_object['outputs']))
    return final_object


def combine_parameter_inputs(parameter_objects):
    """Combines all the inputs into a single list for a list of parameter objects.
    Handles error cases. Returns the combined input list.
    """
    combined_inputs = []
    for parameter_object in parameter_objects:
        if parameter_object['inputs'] and isinstance(parameter_object['inputs'], list):
            combined_inputs += parameter_object['inputs']
    combined_inputs = list(set(combined_inputs))
    return combined_inputs


def update_parameter_object_inputs(test_inputs, final_object):
    """Used in the parameter reduction algorithm, checks inputs to see if they are
    in the reduced object intermediates. If they are not, they are necessary inputs
    for the function and are added. This method returns the updated final reduced object.
    """
    for test_input in test_inputs:
        if test_input and test_input not in final_object['intermediates']:
            final_object['inputs'].append(test_input)
    final_object['inputs'] = list(set(final_object['inputs']))
    return final_object


def restructure_parameter_elements(parameter_object):
    """Restructures parameter elements to get ready for reduction. It does two things.
    1) Moves the elements of a parameter object dictionary from intermediates to
    outputs.
    2) If the inputs is None (NoneType) changes to empty input list.
    """
    if isinstance(parameter_object, dict) or isinstance(parameter_object, OrderedDict):
        parameter_object = intermediates_to_outputs(parameter_object)
        parameter_object = remove_nonetype_inputs(parameter_object)
    return parameter_object


def intermediates_to_outputs(parameter_object):
    """Checks the outputs and intermediates elements of a parameter object dictionary,
    moving intermediate elements to the output and clearing the intermediate if possible.
    Returns the updated parameter_object.
    """
    if 'outputs' in parameter_object and 'intermediates' in parameter_object:
        if parameter_object['intermediates'] and parameter_object['outputs']:
            parameter_object['outputs'] += parameter_object['intermediates']
            parameter_object['intermediates'] = []
        else:
            if not parameter_object['intermediates']:
                parameter_object['intermediates'] = []
            if not parameter_object['outputs']:
                parameter_object['outputs'] = []
    return parameter_object


def remove_nonetype_inputs(parameter_object):
    """Checks the input of a parameter object, and if it is none type, makes it
    an empty list.
    """
    if not parameter_object['inputs']:
        parameter_object['inputs'] = []
    return parameter_object


def flatten_parameters(parameter_object):
    """This function takes a list of arbitrarily nested parameter objects and returns
    a generator to flatten them all into a single list, preserving the order. To use
    this on a list, it must be called as a list(flatten_parameters(param_list)))
    """
    for parameter_element in parameter_object:
        if isinstance(parameter_element, list):
            for nested_element in flatten_parameters(parameter_element):
                yield nested_element
        else:
            yield parameter_element


def get_ordered_subfunctions(subfunctions):
    """Uses the builtin (standard library) sorted function and a lambda key to sort
    a list of subfunctions by their intended order (on order parameter). Returns the sorted list.
    """
    try:
        ordered_subfunctions = sorted(subfunctions, key=lambda subfunction: int(subfunction['order']))
    except:
        ordered_subfunctions = ordered_subfunctions
    return ordered_subfunctions


def order_function_subfunctions(compound_function):
    """Takes a compound function dictionary object and returns the same object,
    with its subfunctions put into the correct order.
    """
    subfunctions = get_ordered_subfunctions(compound_function['subfunctions'])
    compound_function['subfunctions'] = subfunctions
    return compound_function


def subfunction_component_filter_closure(component):
    """A filter function designed to be used in the filter pattern. returns a function
    if it belongs to one of the functions attached to a specified component.
    """

    def subfunction_component_filter(subfunction):
        if subfunction['component'] == component:
            subfunction = compound_model.remove_component(subfunction)
            return subfunction

    return subfunction_component_filter


def assign_subfunction_type_closure(functions):
    """Takes a list of functions ([function_list)
    and uses these functions as a lookup for the
    compound function. For every subfunction in the compound function, a matching function
    is found from the lookup list. The type of the subfunction is assigned from this lookup.
    Returns the updated compound_function with types assigned to its subfunctions.
    """
    def assign_subfunction_types_for_compound_function(compound_function):
        subfunctions = list(map(assign_subfunction_class, compound_function['subfunctions']))
        compound_function['subfunctions'] = subfunctions
        return compound_function

    def assign_subfunction_class(subfunction):
        function_match = list(filter(lambda function: function['name'] == subfunction['name'],
                              functions))[0]
        subfunction['class'] = function_match['class']
        return subfunction

    return assign_subfunction_types_for_compound_function


def make_compound_functions_from_tuples(compound_function_tuples):
    """Takes a list of compound function named tuples and transforms them into a list of
    function dictionary objects.
    """
    add_date = general_utils.get_timestamp()
    compound_function_maker = compound_model.named_tuple_to_compound_function_closure(add_date)
    compound_functions = list(map(compound_function_maker, compound_function_tuples))
    return compound_functions


def get_compound_functions_from_filesystem(profile):
    """Grabs the function definition, then uses the definition to make records
    from the specified function records file. Uses a specified profile to change
    keywords into absolute paths. Returns a 1D array of Function named tuples.
    """
    compound_function_tuples = generic_processor.get_records_from_filesystem("compound_function",
                                                                             "metadata",
                                                                             profile=profile)
    return compound_function_tuples

if __name__ == '__main__':
    print("Please use as method package.")
