import harness.src.main.processor.workflow_processor as workflow_processor
import harness.src.main.processor.workflow_function_processor as workflow_function_processor
import harness.src.main.processor.workflow_parameter_processor as parameter_processor
import harness.src.test.processor.evaluation_processor_test as evaluation_test


def test_updating_workflow_function_parameter(project, workflow):
    """Tests updating workflow function parameters for various test scenarios.
    """
    print('workflow: ')
    print(workflow)
    print('')
    functions = workflow['functions']
    if workflow['name'] == 'get_coordinate_multiple':
        target_1 = {}
        target_1['type'] = 'Coordinate.default'
        target_1['name'] = 'output_coordinate_1'
        function_1 = functions[0]
        parameter_1 = 'coordinate'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function_1, parameter_1,
                                                                     target_1)
        target_2 = {}
        target_2['type'] = 'Coordinate.default'
        target_2['name'] = 'output_coordinate_2'
        function_2 = functions[1]
        parameter_2 = 'coordinate'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function_2, parameter_2,
                                                                     target_2)
    elif workflow['name'] == 'get_coordinate':
        new_target = {}
        new_target['type'] = 'Coordinate.default'
        new_target['name'] = 'output_coordinate'
        parameter = 'coordinate'
        function = functions[0]
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     new_target)
    elif workflow['name'] == 'test_unchained':
        function = functions[2]
        parameter = 'lower_bound'
        source = {}
        source['source'] = 'direct'
        source['type'] = 'integer'
        source['value'] = 1
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'lower_bound'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        parameter = 'upper_bound'
        source = {}
        source['source'] = 'direct'
        source['type'] = 'integer'
        source['value'] = 500
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'upper_bound'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        function = functions[0]
        parameter = 'month_index'
        source = {}
        source['source'] = 'direct'
        source['type'] = 'integer'
        source['value'] = 5
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'month_index'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        function = functions[2]
        parameter = 'random_integer'
        target = {}
        target['name'] = 'random_integer'
        target['type'] = 'integer'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
        function = functions[0]
        parameter = 'month'
        target = {}
        target['name'] = 'month'
        target['type'] = 'string'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
        function = functions[1]
        parameter = 'coordinate'
        target = {}
        target['name'] = 'random_coordinate'
        target['type'] = 'Coordinate.default'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
    elif workflow['name'] == 'test_chained':
        print('testing chained workflow')
        function = functions[1]
        parameter = 'lower_bound'
        source = {}
        source['source'] = 'direct'
        source['type'] = 'integer'
        source['value'] = 1
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'lower_bound'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        parameter = 'upper_bound'
        source = {}
        source['source'] = 'direct'
        source['type'] = 'integer'
        source['value'] = 12
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'upper_bound'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        function = functions[0]
        parameter = 'month_index'
        source = {}
        source['source'] = 'function'
        source['source_id'] = functions[1]['function']
        source['workflow_id'] = functions[1]['unique_id']
        source['parameter'] = 'random_integer'
        source['source_type'] = 'output'
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'month_index'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        function = functions[1]
        parameter = 'random_integer'
        target = {}
        target['name'] = 'random_integer'
        target['type'] = 'integer'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
        function = functions[0]
        parameter = 'month'
        target = {}
        target['name'] = 'month'
        target['type'] = 'string'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)

    elif workflow['name'] == 'test_last_evaluation':
        function = functions[0]
        parameter = 'month_index'
        source = {}
        source['source'] = 'evaluation'
        source['type'] = 'last'
        source['workflow'] = 'test_chained'
        source['parameter'] = 'random_integer'
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'month_index'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)

        parameter = 'month'
        target = {}
        target['name'] = 'month'
        target['type'] = 'string'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
    elif workflow['name'] == 'test_named_evaluation':
        function = functions[0]
        parameter = 'month_index'
        source = {}
        source['source'] = 'evaluation'
        source['type'] = 'named'
        source['name'] = 'starred_evaluation'
        source['workflow'] = 'test_chained'
        source['parameter'] = 'random_integer'
        workflow = parameter_processor.update_workflow_input_source(project, workflow,
                                                                    function, parameter,
                                                                    source)
        target = {}
        target['type'] = 'integer'
        target['name'] = 'month_index'
        workflow = parameter_processor.update_workflow_input_target(project, workflow,
                                                                    function, parameter,
                                                                    target)
        function = functions[0]
        parameter = 'month'
        target = {}
        target['name'] = 'month'
        target['type'] = 'string'
        workflow = parameter_processor.update_workflow_output_target(project, workflow,
                                                                     function, parameter,
                                                                     target)
    else:
        pass
    return workflow


def test_add_workflow_functions_from_filesystem(project, profile='standard', workflow=None):
    """Tests adding functions from a project to a given workflow.
    """
    functions = workflow_function_processor.get_workflow_functions_from_filesystem(project,
                                                                                   profile=profile,
                                                                                   workflow=workflow)
    print('Functions for test workflow: ')
    print(functions)
    print('')
    workflow = workflow_processor.add_functions_to_workflow(project, workflow, functions)
    return workflow


def test_last_evaluation_workflow(project, profile="standard"):
    """Tests creating evaluations of a workflow using the last evaluation of a workflow.
    """
    test_workflow = workflow_processor.get_workflow(project, workflow_name='test_last_evaluation')
    num_times = 10
    evaluations = evaluation_test.test_make_evaluations(project, test_workflow, count=num_times, profile=profile)
    print('Evaluations: ')
    print(evaluations)
    print('')
    print('')
    print('Getting the records for the evaluations: ')
    records = evaluation_test.test_get_evaluation_records(project, evaluations)
    print('Records: ')
    print(records)
    print('')
    print('')


def test_named_evaluation_workflow(project, profile="standard"):
    """Tests creating evaluations of a workflow that uses a named evaluation of a workflow.
    """
    test_workflow = workflow_processor.get_workflow(project, workflow_name='test_named_evaluation')
    num_times = 10
    evaluations = evaluation_test.test_make_evaluations(project, test_workflow, count=num_times, profile=profile)
    print('Evaluations: ')
    print(evaluations)
    print('')
    print('')
    print('Getting the records for the evaluations: ')
    records = evaluation_test.test_get_evaluation_records(project, evaluations)
    print('Records: ')
    print(records)
    print('')
    print('')


def test_custom_structure_workflow(project, profile="standard"):
    """Tests creating evaluations of a workflow that uses a named evaluation of a workflow.
    """
    test_workflow = workflow_processor.get_workflow(project, workflow_name='get_coordinate_multiple')
    num_times = 10
    evaluations = evaluation_test.test_make_evaluations(project, test_workflow, count=num_times, profile=profile)
    print('Evaluations: ')
    print(evaluations)
    print('')
    print('')
    print('Getting the records for the evaluations: ')
    records = evaluation_test.test_get_evaluation_records(project, evaluations)
    print('Records: ')
    print(records)
    print('')
    print('')
    return records


def test_get_workflow(project, workflow_name):
    """Gets a workflow by the name and project.
    """
    return workflow_processor.get_workflow(project, workflow_name=workflow_name)


def test_add_workflows_from_filesystem(project, profile=None):
    """Tests adding the workflows to a given filesystem.
    Also adds functions to the workflows.
    """
    print('Current workflows: ')
    print(workflow_processor.get_current_workflows(project))
    print('')
    print('')
    workflow_processor.remove_workflow_collection(project)
    print('Workflows after removal: ')
    print(workflow_processor.get_current_workflows(project))
    print('')
    print('')
    workflows = workflow_processor.create_workflows_from_metadata(project, profile=profile)
    print('Workflows loaded from filesystem: ')
    print(workflows)
    test_workflow = workflows[0]
    print('Testing workflow: ')
    print(test_workflow)
    print('')
    print('')
    test_workflows = []
    print('Adding functions to all the workflows: ')
    for workflow in workflows:
        print('workflow: ')
        print(workflow)
        print('')
        test_workflows.append(test_add_workflow_functions_from_filesystem(project, profile=profile, workflow=workflow))
    new_workflows = []
    for workflow in test_workflows:
        new_workflows.append(test_updating_workflow_function_parameter(project, workflow))
    return new_workflows


if __name__ == '__main__':
    print('Please use workflow processor test as test package.')
