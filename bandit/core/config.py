# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

import yaml

from bandit.core import constants
from bandit.core import utils


logger = logging.getLogger(__name__)


class BanditConfig():
    def __init__(self, config_file):
        '''Attempt to initialize a config dictionary from a yaml file.

        Error out if loading the yaml file fails for any reason.
        :param config_file: The Bandit yaml config file

        :raises bandit.utils.ConfigFileUnopenable: If the config file cannot be
            opened.
        :raises bandit.utils.ConfigFileInvalidYaml: If the config file cannot
            be parsed.

        '''

        self.config_file = config_file
        try:
            f = open(config_file, 'r')
        except IOError:
            raise utils.ConfigFileUnopenable(config_file)

        try:
            self._config = yaml.safe_load(f)
        except yaml.YAMLError:
            raise utils.ConfigFileInvalidYaml(config_file)

        self._init_settings()

    def get_option(self, option_string):
        '''Returns the option from the config specified by the option_string.

        '.' can be used to denote levels, for example to retrieve the options
        from the 'a' profile you can use 'profiles.a'
        :param option_string: The string specifying the option to retrieve
        :return: The object specified by the option_string, or None if it can't
        be found.
        '''
        option_levels = option_string.split('.')
        cur_item = self._config
        for level in option_levels:
            if cur_item and (level in cur_item):
                cur_item = cur_item[level]
            else:
                return None

        return cur_item

    def get_setting(self, setting_name):
        if setting_name in self._settings:
            return self._settings[setting_name]
        else:
            return None

    @property
    def config(self):
        '''Property to return the config dictionary

        :return: Config dictionary
        '''
        return self._config

    def _init_settings(self):
        '''This function calls a set of other functions (one per setting)

        This function calls a set of other functions (one per setting) to build
        out the _settings dictionary.  Each other function will set values from
        the config (if set), otherwise use defaults (from constants if
        possible).
        :return: -
        '''
        self._settings = {}
        self._init_plugin_name_pattern()

    def _init_plugin_name_pattern(self):
        '''Sets settings['plugin_name_pattern'] from default or config file.'''
        plugin_name_pattern = constants.plugin_name_pattern
        if self.get_option('plugin_name_pattern'):
            plugin_name_pattern = self.get_option('plugin_name_pattern')
        self._settings['plugin_name_pattern'] = plugin_name_pattern
