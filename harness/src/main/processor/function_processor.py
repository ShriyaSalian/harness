import harness.src.main.model.function_model as function_model
import harness.src.main.processor.functions.compound_function_processor as compound_processor
import harness.src.main.processor.functions.external_function_processor as external_processor
import harness.src.main.processor.function_parameter_processor as function_parameter_processor
import harness.src.main.dao.mongo.function_dao as mongo_dao
from pythoncommons import utils
from collections import OrderedDict
from . import generic_processor


def add_function_parameters(component, functions, source='filesystem', profile=None):
    """This method takes an array of functions and adds parameters to them.
    """
    if source == 'filesystem':
        parameters = function_parameter_processor.get_parameters_from_filesystem(profile=profile)
        parameters = function_parameter_processor.filter_parameters_by_component(component, parameters)
        parameter_assembler = assemble_function_parameters_closure(parameters)
        functions = list(map(parameter_assembler, functions))
    return functions


def get_function_by_id(project, function_id):
    """Returns the function by the given function id.
    """
    return mongo_dao.get_function_by_id(project, function_id)


def assemble_function_parameters_closure(parameters):

    def assemble_function_parameters(function):
        """This method takes an array of functions and adds parameters to them.
        """
        parameter_tool = function_parameter_processor.assemble_function_parameters_closure(parameters)
        parameter_set = parameter_tool(function)
        function = function_model.add_parameter_set(function, parameter_set)
        return function

    return assemble_function_parameters


def get_current_functions(project, component=None):
    """Returns the current functions in the given database. Optional component
    parameter lets user return only functions for the given component.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    if not component:
        return mongo_dao.get_all_current_functions(project)
    if type(component) in [dict, OrderedDict]:
        component = component['name']
    return mongo_dao.get_functions_for_component(project, component=component)


def get_functions_from_filesystem(profile, scope=None):
    """Grabs the function definition, then uses the definition to make records
    from the specified function records file. Uses a specified profile to change
    keywords into absolute paths. Returns a 1D array of Function named tuples.
    """
    header = 'function'
    if scope:
        header = scope + '_function'
    function_tuples = generic_processor.get_records_from_filesystem(header,
                                                                    "metadata",
                                                                    profile=profile)
    return function_tuples


def make_functions_from_tuples(function_tuples):
    """Takes a list of function named tuples and transforms them into a list of
    function dictionary objects.
    """
    add_date = utils.get_timestamp()
    function_maker = function_model.named_tuple_to_function_closure(add_date)
    functions = list(map(function_maker, function_tuples))
    return functions


def create_external_functions(component, functions, source='filesystem', profile=None):
    """The list version of add_expressions_to_function, calls the single version
    for a passed list of dictionary function objects. Updates the external function,
    adding a function output object from the external expressions.
    """
    expression_retrieval_tool = external_processor.add_expressions_to_external_function_closure(component,
                                                                                                source=source,
                                                                                                profile=profile)
    external_functions = list(map(expression_retrieval_tool, functions))
    external_functions = list(map(external_processor.update_external_function_parameters, functions))
    return external_functions


def create_compound_functions(component, compound_functions, source='filesystem', profile=None,
                              external_functions=None, internal_functions=None):
    """This method builds compound functions and compile their child functions.
    Calls a recursive function to assemble inputs/intermediates/outputs from all child functions
    and their potential children.
    Returns a list of complete compound function dictionary objects.
    """
    subfunctions = compound_processor.get_subfunctions_for_component(component['name'],
                                                                     source=source,
                                                                     profile=profile)
    compound_functions = compound_processor.add_subfunctions_to_compound_functions(compound_functions, subfunctions)
    compound_functions = list(map(compound_processor.order_function_subfunctions, compound_functions))
    full_function_list = utils.merge_lists([compound_functions, external_functions, internal_functions])
    subfunction_type_assigner = compound_processor.assign_subfunction_type_closure(full_function_list)
    compound_functions = list(map(subfunction_type_assigner, compound_functions))
    compound_functions = compound_processor.assign_complexity_to_compound_functions(compound_functions)
    compound_functions = compound_processor.add_parameters_to_compound_functions(compound_functions,
                                                                                 external_functions=external_functions,
                                                                                 internal_functions=internal_functions)
    return compound_functions


def create_internal_functions(component, functions, source='filesystem', profile=None):
    """This method builds internal functions.
    Returns a list of complete internal function dictionary objects.
    """
#    internal_functions = internal_processor.get_internal_functions_for_component(component['name'],
#                                                                                 source=source,
#                                                                                 profile=profile)
#    return internal_functions
    return functions


def function_filter(function, scope):
    """The generic function filter, takes a function and a type and returns the function
    if it is of that type.
    """
    if function['scope'] == scope:
        return True
    return False


def internal_function_filter(function):
    """Returns a function if it is internal.
    (Internal functions are non-container functions that represent one to one mappings
    with methods internal to a particular component,
    calling some specified internal or external method with the attached parameters).
    """
    if function_filter(function, 'internal'):
        return function


def compound_function_filter(function):
    """Returns a function if it is compound.
    (Compound functions are functions made of other functions).
    """
    if function_filter(function, 'compound'):
        return function


def external_function_filter(function):
    """Returns a function if it is external.
    (External functions are functions made of expressions).
    """
    if function_filter(function, 'external'):
        return function


def function_id_filter(function):
    """Filters a function, only returning the id of the function.
    """
    return function['_id']


def get_functions_for_component_closure(project, source='filesystem', profile=None, scope=None):
    """Closure function for getting functions for components, allowing the function to be
    mapped to multiple similar components.
    """
    def get_functions_for_component(component):
        """This method gathers all functions associated with a particular
        component. Defaults to gather functions from a filesystem. If gathering from a filesystem,
        the profile is required if the filesystem source contains relative paths.
        """
        if source == 'filesystem':
            functions = get_component_functions_from_filesystem(project, component, profile, scope=scope)
        elif source == 'database':
            functions = get_current_functions(project, component)
            functions = list(map(function_id_filter, functions))
        return functions

    return get_functions_for_component


def get_component_functions_from_filesystem(project, component, profile, scope=None):
    """Accepts a component dictionary object and a profile string and assembles
    complete function dictionary objects, and returns the objects as a list.
    """
    function_tuples = get_functions_from_filesystem(profile, scope=scope)
    function_tuples = [function_tuple for function_tuple in function_tuples
                       if function_tuple.component == component['name']]
    functions = make_functions_from_tuples(function_tuples)
    functions = add_function_parameters(component, functions, profile=profile)
    external_functions = list(filter(external_function_filter, functions))
    compound_functions = list(filter(compound_function_filter, functions))
    internal_functions = list(filter(internal_function_filter, functions))
    if internal_functions:
        internal_functions = create_internal_functions(component, internal_functions,
                                                       source='filesystem', profile=profile)
    if external_functions:
        external_functions = create_external_functions(component, external_functions,
                                                       source='filesystem', profile=profile)
    if compound_functions:
        compound_functions = create_compound_functions(component, compound_functions,
                                                       source='filesystem', profile=profile,
                                                       external_functions=external_functions,
                                                       internal_functions=internal_functions)
    functions = external_functions + compound_functions + internal_functions
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    functions = mongo_dao.add_functions(project, functions)
    return functions


def create_functions_from_filesystem(project_id, function_type=None, profile=None):
    """Creates a set of functions from a filesystem. Uses the header/records pattern.
    Requres a project id and a component. Stores the function collection in the database.
    Returns the newly created set of functions.
    """
    return


def make_functions_from_metadata(profile):
    """The test function/overall function for grabbing functions from a metadata(filesystem)
    source.
    """
    function_tuples = get_functions_from_filesystem(profile)
    functions = make_functions_from_tuples(function_tuples)
    return functions


if __name__ == '__main__':
    print('Please use function processor module as method package.')
