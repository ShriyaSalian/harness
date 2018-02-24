from flask import Flask, request, render_template
from pythoncommons import subprocess_utils
import os
import harness.src.main.processor.project_processor as project_processor
import harness.src.main.processor.generic_processor as generic_processor
import harness.src.main.router.parameter_router as parameter_router
import harness.src.main.model.generic_model as generic_model
import harness.src.test.processor.project_processor_test as processor_test


def get_template_folder(paths):
    template_folder = paths['template']
    return template_folder


def get_static_folder(paths):
    static_folder = paths['static']
    return static_folder


def get_paths(profile=None):
    if profile:
        paths = get_profile_dictionary(profile=profile)
    else:
        paths = {}
        current = os.getcwd()
        current = current.replace('src/main/controller', '')
        paths['static'] = current + 'web'
        paths['template'] = current + 'web/html'
    paths['serving_static'] = False
    return paths


def get_profile_dictionary(profile=None):
    profile_dictionary = generic_processor.get_fully_qualified_profile_from_filesystem(profile)
    return profile_dictionary


def get_serving_static():
    return False


serving_static = get_serving_static()
paths = get_paths()
template_folder = get_template_folder(paths)
static_folder = get_static_folder(paths)

app = Flask(__name__, template_folder=template_folder,
            static_folder=static_folder)


@app.route('/static_resources')
def start_static_resources():
    simple_server = static_folder + '/' + 'simple_server.py'
    server_string = 'python {simple_server} 8018'.format(simple_server=simple_server)
    output = subprocess_utils.call_Popen(server_string, directory=static_folder)
    return output


@app.route("/")
def information():
    if not paths['serving_static']:
        try:
            start_static_resources()
            paths['serving_static'] = True
        except:
            pass
    return render_template("index.html")


@app.route("/test_setup")
def project_test_setup():
    test_result = processor_test.perform_fresh_filesystem_setup()
    return generic_model.JSONEncoder().encode(test_result)


@app.route("/get_projects")
def get_projects():
    projects = project_processor.get_all_projects()
    dictionary = {}
    dictionary['projects'] = projects
    dictionary = generic_model.JSONEncoder().encode(dictionary)
    return dictionary


@app.route("/parameters/get_tree")
def get_structures():
    project = project_processor.get_project_by_name('py_common')
    database = project['database']
    parameters = parameter_router.get_all_parameters(database)
    parameters = generic_model.JSONEncoder().encode(parameters)
    return parameters


@app.route("/parameters/get_groups")
def get_groups():
    project = project_processor.get_project_by_name('py_common')
    database = project['database']
    groups = parameter_router.get_groups(database)
    groups = generic_model.JSONEncoder().encode(groups)
    return groups


@app.route('/parameters/update', methods=['GET', 'POST'])
def update_parameter():
    """ This method is a generic handling of updates to project parameters,
    including groups, structures, templates, and fields. It should take a parameters
    object that has a subobject called 'update', which should be an array of update
    dictionaries. Each update in the array should consist of whichever of
    the following keys are necessary to perform the requested action:
    update: contains the key value pairs of changes to be made to the system.
    changes: a list of changes to be made to an existing thing.
    _id: the id of the thing to be updated or removed.
    action: a string, indicating 'add', 'update', 'remove'.
    """
    project = project_processor.get_project_by_name('py_common')
    database = project['database']
    if request.method == 'POST':
        updates = request.get_json(silent=True)['update']
        update_result = parameter_router.modify_parameters(database, updates)
        return generic_model.JSONEncoder().encode(update_result)


@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Shutting down server."


def startup():
    app.run(debug=True, host='0.0.0.0', port=8008)


if __name__ == '__main__':
    startup()
