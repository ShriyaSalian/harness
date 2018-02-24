from python_commons import utils


def add_evaluation_name(evaluation, evaluation_name):
    """Adds the given name to the given evaluation, returning the updated evaluation.
    """
    evaluation['name'] = evaluation_name
    return evaluation


def order_inputs(inputs):
    ordered_inputs = utils.sort_dictionary_list_on_key(inputs, 'order')
    return ordered_inputs


def update_evaluation_functions(evaluation, evaluation_functions):
    """Updates the evaluation functions, returning the updated evaluation record.
    Cleans up the functions and also updates the evaluation info object depending
    on the final status.
    """
    success = True
    runtime = 0
    evaluation['functions'] = evaluation_functions
    for function in evaluation_functions:
        runtime += function['time']
        if not function['success']:
            success = False
    evaluation['info']['success'] = success
    evaluation['info']['time'] = runtime
    return evaluation


def update_evaluation_record(evaluation, record):
    """Updates the evaluation record reference.
    """
    evaluation['record'] = record['_id']
    return evaluation


def make_evaluation_function(function, info):
    """Prepares and returns a function ready for addition to the evaluation metadata.
    """
    evaluation_function = {}
    evaluation_function['name'] = function['function']
    evaluation_function['id'] = function['id']
    evaluation_function['order'] = function['order']
    evaluation_function['time'] = info['runtime']
    evaluation_function['success'] = info['success']
    return evaluation_function


def make_evaluation_closure(workflow, template, add_date=utils.get_timestamp()):
    """Creates an evaluation record for database entry.
    """
    def make_evaluation(evaluation=None):
        if not evaluation:
            evaluation = {}
            add_blank_name(evaluation)
            add_blank_description(evaluation)
        add_dates(evaluation)
        add_workflow(evaluation)
        add_structure(evaluation)
        add_collection(evaluation)
        add_fields(evaluation)
        add_functions(evaluation)
        add_info(evaluation)
        add_record(evaluation)
        return evaluation

    def add_dates(evaluation):
        evaluation['add_date'] = add_date

    def add_blank_name(evaluation):
        evaluation['name'] = 'None'

    def add_blank_description(evaluation):
        evaluation['description'] = 'None'

    def add_workflow(evaluation):
        evaluation['workflow'] = workflow['name']

    def add_structure(evaluation):
        evaluation['structure'] = workflow['structure']

    def add_collection(evaluation):
        evaluation['template'] = template['name']
        evaluation['collection'] = template['collection']

    def add_fields(evaluation):
        if 'fields' in list(template.keys()):
            evaluation['fields'] = get_evaluation_fields(template)
        else:
            evaluation['fields'] = []

    def add_info(evaluation):
        evaluation['info'] = {}
        evaluation['info']['success'] = False
        evaluation['info']['time'] = None

    def add_functions(evaluation):
        evaluation['functions'] = []

    def add_record(evaluation):
        evaluation['record'] = None

    return make_evaluation


def get_evaluation_fields(template):
    """Prepares and returns template fields for attachment on an evaluation record.
    """
    evaluation_fields = [{'name': field['name'], 'type': field['type']} for field in template['fields']]
    return evaluation_fields


def parse_module_name_from_path(function_path, extension='.py'):
    """Returns the module name from a given path.
    """
    if function_path.endswith(extension):
        path_parts = function_path.split('/')
        module_path = path_parts[-1]
        module = module_path.rstrip(extension)
        return module
    return None


def get_location_path(function_path, component_path, module_name, extension='.py'):
    """Combines a component path (base path) to the function path (specific path)
    to return the specific location for a module.
    """
    if function_path.endswith(extension):
        target_path = function_path.rstrip(module_name + extension)
    full_path = '/'.join([component_path, target_path])
    if full_path.endswith('/'):
        full_path = full_path.rstrip('/')
    return full_path


def prepare_function_output(function):
    """Returns an output for use in function evaluation.
    """
    if 'outputs' in list(function.keys()):
        output = {}
        if function['outputs']:
            if function['outputs'][0]:
                output['name'] = function['outputs'][0]['name']
                return output
    return None


def prepare_function_input(function):
    """Returns an input dictionary for use in function evaluation.
    """
    if 'inputs' in list(function.keys()):
        inputs = {}
        if function['inputs']:
            ordered_inputs = order_inputs(function['inputs'])
            for inpt in ordered_inputs:
                if 'source' in list(inpt.keys()):
                    if inpt['source']:
                        if 'source' in list(inpt['source'].keys()):
                            if inpt['source']['source'] == 'direct':
                                inputs[int(inpt['order'])] = inpt['source']['value']
                                if inpt['source']['type'] == 'string':
                                    inputs[int(inpt['order'])] = str(inputs[int(inpt['order'])])
                                elif inpt['source']['type'] == 'integer':
                                    inputs[int(inpt['order'])] = int(inputs[int(inpt['order'])])
                            elif inpt['source']['source'] == 'function':
                                inputs[int(inpt['order'])] = {}
                                inputs[int(inpt['order'])]['parameter'] = inpt['source']['parameter']
                                inputs[int(inpt['order'])]['function'] = inpt['source']['workflow_id']
                                inputs[int(inpt['order'])]['type'] = inpt['source']['source_type']
                            elif inpt['source']['source'] == 'evaluation':
                                inputs[int(inpt['order'])] = {}
                                if inpt['source']['type'] == 'named':
                                    inputs[int(inpt['order'])]['type'] = 'named'
                                    inputs[int(inpt['order'])]['evaluation'] = inpt['source']['name']
                                    inputs[int(inpt['order'])]['parameter'] = inpt['source']['parameter']
                                    inputs[int(inpt['order'])]['workflow'] = inpt['source']['workflow']
                                elif inpt['source']['type'] == 'last':
                                    inputs[int(inpt['order'])]['type'] = 'last'
                                    inputs[int(inpt['order'])]['evaluation'] = None
                                    inputs[int(inpt['order'])]['parameter'] = inpt['source']['parameter']
                                    inputs[int(inpt['order'])]['workflow'] = inpt['source']['workflow']
    return inputs


def prepare_functions_for_evaluation_closure(project, workflow):
    """Prepares a function for its specific type of evaluation.
    """
    def prepare_functions_for_evaluation(function):
        if function['definition']['scope'] == 'internal':
            return prepare_internal(function)

    def prepare_internal(function):
        if function['definition']['language'] == 'python':
            return prepare_python(function)

    def prepare_python(function):
        if function['definition']['type'] == 'method':
            return prepare_python_method(function)

    def prepare_python_method(function):
        prepared = {}
        prepared['order'] = function['order']
        prepared['id'] = function['function']
        prepared['unique_id'] = function['unique_id']
        prepared['includes'] = []
        prepared['scope'] = 'internal'
        prepared['language'] = 'python'
        prepared['language_version'] = function['definition']['language_version']
        prepared['type'] = 'method'
        prepared['inputs'] = prepare_function_input(function)
        prepared['output'] = prepare_function_output(function)
        prepared['function'] = function['definition']['function']
        prepared['module'] = parse_module_name_from_path(function['definition']['location'])
        prepared['location'] = get_location_path(function['definition']['location'],
                                                 function['component']['location'],
                                                 prepared['module'])
        prepared['includes'].append(prepared['location'])
        return prepared

    return prepare_functions_for_evaluation

if __name__ == '__main__':
    print('Please use evaluation model module as method package.')
