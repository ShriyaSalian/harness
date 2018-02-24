import harness.src.main.model.function_parameter_model as parameter_model
from . import generic_processor


def filter_parameters_by_component(component, parameters):
    """Takes a component and a set of parameters, returning only those associated
    with the given component.
    """
    component_filter = component_filter_closure(component)
    parameters = list(filter(component_filter, parameters))
    return parameters


def project_filter_closure(component):
    """Closure for a method that returns any parameters associated with a
    specific project.
    """

    def project_filter(parameter):
        if parameter['project'] == component['project']:
            return parameter

    return project_filter


def component_filter_closure(component):
    """Closure for a method that returns any parameters associated with a
    specific component.
    """

    def component_filter(parameter):
        if parameter['component'] == component['name']:
            return parameter

    return component_filter


def function_filter_closure(function):
    """Closure for a method that returns any parameters associated with a
    specific function.
    """
    def function_filter(parameter):
        if 'function' in list(parameter.keys()):
            if parameter['function'] == function['name']:
                return parameter

    return function_filter


def get_parameters_from_filesystem(header=None, profile=None):
    """Retrieves all function parameters as an array of named tuples from a filesystem.
    """
    if not header:
        header = 'function_parameter'
    parameter_tuples = generic_processor.get_records_from_filesystem(header,
                                                                     'metadata',
                                                                     profile=profile)
    parameter_maker = parameter_model.named_tuple_to_function_parameter_closure()
    parameters = list(map(parameter_maker, parameter_tuples))
    return parameters


def input_filter(parameter):
    """Used to filter parameters that have an input type.
    """
    if parameter['type'] == 'input':
        return parameter


def output_filter(parameter):
    """Used to filter parameters that have an output type.
    """
    if parameter['type'] == 'output':
        return parameter


def classify_parameters(parameters):
    """Classifies a set of parameters into inputs and outputs, returning a dictionary
    with inputs and outputs keys and an array for each.
    """
    input_parameters = list(filter(input_filter, parameters))
    output_parameters = list(filter(output_filter, parameters))
    parameter_set = parameter_model.assemble_function_object(input_parameters,
                                                             output_parameters)
    return parameter_set


def assemble_function_parameters_closure(parameters):
    """Closure function for the process of taking a function dictionary and adding
    the associated parameters.
    """

    def assemble_function_parameters(function):
        function_filter = function_filter_closure(function)
        function_parameters = list(filter(function_filter, parameters))
        parameter_set = classify_parameters(function_parameters)
        return parameter_set

    return assemble_function_parameters

if __name__ == '__main__':
    print('Please use function parameter processor as method package.')
