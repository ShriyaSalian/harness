import os
from pythoncommons import record_reader_utils, property_reader_utils, record_writer_utils, subprocess_utils, directory_utils, general_utils


def clone_repository(repository_info):
    """Attempts to clone the repository at the given source, with the given
    name, into the specified location. If successful, returns a dictionary
    containing information on the status of clone, the branch, and current version.
    """
    if repository_info['repository_type'] == 'git':
        clone_dictionary = subprocess_utils.clone_git_repository(repository_info['repository'],
                                                                 repository_info['name'],
                                                                 repository_info['location'])
        return clone_dictionary


def get_remote_repository_state(directory, repository, branch):
    remote_state = subprocess_utils.git_get_remote_hash(directory, repository, branch)
    return remote_state


def pull_remote_repository(name, repository, directory, branch):
    repository = subprocess_utils.pull_git_repository(name, repository, directory, branch=branch)
    return repository


def file_to_properties(extension, rel_exec_path=None, rel_property_path=None):
    current_path = os.path.dirname(os.path.realpath(__file__))
    setup_file = current_path.replace(rel_exec_path, rel_property_path)
    setup_file += extension
    properties = property_reader_utils.make_dictionary(setup_file)
    return properties


def get_unique_records(record_properties, data_types=None, read_type='file'):
    records = []
    if data_types:
        for data_type in data_types:
            if read_type == 'file':
                record_properties['records_file'] = [record_properties['base_filepath'][0] +
                                                     data_type]
            elif read_type == 'directory':
                record_properties['records_extension'] = [record_properties['base_extension'][0] +
                                                          data_type]
            records += record_reader_utils.get_records_as_tuples(record_properties)
    else:
        records += record_reader_utils.get_records_as_tuples(record_properties)
    if records and type(records) is list:
        try:
            unique_records = list(set(records))
            return unique_records
        except:
            return unique_records
    return None


def get_dictionary_by_profile(profile):
    properties = get_properties_from_file(property_file=profile,
                                          rel_prop_path='/properties/profiles/')
    dictionary = {key: properties[key][0] for key in properties.keys()}
    if 'project' not in list(dictionary.keys()):
        current = os.getcwd()
        base = current.rsplit('/harness/', 1)[0]
        base += '/harness'
        dictionary['project'] = base
    return dictionary


def property_keywords_dictionary_closure(profile):

    profile_dictionary = get_dictionary_by_profile(profile)
    general_utils.get_fully_qualified_dictionary_values(profile_dictionary)

    def replace_value(value):
        for keyword in profile_dictionary:
            if type(value) is list:
                value = [v.replace('{' + keyword + '}', profile_dictionary[keyword])
                         for v in value]
            else:
                try:
                    value = value.replace('{' + keyword + '}', profile_dictionary[keyword])
                except AttributeError:
                    pass
        return value

    def adjust_property_keywords(property_dictionary):
        updated_property_dictionary = {}
        for key in property_dictionary.keys():
            updated_value = replace_value(property_dictionary[key])
            updated_property_dictionary[key] = updated_value
        return updated_property_dictionary

    return adjust_property_keywords


def property_file_lookup(property_type, map_type):
    if map_type == "properties":
        return property_type.strip() + ".setup.properties"
    elif map_type == "metadata":
        return property_type.strip() + ".metadata.headers"
    elif map_type == "records":
        return property_type.strip() + ".records.headers"


def get_properties_from_file(property_type=None,
                             property_file=None,
                             file_type=None,
                             rel_exec_path='/src/main/dao/filesystem',
                             rel_prop_path='/properties/models/'):
    if not property_file:
        property_file = property_file_lookup(property_type, file_type)
    if not property_file:
        return "Cannot build properties for unspecified type"
    return file_to_properties(property_file, rel_exec_path, rel_prop_path)


def remove_directory(directory):
    """Removes directory and subdirectories from the filesystem.
    """
    directory_utils.remove_directory(directory)
    return True


def get_directory_exists(directory):
    """Returns True if the directory exists, or False if the directory does not
    exist.
    """
    directory_exists = directory_utils.get_directory_exists(directory)
    return directory_exists


def write_records(records, properties):
    write_status = record_writer_utils.write_records(records, properties)
    return write_status


if __name__ == '__main__':
    print("Please access this module as a method package.")
