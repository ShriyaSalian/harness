import harness.src.main.model.expression_model as expression_model
from . import generic_processor
from python_commons import utils
from collections import deque, OrderedDict
from copy import deepcopy
import re


def get_empty_parameters():
    parameters = {'inputs': [],
                  'intermediates': [],
                  'outputs': []}
    return parameters


def expression_filter_function_closure(component_name, function_name):
    """A filter function that returns a named tuple if it matches the
    given component and function external key.
    """

    def expression_filter_function(expression):
        if expression.component == component_name and expression.function == function_name:
            return expression

    return expression_filter_function


def update_expression_location_closure(component_location):

    def update_expression_evaluation_location(expression):
        """Returns the expression with the relative keyword path replaced by the
        actual evaluation path where the expression statement should be evaluated.
        """
        if 'location' in list(expression.keys()):
            expression = expression_model.update_location(expression, component_location)
        return expression

    return update_expression_evaluation_location


def add_parameters_to_expression(expression):
    """This method parses variables from an expression statement and
    adds the variables to a parameters collection on the expression object.
    """
    if 'statement' in list(expression.keys()):
        parameters = get_parameters_from_statement(expression['statement'])
        expression = expression_model.add_parameters_to_expression(expression, parameters)
    return expression


def get_parameters_from_statement(statement, pattern='$()'):
    """Parses a given statement and returns a list of the parameters in the statement.
    """
    if pattern == '$()':
        pattern = '\$\([a-zA-Z0-9_]*\)'
    parameters = re.findall(pattern, statement)
    parameters = list(set(parameters))
    return parameters


def get_expressions_for_function(component, function, expression_tuples=None,
                                 source="filesystem", profile=None):
    """Returns a list of all expressions for the given function and
    component name.
    """
    if not expression_tuples:
        if source == "filesystem":
            expression_tuples = get_expressions_from_filesystem(profile)
    filter_function = expression_filter_function_closure(component['name'], function['name'])
    expression_tuples = list(filter(filter_function, expression_tuples))
    expressions = make_expressions_from_tuples(expression_tuples)
    expression_evaluation_updater = update_expression_location_closure(component['location'])
    expressions = list(map(expression_evaluation_updater, expressions))
    expressions = list(map(add_parameters_to_expression, expressions))
    return expressions


def get_expressions_from_filesystem(profile):
    """Grabs the expression definition, then uses the definition to make records
    from the specified expression records file. Uses a specified profile to change
    keywords into absolute paths. Returns a 1D array of Expression named tuples.
    """
    expression_tuples = generic_processor.get_records_from_filesystem("expression",
                                                                      "metadata",
                                                                      profile=profile)
    return expression_tuples


def get_ordered_expressions(expressions):
    """Uses the builtin (standard library) sorted function and a lambda key to sort
    a list of expressions by their intended order. Returns the sorted list.
    """
    try:
        ordered_expressions = sorted(expressions, key=lambda expression: int(expression['order']))
    except:
        ordered_expressions = expressions
    return ordered_expressions


def get_classified_expression_parameters(expressions):
    """Classifies parameters of the input expression dictionary objects into inputs,
    intermediates, and outputs. See the README for definitions of these classifications.
    Returns a dictionary object containing the classified lists.
    """
    parameters = get_empty_parameters()
    ordered_expressions = get_ordered_expressions(expressions)
    parameter_maker = classify_expression_parameters_closure(parameters)
    ordered_expressions_deque = deque(ordered_expressions)
    parameters = parameter_maker(ordered_expressions_deque)
    return parameters


def update_parameters_input_collection(target_inputs, parameters, counter=0):
    """Takes an input list and a parameters dictionary object, checks each input to
    see if the input is in the intermediates and adds the parameter to the inputs if not.
    """
    try:
        if target_inputs[counter] not in parameters['intermediates']:
            parameters['inputs'].append(target_inputs[counter])
        counter += 1
        update_parameters_input_collection(target_inputs, parameters, counter)
    except IndexError:
        parameters['inputs'] = list(set(parameters['inputs']))
        return parameters


def update_parameters_output_collection(target_output, compare_inputs, parameters):
    """Takes an output and a parameters collection, checks the output against the
    parameters input collection. If the output is found, it is added to the parameters
    intermediates collection. If it is not found, it is added to the parameters output collection.
    """
    if target_output in compare_inputs:
        parameters['intermediates'].append(target_output)
    else:
        parameters['outputs'].append(target_output)
    return parameters


def classify_expression_parameters_closure(parameters):
    """Recursive function that takes a deque of ordered expressions and a parameters
    object, cycling over the expressions and classifying their parameters into three
    types (inputs, intermediates, or outputs), updating the parameters object, ultimately
    returning the final parameters object.
    """
    def classify_expression_parameters(expressions):
        try:
            expression = expressions.popleft()
            if expressions:
                compare_inputs = get_expression_parameters(deepcopy(expressions), 'inputs')
            else:
                compare_inputs = []
            update_parameters_input_collection(expression['inputs'], parameters)
            update_parameters_output_collection(expression['output'], compare_inputs, parameters)
            classify_expression_parameters(expressions)
        except IndexError:
            return
        return get_unique(parameters)

    def get_unique(parameters):
        parameter_lists = ['inputs', 'intermediates', 'outputs']
        for parameter_list in parameter_lists:
            parameters[parameter_list] = get_unique_template(parameters[parameter_list])
        return parameters

    def get_unique_template(parameter_list):
        empties = [None, 'None']
        if parameter_list in empties:
            parameter_list = []
        parameter_list = [i for i in list(set(parameter_list)) if i not in empties]
        return parameter_list

    return classify_expression_parameters


def get_expression_parameters(expressions, parameter, inputs=[]):
    """Returns all the things for the input expressions. Can be a single expression
    or a list of expressions. Takes expressions and also a parameter which specifies
    which things are being aggregated (inputs, output, etc)
    """
    if type(expressions) is deque:
        try:
            expression = expressions.popleft()
            inputs = get_expression_parameters(expression, parameter, inputs)
            get_expression_parameters(expressions, parameter, inputs)
        except IndexError:
            return inputs
    elif type(expressions) is list:
        get_expression_parameters(deque(expressions))
    elif type(expressions) is dict or type(expressions) is OrderedDict:
        inputs += expressions[parameter]
        return inputs
    return inputs


def make_expressions_from_tuples(expression_tuples):
    """Takes a list of expression named tuples and transforms them into
    a list of expression dictionary objects.
    """
    add_date = utils.get_timestamp()
    expression_maker = expression_model.named_tuple_to_expression_closure(add_date)
    expressions = list(map(expression_maker, expression_tuples))
    return expressions


def make_expressions_from_metadata(profile, component):
    """The test/overall method for grabbing expressions from
    a metadata(filesystem) source
    """
    expression_tuples = get_expressions_from_filesystem(profile)
    expressions = make_expressions_from_tuples(expression_tuples)
    expression_evaluation_updater = update_expression_location_closure(component['location'])
    expressions = list(map(expression_evaluation_updater, expressions))
    expressions = list(map(add_parameters_to_expression, expressions))
    return expressions


if __name__ == '__main__':
    print('Please use expression processor module as method package.')
