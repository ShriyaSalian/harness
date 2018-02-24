import harness.src.main.model.function_model as function_model
import harness.src.main.model.functions.external_function_model as external_model
import harness.src.main.processor.expression_processor as expression_processor


def update_external_function_parameters(function):
    """Inputs an external function dictionary object and uses its external expressions
    to create and add an output object to the function. Returns the updated function.
    """
    parameters = expression_processor.get_classified_expression_parameters(function['expressions'])
    function = function_model.update_function_parameters(function, parameters)
    return function


def add_expressions_to_external_function_closure(component, source='filesystem', profile=None):

    def add_expressions_to_external_function(function):
        """Method designed to get function expressions as a list of dictionary
        objects and then use the function_model module to add the expressions to the
        appropriate function.
        """
        expressions = get_function_expressions(component, function, source=source, profile=profile)
        function = external_model.add_expressions_to_external_function(function, expressions)
        return function

    return add_expressions_to_external_function


def get_function_expressions(component, function, source="filesystem", profile=None):
    """Returns a dictionary object of expressions associated with the passed function.
    The function should be passed as a name. The source may be specified to handle where
    the expressions are retrieved from, in memory, database, or filesystem. Defaults
    to filesystem.
    """
    expressions = expression_processor.get_expressions_for_function(component, function,
                                                                    source=source,
                                                                    profile=profile)
    return expressions

if __name__ == '__main__':
    print("External Function Processor Module. Please use as method package.")
