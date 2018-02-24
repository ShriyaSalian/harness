import harness.src.main.processor.function_processor as function_processor


def test_create_new_function(project, component, function):
    """Tests creating a new function in the database for the given project and component.
    Returns the inserted function.
    """
    function = function_processor.add_new_function(project, component, function)
    return function
