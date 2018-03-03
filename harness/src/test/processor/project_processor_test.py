import harness.src.main.processor.project_processor as project_processor
import harness.src.main.processor.parameter_processor as parameter_processor
import harness.src.main.processor.generic_processor as generic_processor
import harness.src.main.processor.component_processor as component_processor
import harness.src.main.processor.function_processor as function_processor
import harness.src.test.processor.workflow_processor_test as workflow_test
import harness.src.test.processor.evaluation_processor_test as evaluation_test
import harness.src.test.processor.function_processor_test as function_test
from collections import OrderedDict
import sys


def test_print_function(project_name='py_common'):
    """Simple test function to test removing, adding, disabling, enabling components.
    """
    project = project_processor.get_project_for_testing(project_name)
    print('Testing component actions on project: ', project['name'])
    print('All components: ')
    print(project_processor.get_all_components(project=project))
    print('Current components: ')
    print(project_processor.get_current_components(project=project))
    print('Current enabled components: ')
    print(component_processor.get_enabled_components(project['database']))
    print('Current disabled components: ')
    print(component_processor.get_disabled_components(project['database']))
    print('Current vcs enabled components: ')
    print(component_processor.get_vcs_enabled_components(project['database']))
    print('Current vcs disabled components: ')
    print(component_processor.get_vcs_disabled_components(project['database']))
    print('Current removed components: ')
    print(component_processor.get_removed_components(project['database']))


def update_component_status_test_function(test_project):
    """Tests updating the components.
    """
    component_one = 'py_common'
    component_two = 'ghcn_data'
    database = test_project['database']
    component_disabler = component_processor.disable_component_closure(database,
                                                                       parameter='name')
    component_enabler = component_processor.enable_component_closure(database,
                                                                     parameter='name')
    vcs_disabler = component_processor.disable_vcs_closure(database,
                                                           parameter='name')
    vcs_enabler = component_processor.enable_vcs_closure(database,
                                                         parameter='name')
#    component_remover = component_processor.remove_component_closure(database,
#                                                                     parameter='name')
#    component_adder = component_processor.add_component_closure(project, parameter='id')
#    print 'Disabling component: ', 'ghcn_data'
    component_disabler(component_one)
#    print 'Got component: '
#    print component
#    print 'Disabling component vcs for: ', 'py_common'
    vcs_disabler(component_two)
#    print 'Got component: '
#    print component
#    print 'Enabling component: ', 'py_common'
    component_enabler(component_two)
#    print 'Enabling vcs component: ', 'ghcn_data'
    vcs_enabler(component_one)


def component_updater_test_function(project_name='py_common'):
    project = project_processor.get_project_for_testing(project_name)
    print('project: ')
    print(project)
    new_components = project_processor.update_project_components_from_vcs(project=project)
    print('New components: ')
    print(new_components)
    return


def reset_projects_with_components(profile='standard'):
    """Resets projects (removes any projects that it finds in the system) and
    subsequently recreates from the filesystem for the specified profile.
    """
    all_projects = project_processor.get_all_projects()
    print('All projects in mongo: ')
    print(all_projects)
    print("First removing all projects")
    project_processor.remove_all_projects()
    all_projects = project_processor.get_all_projects()
    if not all_projects:
        print("Successfully removed all projects")
    print("Making projects from filesystem")
    project_processor.make_projects_from_metadata(profile=profile)
    all_projects = project_processor.get_all_projects()
    print('All projects in mongo: ')
    print(all_projects)
    return all_projects


def get_profile_dictionary(profile='standard'):
    """Assembles a complete profile dictionary.
    """
    dictionary = generic_processor.get_fully_qualified_profile_from_filesystem(profile)
    return dictionary


def perform_fresh_filesystem_setup(profile='standard'):
    """Test function to blow away all project data and recreate from filesystem.
    """
    profile_dictionary = get_profile_dictionary(profile=profile)
    print('Testing for profile: ')
    print(profile_dictionary)
    print('')
    print('')
    reset_projects_with_components(profile=profile)
    project = project_processor.get_project_by_name('py_common')
    print('Test project: ')
    print(project)
    print('')
    print('')
    components = component_processor.get_all_components(project['database'])
    print('Components:')
    print(components)
    print('')
    print('')
    component = components[0]
    print('Test component: ')
    print(component)
    print('')
    print('')
    print('all functions before entry: ')
    print(function_processor.get_current_functions(project))
    print('')
    print('')
    function_getter = function_processor.get_functions_for_component_closure(project, profile=profile, scope='internal')
    for component in components:
        functions = function_getter(component)
        print('functions: ')
        print(functions)
        print('')
        print('')
    function_adder = component_processor.add_functions_to_component_closure(project, source='database', profile=profile)
    components = list(map(function_adder, components))
    print('updated components: ')
    print(components)
    print('')
    print('')
    print('')
    print('Setting up structures: ')
    add_parameters_to_test_project(profile, project=project, dictionary=profile_dictionary)
    print('')
    print('')
    print('')
    print('Setting up the test workflows: ')
    test_workflow_setup(project, profile=profile)
    test_workflow = workflow_test.test_get_workflow(project, workflow_name='test_chained')
    print('The test workflow: ')
    print(test_workflow)
    print('')
    print('')
    print('Testing evaluation of workflow multiple times: ')
    number_times = 10
    evaluations = evaluation_test.test_make_evaluations(project, test_workflow, count=number_times)
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
    print('Adding a name to one of the evaluations to test: ')
    evaluation = evaluation_test.test_add_evaluation_name(project, test_workflow, 'starred_evaluation')
    print('Evaluation: ')
    print(evaluation)
    print('')
    print('')
    print('Testing evaluation of a workflow that is dependent on the last evaluation of another workflow: ')
    workflow_test.test_last_evaluation_workflow(project)
    print('')
    print('')
    print('Testing evaluation of a workflow that is dependent on a named evaluation: ')
    workflow_test.test_named_evaluation_workflow(project)
    print('')
    print('')
    print('Testing an evaluation with a custom structure: ')
    test_records = workflow_test.test_custom_structure_workflow(project)
    print('')
    print('')
    return test_records


def add_parameters_to_test_project(profile, project='py_common', dictionary=None):
    if type(project) not in [dict, OrderedDict]:
        project = project_processor.get_project_by_name(project_name=project)
    print('project: ')
    print(project)
    print('')
    print('')
    project_profile = generic_processor.get_fully_qualified_profile_from_filesystem(profile)
    profile_path = project_profile['profiles'] + '/' + profile
    setup = parameter_processor.add_parameters_to_project_from_filesystem(profile_path, project, full_path=True, profile_name=profile, profile_dictionary=dictionary)
    print('mars profile: ')
    print(setup['profile'])
    print('')
    print('mars structures: ')
    print(setup['structures'])
    print('')
    print('mars templates: ')
    print(setup['templates'])
    print('')
    print('mars translators: ')
    print(setup['translators'])
    print('')


def test_get_parameter_tree(project_name='py_common'):
    """Should return the parameter set as a tree for the given project.
    """
    project = project_processor.get_project_by_name(project_name=project_name)
    parameter = parameter_processor.get_parameter_tree(project['database'])
    print(parameter)
    return parameter


def test_get_components(project_name='py_common'):
    """Should return the components that are part of a given project.
    """
    project = project_processor.get_project_by_name(project_name)
    test_components = project_processor.get_all_components(project=project)
    print('py_common components: ')
    print(test_components)
    print('')
    return project


def test_add_function(project_name='py_common', component_name='py_common'):
    """Tests adding new functions to the test project.
    """
    function = None
    project = project_processor.get_project_by_name(project_name)
    component = component_processor.get_current_component_by_name(project['database'], component_name)
    function = function_test.test_create_new_function(project, component, function)
    return function


def test_workflow_setup(project, profile="standard"):
    """Workflow tests relating to the test project.
    """
    if type(project) not in [dict, OrderedDict]:
        project = project_processor.get_project_by_name(project)
    test_workflows = workflow_test.test_add_workflows_from_filesystem(project, profile=profile)
    return test_workflows


if __name__ == '__main__':
    print('Running main routine of project processor test')
    x = None
    try:
        x = sys.argv[1]
    except IndexError:
        pass
    if x:
        perform_fresh_filesystem_setup(profile=x)
    else:
        perform_fresh_filesystem_setup()
    print('End of test')
