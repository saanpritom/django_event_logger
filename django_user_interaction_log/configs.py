from django.conf import settings
from django.core.exceptions import ValidationError


class ModuleConfigurations:
    """This file is responsible for the environment and configuration of the module. Which funtion allowed or
       not allowed is determined here. This configs methods are dependent on the settings.py file.
       The DJANGO_USER_INTERACTION_LOG_SETTINGS keyword arguments on the settings.py file values are used here.
       But if the keyword argument is not on the settings.py file then it will use the default values"""

    default_allow_sensitive_test_case = False   # check self.allow_sensitive_test_cases() method
    default_user_representer_field = '__str__'  # check self.get_default_user_representer_field() method
    default_log_list_paginated_by = 100  # check self.get_log_records_list_pagination() method

    def get_settings_object(self, on_test, test_settings_object):
        """If it is a Test Case then return test_settings_object. If not then return the settings object"""
        if on_test is False:
            return settings
        else:
            return test_settings_object

    def is_default_settings_modified(self, settings_object):
        """This function return True if DJANGO_USER_INTERACTION_LOG_SETTINGS
           is on the settings file otherwise return False"""
        if hasattr(settings_object, 'DJANGO_USER_INTERACTION_LOG_SETTINGS'):
            return True
        return False

    def is_key_in_dict(self, dict, key):
        """Returns True if the key found on the dict otherwise False"""
        if key in dict:
            return True
        return False

    def allow_sensitive_test_cases(self, on_test=False, test_settings_object=None):
        """The default value is FALSE. If it is TRUE then it will run some model based TestCases which may not be
           suitable for your application. If it throws any error then just make it FALSE. The second argument
           on_test is used for various TestCases to run. Genrally it is False so the original data will
           run if it is True then only the sent fake data will run. The test_settings_object contains a fake
           settings object if on_test is True"""
        config_settings_object = self.get_settings_object(on_test, test_settings_object)

        if self.is_default_settings_modified(config_settings_object):
            if self.is_key_in_dict(config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS, 'sensitive_test_cases'):
                if config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['sensitive_test_cases'] is True:
                    return True
                elif config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['sensitive_test_cases'] is False:
                    return False
                else:
                    raise ValidationError('sensitive_test_cases value is expected a Boolean value')
            else:
                return self.default_allow_sensitive_test_case
        else:
            return self.default_allow_sensitive_test_case

    def get_default_user_representer_field(self, on_test=False, test_settings_object=None):
        """The default value is __str__ which means the default string representation of the User model of the
           application"""
        config_settings_object = self.get_settings_object(on_test, test_settings_object)

        if self.is_default_settings_modified(config_settings_object):
            if self.is_key_in_dict(config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS, 'user_representer_field'):
                if isinstance(config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['user_representer_field'], str):
                    return config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['user_representer_field']
                else:
                    raise ValidationError('user_representer_field value must be a string')
            else:
                return self.default_user_representer_field
        else:
            return self.default_user_representer_field

    def get_log_records_list_pagination(self, on_test=False, test_settings_object=None):
        """This set the pagination number of the log list views. If you want to change it then please change
            list_paginated_by keyword on DJANGO_USER_INTERACTION_LOG_SETTINGS"""
        config_settings_object = self.get_settings_object(on_test, test_settings_object)

        if self.is_default_settings_modified(config_settings_object):
            if self.is_key_in_dict(config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS, 'list_paginated_by'):
                if isinstance(config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['list_paginated_by'], int):
                    return config_settings_object.DJANGO_USER_INTERACTION_LOG_SETTINGS['list_paginated_by']
                else:
                    raise ValidationError('list_paginated_by value must be an Integer')
            else:
                return self.default_log_list_paginated_by
        else:
            return self.default_log_list_paginated_by
