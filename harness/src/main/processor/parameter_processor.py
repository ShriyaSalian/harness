import harness.src.main.model.parameter_model as parameter_model
import harness.src.main.dao.mongo.parameter_dao as parameter_dao
from pythoncommons import utils
from mars import mars


def add_parameters_to_project_from_filesystem(profile_path, project, full_path=False, profile_name=None, profile_dictionary=None):
    mars.setup.remove_all_storage(project['database'])
    setup = mars.setup.basic_system_setup(project['database'], profile_path, full_path=full_path, profile_name=profile_name, profile_dictionary=profile_dictionary)
    structures = get_current_structures(project['database'])
    groups = assemble_groups_from_structures(structures, complete=False)
    add_parameter_groups(project['database'], groups)
    return setup


def get_group_by_name(groups, group_name):
    for group in groups:
        if group['name'] == group_name:
            return group


def get_current_parameter_groups(database):
    """Returns the parameter groups currently stored in the project database.
    """
    groups = parameter_dao.get_all_current_groups(database)
    return groups


def add_parameter_groups(database, groups):
    """Adds the array of group names (as an array of strings) to the given project
    database. Returns the created groups.
    """
    groups = parameter_dao.create_group_collection(database, groups)
    return groups


def add_parameter_group(database, group):
    """Adds the passed parameter group (as a string) to the given project database.
    This method should check to ensure the name is unique to the database.
    """
    group = parameter_dao.add_group(database, group)
    return group


def assemble_groups_from_structures(structures, complete=True):
    """Returns the unique set of groups for the array of dictionaries that is passed.
    If keyword parameter 'complete' is True, adds complete structures to each group.
    If keyword parameter 'complete' is False, only adds structure names to the group.
    """
    add_date = utils.get_timestamp()
    group_names = []
    groups = []
    counter = 0
    for structure in structures:
        if structure['group'] not in group_names:
            groups.append(parameter_model.make_group(structure['group'], add_date, order=counter))
            group_names.append(structure['group'])
            counter += 1
        if complete:
            get_group_by_name(groups, structure['group'])['structures'].append(structure)
        else:
            get_group_by_name(groups, structure['group'])['structures'].append(structure['name'])
    return groups


def get_current_structures(database):
    """Returns the structures currently attached to the given project database.
    """
    structures = mars.structure.get_current_structures(database)
    return structures


def get_parameter_tree(database):
    """Returns a complete parameter tree for the specified database. The tree is
    returned as root -> groups -> structures -> templates -> fields. This method
    does not return workflow structures.
    """
    args = [{'key': 'group',
             'value': 'workflow',
             'operation': 'not_equals'}]
    structures = mars.structure.get_current_structures(database, args=args)
    template_adder = mars.structure.get_structure_templates_closure(database, 'current')
    structures = list(map(template_adder, structures))
    groups = assemble_groups_from_structures(structures)
    tree = parameter_model.make_parameter_tree(groups=groups)
    return tree


def update_template_fields(database, template):
    """ Updates the given template fields collection. The passed template dictionary
    must contain the template ID (_id) and the new fields array.
    Returns the updated template object.
    """
    template = mars.template.update_template_fields(database, template)
    return template


def update_root(database, root, changes):
    """Updates the root paramter tree.
    """
    return root


def update_group(database, group, changes):
    """Updates a paramter group.
    """
    return group


def update_structure(database, structure, changes):
    """Updates a parameter structure.
    """
    structure = mars.structure.update_structure(database, structure, changes=changes)
    return structure


def update_template(database, template, changes):
    """Updates a parameter template.
    """
    template = mars.template.update_template(database, template, changes=changes)
    return template


def remove_template(database, template, structure):
    """Removes a parameter template. If successful, this method returns
    the updated parent structure. If it fails, it will return None.
    """
    return mars.template.remove_template(database, template, structure)


def add_template(database, template, structure, order=None):
    """Adds a new template to the database.
    """
    return mars.template.create_new_template(database, structure, template, order=order)


def move_template(database, update):
    """Move a template with the given id from the given old_parent to the given
    new_parent. Returns the updated template.
    """
    template = update['_id']
    new_structure = update['new_parent']
    new_name = update['new_name']
    return mars.template.move_template(database, template, new_structure, new_name)


def move_structure(database, update):
    """Move a structure with the given id from the given old_parent to the new_parent.
    Returns the updated structure.
    """
    pass


if __name__ == '__main__':
    print('Please use parameter processor module as method package.')
