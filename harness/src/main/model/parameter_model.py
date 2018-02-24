from python_commons import utils


def make_parameter_tree(groups):
    parameter = {}
    parameter['name'] = 'Structures'
    parameter['type'] = 'root'
    parameter['groups'] = groups
    return parameter


def make_group(group_name, add_date=utils.get_timestamp(), order=None):
    group = {}
    group['name'] = group_name
    group['type'] = 'group'
    group['structures'] = []
    group['order'] = order
    group['remove_date'] = None
    group['add_date'] = add_date
    return group


if __name__ == '__main__':
    print('Please use parameter model module as method package.')
