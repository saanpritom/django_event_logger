from django.conf import settings
from django.core.exceptions import ValidationError


class ModuleConfigurations:
    """This file is responsible for the environment and configuration of the module. Which funtion allowed or
       not allowed is determined here. This configs methods are dependent on the settings.py file.
       The EVENT_LOGGER_SETTINGS keyword arguments on the settings.py file values are used here. But if the
       keyword argument is not on the settings.py file then it will use the default values"""

    default_allow_sensitive_test_case = False   # check self.allow_sensitive_test_cases() method

    def allow_sensitive_test_cases(self, on_test=False, test_settings_object=None):
        """The default value is FALSE. If it is TRUE then it will run some model based TestCases which may not be
           suitable for your application. If it throws any error then just make it FALSE. The second argument
           on_test is used for various TestCases to run. Genrally it is False so the original data will
           run if it is True then only the sent fake data will run. The test_settings_object contains a fake
           settings object if on_test is True"""
        if on_test is False:
            config_settings_object = settings
        else:
            config_settings_object = test_settings_object

        if hasattr(config_settings_object, 'EVENT_LOGGER_SETTINGS'):
            if 'sensitive_test_cases' in config_settings_object.EVENT_LOGGER_SETTINGS:
                if config_settings_object.EVENT_LOGGER_SETTINGS['sensitive_test_cases'] is True:
                    return True
                elif config_settings_object.EVENT_LOGGER_SETTINGS['sensitive_test_cases'] is False:
                    return False
                else:
                    raise ValidationError('sensitive_test_cases value is expected a Boolean value')
            else:
                return self.default_allow_sensitive_test_case
        else:
            return self.default_allow_sensitive_test_case
