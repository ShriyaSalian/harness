from python_commons import utils


def update_location(expression, location):
    if 'location' in list(expression.keys()):
        expression['location'] = expression['location'].replace('{' + 'component' + '}',
                                                                location)
    return expression


def add_parameters_to_expression(expression, parameters):
    expression['inputs'] = parameters
    return expression


def named_tuple_to_expression_closure(add_date):

    def named_tuple_to_expression(expression_tuple):
        expression = expression_tuple._asdict()
        expression["add_date"] = add_date
        expression["remove_date"] = None
        del expression_tuple
        remove_identifiers(expression)
        return expression

    def remove_identifiers(expression):
        """Removes identifier keys from the expression dictionary.
        """
        remove_expression_keys = ['project', 'component', 'function']
        utils.remove_dictionary_keys(expression, remove_expression_keys)

    return named_tuple_to_expression
