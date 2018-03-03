from pythoncommons import general_utils
from collections import OrderedDict
import harness.src.main.processor.generic_processor as generic_processor
import harness.src.main.model.workflow_model as workflow_model
import harness.src.main.processor.workflow_function_processor as workflow_function_processor
import harness.src.main.dao.mongo.workflow_dao as mongo_dao
from mars import mars


def get_template_tree(database, template):
    """Expands the fields for the given template into their terminal structures.
    (This means that if a template contains a Location.default field, and the
    Location.default field has a name field (string), and a coordinate field
    (Coordinate.default), this method will expand the Coordinate.default and return
    it as a nested dictionary made of its parts.
    """
    return template


def expand_template_field(database, field):
    """Expands the given field by using the structures to create a nested output,
    terminating on fundamental field types. Returns the expanded field object.
    """
    return field


def get_workflow_structure_name(workflow):
    """Returns the workflow structure name for the given workflow.
    """
    return workflow_model.get_workflow_structure(workflow)


def get_workflow_template(database, structure, current=True):
    """Returns the workflow template object from the database for the given structure.
    """
    templates = mars.template.get_current_templates_by_structure_name(database, structure)
    return templates[0]


def make_storage_field(parameter, target, scope):
    """Creates and returns a workflow structure template field.
    """
    field_info = {}
    field_info['scope'] = scope
    field_info['parameter'] = parameter
    field = mars.template.make_template_field(target['name'], target['type'],
                                              others=field_info)
    return field


def update_storage_fields(current, new):
    """Updates the storage fields, either replacing, removing, or adding the new
    storage field of/from/to the given current set.
    CURRENTLY ONLY HANDLES ADDING.
    """
    current.append(new)
    return current


def update_workflow_template(project, workflow, function, parameter, target, scope):
    """Creates a new template for the given workflow with the given fields.
    Processes the fields by updating or adding. Returns the newly formed template.
    """
    database = project['database']
    structure = workflow_model.get_workflow_structure(workflow)
    templates = mars.template.get_current_templates_by_structure_name(database, structure)
    current_template = templates[0]
    modify_date = general_utils.get_timestamp()
    current_fields = mars.template.copy_template_fields(current_template)
    new_field = make_storage_field(parameter, target, scope)
    update_storage_fields(current_fields, new_field)
    mars.template.set_template_removal_date(database, current_template, modify_date)
    new_template = {}
    new_template['fields'] = current_fields
    new_template = mars.template.create_new_template(database, workflow['structure'],
                                                     new_template, add_date=modify_date)
    return new_template


def create_workflow_structure_closure(project, update=False):

    def create_workflow_structure(workflow):
        """Creates a new workflow storage container using the mars storage model.
        Adds it to a new workflow group. Adds the storage to the workflow. Optionally
        updates the workflow in the database.
        """
        database = project
        if type(database) in [dict, OrderedDict]:
            database = database['database']
        if type(workflow) not in [dict, OrderedDict]:
            workflow = get_workflow(database, workflow_id=workflow)
        workflow_structure = workflow_model.make_workflow_structure(workflow)
        workflow_structure = mars.structure.create_new_structure(database, workflow_structure)
        mars.template.create_new_template(database, workflow_structure, {}, setup=False)
        workflow = workflow_model.add_workflow_structure(workflow, workflow_structure)
        if update:
            changes = ['structure']
            workflow = update_workflow(database, workflow, changes)
        return workflow

    return create_workflow_structure


def remove_workflow_collection(project):
    """Removes the workflow collection for the specified project.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    removal = mongo_dao.remove_workflow_collection(project)
    return removal


def update_workflow(project, workflow, changes=[]):
    """Updates the specified workflow in the database by setting the indicated changed
    parameters to their new values. Returns the updated workflow.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    workflow = mongo_dao.update_workflow(project, workflow, changes)
    return workflow


def get_current_workflows(project):
    """Returns all the current workflows for the given project.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    return mongo_dao.get_all_workflows(project, current_only=True)


def get_workflow(project, workflow_id=None, workflow_name=None):
    """Returns the workflow using an id or a name for the given project.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    if workflow_id:
        return mongo_dao.get_workflow_by_id(project, workflow_id)
    elif workflow_name:
        workflow = mongo_dao.get_workflows_by_name(project, workflow_name)
        if type(workflow) in [dict, OrderedDict]:
            return workflow
        elif type(workflow) in [list] and len(workflow) == 1:
            return workflow[0]
        return workflow
    return None


def create_workflow_collection(project, workflows=None):
    """Creates a new workflow collection in the database for the specified project.
    Returns the newly inserted workflow records.
    """
    collection = mongo_dao.create_workflow_collection(project, workflows=workflows)
    return collection


def add_workflows_to_database(project, workflows):
    """Adds the passed workflows to the specified database. Returns the inserted
    workflow records. Handles inserting a single workflow or multiple workflows.
    """
    if type(project) in [dict, OrderedDict]:
        project = project['database']
    if type(workflows) in [dict, OrderedDict]:
        return mongo_dao.add_workflow(project, workflows)
    elif type(workflows) in [list]:
        if len(workflows) == 1:
            return mongo_dao.add_workflow(project, workflows[0])
        return mongo_dao.add_workflows(project, workflows)


def add_functions_to_workflow(project, workflow, functions):
    """Adds the passed functions to the given workflow. Parses function inputs
    and outputs, adding them to the workflow. Updates the workflow in the given project.
    """
    function_maker = workflow_function_processor.get_function_from_database_closure(project)
    if type(functions) in [dict, OrderedDict]:
        function = function_maker(functions)
        workflow_model.add_function_to_workflow(workflow, function)
    elif type(functions) in [list]:
        functions = list(map(function_maker, functions))
        for function in functions:
            workflow_model.add_function_to_workflow(workflow, function)
    workflow = update_workflow(project, workflow, changes=['functions', 'parameters'])
    return workflow


def make_workflows_from_tuples(workflow_tuples):
    """Takes workflow named tuples and returns them as a list of dictionaries.
    Additionally, uses an add date to indicate when the component was added.
    """
    add_date = general_utils.get_timestamp()
    workflow_maker = workflow_model.named_tuple_to_workflow_closure(add_date)
    workflows = list(map(workflow_maker, workflow_tuples))
    return workflows


def get_workflows_from_filesystem(profile=None):
    """Grabs the workflow definition, then uses the definition to make workflow
    records. Returns a 1D array of workflow dictionary objects.
    """
    header = 'workflow'
    workflow_tuples = generic_processor.get_records_from_filesystem(header,
                                                                    "metadata",
                                                                    profile=profile)
    workflows = make_workflows_from_tuples(workflow_tuples)
    return workflows


def create_workflows_from_metadata(project, profile=None):
    """Used to create workflows from a filesystem. Assembles the complete workflows
    (adds functions, parameters, and assigns sources and targets to the parameters).
    """
    workflows = get_workflows_from_filesystem(profile=profile)
    workflows = add_workflows_to_database(project, workflows)
    storage_adder = create_workflow_structure_closure(project, update=True)
    if type(workflows) in [dict, OrderedDict]:
        workflows = storage_adder(workflows)
    else:
        workflows = list(map(storage_adder, workflows))
    return workflows


if __name__ == '__main__':
    print('Please use workflow processor module as method package.')
