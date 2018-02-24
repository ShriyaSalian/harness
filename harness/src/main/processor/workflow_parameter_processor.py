import harness.src.main.model.workflow_parameter_model as parameter_model
import harness.src.main.model.workflow_model as workflow_model
import harness.src.main.processor.workflow_processor as workflow_processor
# from mars import mars


def get_parameter_source(parameter):
    """Returns the source for the given parameter.
    """
    source = parameter_model.get_parameter_source(parameter)
    return source


def set_parameter_target_structure(parameter, structure, name, translator=None):
    """Sets the parameter target to use the given structure with the given
    name. Optionally sets a translator that will first process the function
    output before storing in the target structure. Returns the updated
    parameter.
    """
    pass


def get_parameter_target(parameter):
    """Returns the target for the given parameter.
    """
    target = parameter_model.get_parameter_target(parameter)
    return target


def get_workflow_parameter(workflow, parameter_name, parameter_type):
    """Returns the workflow parameter by the given name and type for the given
    function. NEED TO ADD FUNCTION DEPENDENCE HERE!
    """
    if parameter_type == 'input':
        parameters = workflow_model.get_workflow_inputs(workflow)
    elif parameter_type == 'output':
        parameters = workflow_model.get_workflow_outputs(workflow)
    for parameter in parameters:
        if parameter['name'] == parameter_name:
            return parameter
    return None


def update_workflow_parameter_source(workflow, parameter, source):
    """Updates the source for the specified parameter to the given source.
    Returns the updated parameter.
    """
    '''parameter = parameter_model.set_parameter_source(source)
    return parameter'''
    return parameter


def check_valid_parameter_target(workflow, parameter, target):
    """Checks the desired parameter target against other current workflow parameters
    to ensure there are no recursive or other conflicts in execution.
    """
    valid = True
    return valid


def check_valid_parameter_source(workflow, parameter, source):
    """Checks the desired parameter source to ensure it is valid.
    """
    valid = True
    return valid


def update_workflow_input_source(project, workflow, function, parameter, source):
    """Updates the source for the specified parameter to the given parameter.
    Returns the updated workflow.
    """
    updated = False
    function_id = function['unique_id']
    inputs = workflow['parameters']['inputs']
    for inpt in inputs:
        if inpt['function_id'] == function_id and inpt['name'] == parameter:
            if check_valid_parameter_source(workflow, parameter, source):
                updated = True
                parameter_model.update_parameter_source(inpt['source'], source)
    if updated:
        workflow = workflow_processor.update_workflow(project, workflow,
                                                      changes=['parameters.inputs'])
    return workflow


def update_workflow_input_target(project, workflow, function, parameter, target):
    """Updates the target for the specified parameter to the given parameter.
    Returns the updated workflow.
    """
    updated = False
    function_id = function['unique_id']
    inputs = workflow['parameters']['inputs']
    for inpt in inputs:
        if inpt['function_id'] == function_id and inpt['name'] == parameter:
            if check_valid_parameter_target(workflow, parameter, target):
                updated = True
                parameter_model.update_parameter_target(inpt['target'], target)
    if updated:
        workflow_processor.update_workflow_template(project, workflow, function,
                                                    parameter, target, 'input')
        workflow = workflow_processor.update_workflow(project, workflow,
                                                      changes=['parameters.inputs'])
    return workflow


def update_workflow_output_target(project, workflow, function, parameter, target):
    """Updates the target for the specified parameter to the given parameter.
    Returns the updated workflow.
    """
    updated = False
    function_id = function['unique_id']
    outputs = workflow['parameters']['outputs']
    for output in outputs:
        if output['function_id'] == function_id and output['name'] == parameter:
            if check_valid_parameter_target(workflow, parameter, target):
                updated = True
                parameter_model.update_parameter_target(output['target'], target)
    if updated:
        workflow_processor.update_workflow_template(project, workflow, function,
                                                    parameter, target, 'output')
        workflow = workflow_processor.update_workflow(project, workflow,
                                                      changes=['parameters.outputs'])
    return workflow


if __name__ == '__main__':
    print('Please use workflow parameter processor module as method package.')
