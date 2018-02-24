import harness.src.main.dao.filesystem.filesystem_dao as file_dao
from pythoncommons import general_utils


def get_fully_qualified_profile_from_filesystem(profile):
    """Returns the fully qualified profile from the filesystem location for the given
    profile (by string). The profile must live in the project/profiles directory.
    """
    profile_dictionary = file_dao.get_dictionary_by_profile(profile)
    general_utils.get_fully_qualified_dictionary_values(profile_dictionary)
    return profile_dictionary


def get_dictionary_from_filesystem(property_type, file_type, profile=None):
    dictionary = file_dao.get_properties_from_file(property_type=property_type,
                                                   file_type=file_type)
    if profile:
        dict_updater = file_dao.property_keywords_dictionary_closure(profile)
        dictionary = dict_updater(dictionary)
        dictionary['keyword_converter'] = dict_updater
    return dictionary


def get_records_from_filesystem(property_type, file_type, profile=None):
    dictionary = get_dictionary_from_filesystem(property_type, file_type, profile=profile)
    tuples = file_dao.get_unique_records(dictionary)
    return tuples


def load_profile_from_filesystem(profile=None):
    profile_dictionary = file_dao.get_dictionary_by_profile(profile)
    return profile_dictionary


if __name__ == '__main__':
    print("Please use this as a method package.")
