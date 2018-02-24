from pythoncommons import utils


def named_tuple_to_compound_function_closure(add_date):
    """A function that turns a named tuple compound function record into a
    dictionary, removing extraneous identifier keys, and adding metadata.
    Used in the functional mapping pattern.
    """

    def named_tuple_to_compound_function(compound_function_tuple):
        compound_function = compound_function_tuple._asdict()
        add_dates(compound_function)
        del compound_function_tuple
        return compound_function

    def add_dates(compound_function):
        compound_function['add_date'] = add_date
        compound_function['remove_date'] = None

    return named_tuple_to_compound_function


def remove_subfunction_identifiers(subfunction):
    subfunction_identifiers = ['project', 'function']
    utils.remove_dictionary_keys(subfunction, subfunction_identifiers)
    return subfunction


def remove_all_subfunction_identifiers(compound_function):
    """Removes the compound function identifiers from the passed compound function.
    Currently removes the function name from the subfunctions in the compound function.
    Returns the updated compound function dictionary object.
    """

    subfunctions = list(map(remove_subfunction_identifiers, compound_function['subfunctions']))
    compound_function['subfunctions'] = subfunctions

    return compound_function


def make_complexity_simple(compound_function):
    """Function changes the complexity parameter of the class object to simple and
    returns the updated function.
    """
    compound_function = change_complexity(compound_function, 'simple')
    return compound_function


def make_complexity_recursive(compound_function):
    """Function changes the complexity parameter of the class object to recursive and
    returns the updated function.
    """
    compound_function = change_complexity(compound_function, 'recursive')
    return compound_function


def change_complexity(compound_function, new_complexity):
    """Generic function to change the complexity of the passed function.
    """
    compound_function['class']['complexity'] = new_complexity
    return compound_function


def remove_component(function):
    """Removes a component key from a function dictionary. Can be used for subfunction
    or compound_function.
    """
    remove_keys = ['component']
    utils.remove_dictionary_keys(function, remove_keys)
    return function

if __name__ == '__main__':
    print("Compound function model module. Please use as method package.")
