from . import generic_processor
import harness.src.main.model.workflow_function_model as workflow_function_model
import harness.src.main.model.function_model as function_model
import harness.src.main.dao.mongo.function_dao as function_dao
from collections import OrderedDict


def get_function_from_database_closure(project):
    """Returns a database function. Either returns what is passed in or grabs
    the function from the database first if the function doesnt have an id tag.
    """

    def get_function_from_database(function):
        function_id = function_model.get_function_id(function)
        if function_id:
            return function
        else:
            if type(project) in [dict, OrderedDict]:
                database = project['database']
                fcn = function_dao.get_current_function_by_name(database, function['function'])
            else:
                fcn = function_dao.get_current_function_by_name(project, function['function'])
            if 'order' in list(function.keys()):
                fcn['order'] = int(function['order'])
            return fcn

    return get_function_from_database


def workflow_filter_closure(workflow):
    """Closure for simple filter.
    Returns a function if it belongs to the specific workflow.
    """
    def workflow_filter(workflow_function):
        """Should handle multiple workflow cases.
        """
        if workflow_function['workflow'] == workflow:
            return workflow_function

    return workflow_filter


def make_workflow_functions_from_tuples(workflow_function_tuples, workflow=None):
    """Takes workflow function named tuples and returns them as a list of dictionaries.
    """
    function_maker = workflow_function_model.named_tuple_to_workflow_function_closure()
    workflow_functions = list(map(function_maker, workflow_function_tuples))
    if workflow:
        if type(workflow) in [dict, OrderedDict]:
            workflow = workflow['name']
        function_filter = workflow_filter_closure(workflow)
        workflow_functions = list(filter(function_filter, workflow_functions))
    workflow_functions = list(map(workflow_function_model.remove_workflow_identifier, workflow_functions))
    return workflow_functions


def get_workflow_functions_from_filesystem(project, workflow=None, profile=None):
    """Grabs the workflow function definition, then uses the definition to make workflow
    function records. Returns a 1D array of workflow function dictionary objects.
    If workflow is specified, filters the functions to only return functions for the
    given workflow.
    """
    header = 'workflow_function'
    workflow_function_tuples = generic_processor.get_records_from_filesystem(header,
                                                                             "metadata",
                                                                             profile=profile)
    workflow_functions = make_workflow_functions_from_tuples(workflow_function_tuples,
                                                             workflow=workflow)
    return workflow_functions


if __name__ == '__main__':
    print('Please use workflow function processor module as method package.')
