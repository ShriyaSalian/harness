from collections import OrderedDict
import harness.src.main.processor.workflow_processor as workflow_processor
import harness.src.main.processor.function_processor as function_processor
import harness.src.main.processor.component_processor as component_processor
import harness.src.main.processor.language_processor as language_processor
import harness.src.main.model.evaluation_model as evaluation_model
import harness.src.main.dao.mongo.evaluation_dao as evaluation_dao
from pythoncommons import general_utils
from mars import mars


def get_ordered_workflow_functions(workflow):
    """Takes a workflow, parsing the functions object, and returns them
    as a list of function objects ordered by their specified order.
    """
    functions = workflow['functions']
    if functions:
        ordered_functions = general_utils.sort_dictionary_list_on_key(functions, 'order')
    return ordered_functions


def add_function_definition_closure(project):
    """Adds a definition to each function that is to be evaluated.
    """
    def add_function_definition(function):
        database = project
        if type(project) in [dict, OrderedDict]:
            database = project['database']
        function_definition = function_processor.get_function_by_id(database, function['function'])
        function['definition'] = function_definition
        return function

    return add_function_definition


def add_component_to_function_closure(project):
    """Adds the relevant component to the passed function.
    """

    def add_component_to_function(function):
        component_name = function['definition']['component']
        component = component_processor.get_current_component_by_name(project, component_name)
        function['component'] = component
        return function

    return add_component_to_function


def add_parameters_to_function_closure(workflow):
    """Adds the inputs and outputs to each function for the workflow.
    """
    def add_parameters_to_function(function):
        function['inputs'] = []
        function['outputs'] = []
        workflow_inputs = workflow['parameters']['inputs']
        workflow_outputs = workflow['parameters']['outputs']
        for workflow_input in workflow_inputs:
            if workflow_input['function_id'] == function['unique_id']:
                function['inputs'].append(workflow_input)
        for workflow_output in workflow_outputs:
            if workflow_output['function_id'] == function['unique_id']:
                function['outputs'].append(workflow_output)
        return function

    return add_parameters_to_function


def prepare_evaluation_record(template):
    """Prepares a record ready for insertion into the given template collection based
    on the template fields.
    """
    record = {}
    if 'fields' in list(template.keys()):
        for field in template['fields']:
            if field['default']:
                record[field['name']] = field['default']
            else:
                record[field['name']] = None
    return record


def validate_data_targets(target, data, add_defaults=True):
    """Validates the output of a function against its target storage. If the
    """
    for element in list(data.keys()):
        data[element] = data[element]
    return data


def update_evaluation_record(record, structures, definitions):
    """Updates the record by substituting the proper definition.
    """
    if type(structures) in [dict, OrderedDict]:
        for structure in list(structures.keys()):
            record[definitions[structure]] = structures[structure]
    return record


def get_evaluation_record(project, evaluation):
    """Returns the evaluation record in the database for the specified project
    and evaluation.
    """
    database = project
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    if type(evaluation) in [dict, OrderedDict]:
        template = evaluation['collection']
        record_id = evaluation['record']
    evaluation_record = mars.record.get_record_by_id(database, template, record_id)
    return evaluation_record


def get_record_translator(functions):
    """Prepares a dictionary for use in translating function fields (inputs or outputs)
    that are meant to be stored into their final storage field in the evaluation record.
    Returns this translator as a nested dictionary where the top level are function ids
    and each function id key has a dictionary set of function_field:record_field
    """
    translator = {}
    for function in functions:
        translator[function['order']] = {}
        for function_input in function['inputs']:
            if function_input['target']:
                translator[function['order']][function_input['name']] = function_input['target']['name']
        for function_output in function['outputs']:
            if function_output['target']:
                translator[function['order']][function_output['name']] = function_output['target']['name']
    return translator


def update_function_inputs(project, workflow, function, evaluation_output, output_dictionary):
    """Updates the inputs for the given function, assembling values from previous
    functions or other sources if necessary, adding them to the evaluation record
    if a target is specified.
    """
    for key in list(function['inputs'].keys()):
        if type(function['inputs'][key]) in [dict, OrderedDict]:
            if 'function' in list(function['inputs'][key].keys()):
                function['inputs'][key] = output_dictionary[function['inputs'][key]['function']]
            elif 'evaluation' in list(function['inputs'][key].keys()):
                function['inputs'][key] = get_evaluation_parameter(project, workflow, function['inputs'][key])
    records = [fcn for fcn in workflow['functions'] if fcn['unique_id'] == function['unique_id']]
    record = records[0]
    input_records = record['inputs']
    for inpt in list(function['inputs'].keys()):
        matches = [i for i in input_records if int(i['order']) == inpt]
        input_record = matches[0]
        if input_record['target']:
            evaluation_output[input_record['target']['name']] = function['inputs'][inpt]
    return function


def get_evaluation_parameter(project, workflow, function_input):
    """Retrieves the value of an evaluation for use in a current workflow evaluation.
    """
    if function_input['evaluation']:
        evaluation = get_workflow_evaluation_by_name(project, function_input['workflow'], function_input['evaluation'])
    else:
        evaluation = get_most_recent_evaluation(project, function_input['workflow'])
    record = get_evaluation_record(project, evaluation)
    return record[function_input['parameter']]


def update_function_output_dictionary(function, output, output_dictionary):
    """Maintains a dictionary of function outputs for use by other functions in the
    case of function chaining.
    """
    output_dictionary[function['unique_id']] = output[function['output']['name']]
    return output_dictionary


def has_inputs(function):
    """Returns True if the function has inputs.
    """
    if 'inputs' in list(function.keys()):
        if function['inputs']:
            return True
    return False


def get_evaluations_by_workflow(project, workflow):
    """Returns all evaluations for a given workflow in the given project.
    """
    database = project
    if type(database) in [dict, OrderedDict]:
        database = project['database']
    if type(workflow) in [dict, OrderedDict]:
        workflow = workflow['name']
    evaluations = evaluation_dao.get_evaluations_by_workflow(database, workflow)
    return evaluations


def get_workflow_evaluation_by_name(project, workflow, name):
    """Returns all evaluations with the given name.
    """
    database = project
    if type(database) in [dict, OrderedDict]:
        database = project['database']
    if type(workflow) in [dict, OrderedDict]:
        workflow = workflow['name']
    evaluations = evaluation_dao.get_workflow_evaluations_by_name(database, workflow, name)
    if type(evaluations) in [list] and len(evaluations) == 1:
        return evaluations[0]
    elif type(evaluations) in [dict, OrderedDict]:
        return evaluations
    return None


def get_most_recent_evaluation(project, workflow):
    """Returns the most recent evaluation for the given workflow.
    """
    database = project
    if type(database) in [dict, OrderedDict]:
        database = project['database']
    if type(workflow) in [dict, OrderedDict]:
        workflow = workflow['name']
    evaluations = evaluation_dao.get_evaluations_by_workflow(database, workflow)
    if type(evaluations) in [list] and len(evaluations) == 1:
        return evaluations[0]
    elif type(evaluations) in [list]:
        return evaluations[-1]
    elif type(evaluations) in [dict, OrderedDict]:
        return evaluations
    return None


def get_evaluation_by_id(project, evaluation_id):
    """Returns the evaluation for the given id.
    """
    evaluation = evaluation_dao.get_evaluation_by_id(project, evaluation_id)
    return evaluation


def add_evaluation_name(project, evaluation, evaluation_name):
    """Adds a name to the given evaluation. If the evaluation has an _id, the
    evaluation record is updated in the database.
    """
    evaluation = evaluation_model.add_evaluation_name(evaluation, evaluation_name)
    if '_id' in list(evaluation.keys()):
        database = project
        if type(database) in [dict, OrderedDict]:
            database = project['database']
        evaluation = evaluation_dao.update_evaluation(database, evaluation, changes=['name'])
    return evaluation


def get_ordered_evaluation_functions(project, workflow):
    """
    """
    ordered_functions = get_ordered_workflow_functions(workflow)
    parameter_adder = add_parameters_to_function_closure(workflow)
    ordered_functions = list(map(parameter_adder, ordered_functions))
    # record_translator = get_record_translator(ordered_functions)
    definition_adder = add_function_definition_closure(project)
    ordered_functions = list(map(definition_adder, ordered_functions))
    component_adder = add_component_to_function_closure(project)
    ordered_functions = list(map(component_adder, ordered_functions))
    return ordered_functions


def get_prepared_evaluation_functions(project, workflow, ordered_functions):
    """
    """
    function_preparer = evaluation_model.prepare_functions_for_evaluation_closure(project, workflow)
    prepared_functions = list(map(function_preparer, ordered_functions))
    return prepared_functions


def create_evaluation(project, workflow, evaluation=None, profile="standard"):
    """The basic method for creating an evaluation (evaluating a workflow).
    """
    output_dictionary = {}
    database = project
    if type(database) in [dict, OrderedDict]:
        database = database['database']
    if type(workflow) not in [dict, OrderedDict]:
        workflow = workflow_processor.get_workflow(database, workflow_name=workflow)
    structure = workflow_processor.get_workflow_structure_name(workflow)
    template = workflow_processor.get_workflow_template(database, structure)
    record = prepare_evaluation_record(template)
    evaluation_maker = evaluation_model.make_evaluation_closure(workflow, template)
    evaluation = evaluation_maker(evaluation)
    evaluation = evaluation_dao.add_evaluation(database, evaluation)
    ordered_functions = get_ordered_evaluation_functions(project, workflow)
    record_translator = get_record_translator(ordered_functions)
    prepared_functions = get_prepared_evaluation_functions(project, workflow, ordered_functions)
    evaluation_functions = []
    for function in prepared_functions:
        if has_inputs(function):
            function = update_function_inputs(project, workflow, function, record, output_dictionary)
        result = language_processor.route_function(project, function, profile=profile)
        function['output'] = function['hold_output']
        if validate_data_targets(function, result['output']):
            record = update_evaluation_record(record, result['output'],
                                              record_translator[function['order']])
            output_dictionary = update_function_output_dictionary(function, result['output'], output_dictionary)
        evaluation_functions.append(evaluation_model.make_evaluation_function(function, result['info']))
    evaluation = evaluation_model.update_evaluation_functions(evaluation, evaluation_functions)
    record = mars.record.add_new_record(database, template, record)
    evaluation = evaluation_model.update_evaluation_record(evaluation, record)
    evaluation = evaluation_dao.update_evaluation(database, evaluation,
                                                  changes=['functions', 'record', 'info'])
    return evaluation


if __name__ == '__main__':
    print('Please use evaluation processor as method package.')
