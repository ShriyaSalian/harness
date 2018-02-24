from pythoncommons import utils
import harness.src.main.model.function_model as function_model
import harness.src.main.model.function_parameter_model as function_parameter_model
import harness.src.main.model.workflow_parameter_model as workflow_parameter_model


def make_workflow_structure(workflow):
    """Creates and returns a new structure for use in structure storage.
    """
    structure = {}
    structure['group'] = 'workflow'
    structure['name'] = workflow['name'] + '_' + utils.get_random_string()
    structure['description'] = 'The storage collection for the {0} workflow.'.format(workflow['name'])
    return structure


def add_workflow_structure(workflow, structure):
    workflow['structure'] = structure['name']
    return workflow


def get_workflow_structure(workflow):
    """Returns the structure for the given workflow.
    """
    return workflow['structure']


def get_workflow_functions(workflow):
    """Returns the functions object for a given workflow.
    """
    return workflow['functions']


def get_workflow_parameters(workflow):
    """Returns the parameters object for a given workflow.
    """
    return workflow['parameters']


def get_workflow_inputs(workflow):
    """Returns the inputs object for a given workflow.
    """
    parameters = get_workflow_parameters(workflow)
    return parameters['inputs']


def get_workflow_outputs(workflow):
    """Returns the outputs for a given workflow.
    """
    parameters = get_workflow_parameters(workflow)
    return parameters['outputs']


def add_workflow_function(workflow, function):
    """Updates the workflow by adding the passed function. Returns the workflow.
    """
    workflow_functions = get_workflow_functions(workflow)
    workflow_function_count = len(workflow_functions)
    new_workflow_function = {}
    new_workflow_function['function'] = function_model.get_function_id(function)
    if 'order' in list(function.keys()):
        new_workflow_function['order'] = int(function['order'])
    else:
        new_workflow_function['order'] = workflow_function_count
    new_workflow_function['unique_id'] = function_model.get_unique_id(function)
    workflow_functions.append(new_workflow_function)
    return workflow


def add_workflow_inputs(workflow, inputs):
    """Updates the workflow by adding the passed inputs. Returns the workflow.
    """
    workflow_inputs = get_workflow_inputs(workflow)
    workflow_inputs += inputs
    return workflow


def add_workflow_outputs(workflow, outputs):
    """Updates the workflow by adding the passed outputs. Returns the workflow.
    """
    workflow_outputs = get_workflow_outputs(workflow)
    workflow_outputs += outputs
    return workflow


def make_new_workflow_input_closure(function):

    def make_new_workflow_input(function_input):
        """Creates a new workflow input for the given function input.
        """
        workflow_input = {}
        workflow_input['function'] = function_model.get_function_id(function)
        workflow_input['function_id'] = function_model.get_unique_id(function)
        workflow_input['name'] = function_input['name']
        workflow_input['description'] = function_input['description']
        workflow_input['order'] = function_input['order']
        workflow_input['source'] = workflow_parameter_model.make_new_workflow_parameter_source()
        workflow_input['target'] = workflow_parameter_model.make_new_workflow_parameter_target()
        return workflow_input

    return make_new_workflow_input


def make_new_workflow_output_closure(function):

    def make_new_workflow_output(function_output):
        """Creates a new workflow output for the given function output.
        """
        workflow_output = {}
        workflow_output['function'] = function_model.get_function_id(function)
        workflow_output['function_id'] = function_model.get_unique_id(function)
        workflow_output['name'] = function_output['name']
        workflow_output['description'] = function_output['description']
        workflow_output['target'] = workflow_parameter_model.make_new_workflow_parameter_target()
        return workflow_output

    return make_new_workflow_output


def add_function_to_workflow(workflow, function):
    """Adds the given function to the given workflow.
    """
    function = function_model.add_unique_id(function)
    function_parameters = function_model.get_function_parameters(function)
    function_inputs = function_parameter_model.get_inputs(function_parameters)
    function_outputs = function_parameter_model.get_outputs(function_parameters)
    input_maker = make_new_workflow_input_closure(function)
    output_maker = make_new_workflow_output_closure(function)
    new_inputs = list(map(input_maker, function_inputs))
    new_outputs = list(map(output_maker, function_outputs))
    workflow = add_workflow_function(workflow, function)
    workflow = add_workflow_inputs(workflow, new_inputs)
    workflow = add_workflow_outputs(workflow, new_outputs)
    return workflow


def named_tuple_to_workflow_closure(add_date=utils.get_timestamp()):
    """Takes a named tuple workflow object and transforms it into the dictionary
    version, removing extraneous identifiers and including metadata.
    """

    def named_tuple_to_workflow(workflow_tuple):
        workflow = workflow_tuple._asdict()
        add_dates(workflow)
        add_empty_storage(workflow)
        add_empty_function_collection(workflow)
        add_empty_parameter_collection(workflow)
        remove_identifiers(workflow)
        del workflow_tuple
        return workflow

    def add_dates(workflow):
        workflow['add_date'] = add_date
        workflow['remove_date'] = None

    def add_empty_storage(workflow):
        workflow['structure'] = None

    def add_empty_function_collection(workflow):
        workflow['functions'] = []

    def add_empty_parameter_collection(workflow):
        workflow['parameters'] = {}
        workflow['parameters']['inputs'] = []
        workflow['parameters']['outputs'] = []

    def remove_identifiers(workflow):
        identifiers = ['project']
        utils.remove_dictionary_keys(workflow, identifiers)

    return named_tuple_to_workflow

if __name__ == '__main__':
    print('Please use workflow model module as method package.')
