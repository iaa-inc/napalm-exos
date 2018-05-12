# Copyright Internet Association of Australia 2018. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Napalm driver for Extreme EXOS.

Read https://napalm.readthedocs.io for more information.
"""
from napalm.base.base import NetworkDriver
from napalm.base.utils import py23_compat
from napalm.base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )
from netmiko import ConnectHandler, SCPConn
from textfsm import TextFSM

import logging
import re
import os
import uuid
import tempfile
import copy
import jinja2

logging.basicConfig()


class ExosDriver(NetworkDriver):
    """Napalm driver for Extreme Networks EXOS."""

    def __init__(self, hostname, username, password, timeout=60, optional_args={}):
        """Constructor."""
        self.device = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout
        self.optional_args = optional_args

        if optional_args is None:
            optional_args = {}

    def open(self):
        """Implementation of NAPALM method open."""
        self.device = ConnectHandler(
            device_type = 'extreme',
            ip=self.hostname,
            username=self.username,
            password=self.password,
            **self.optional_args)

    def close(self):
        """Implementation of NAPALM method close.
        """
        self.device.disconnect()

    def get_config(self, retrieve='all'):

        # EXOS doesn't support candidate configuration
        # TODO: support startup configuration (saved)
        configs = {
            'startup' : '',
            'running' : '',
        }

        configs['running'] = self.device.send_command('show configuration')

        return configs

    def get_optics(self, interface=None):
        template_path = os.path.join(self._template_location(), 'show_ports_transceiver_information_detail.tpl')
        template = open(template_path)
        re_table = TextFSM(template)
        
        command = 'show ports transceiver information detail'
        show_ports = self.device.send_command(command)

        structured = re_table.ParseText(show_ports)
        optics = {}

        for item in structured:
            if not item[8] or item[8] == "1":  # First / only channel
                optics[item[0]] = {}
                optics[item[0]]["physical_channels"] = {}
                optics[item[0]]["physical_channels"]["channel"] = []

            channel = {
                "index": int(item[8]) - 1 if item[8] else 0,
                "state": {
                    "input_power": {
                        "instant": float(item[9] or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    },
                    "output_power": {
                        "instant": float(item[10] or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    },
                    "laser_bias_current": {
                        "instant": float(item[11] or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    }
                }
            }
            optics[item[0]]["physical_channels"]["channel"].append(channel)

        return optics

    def cli(self, commands):

        output = {}

        for cmd in commands:
            cmd_output = self.device.send_command(cmd)
            output[cmd] = cmd_output

        return output

    @staticmethod
    def _template_location():
        return os.path.join(os.path.dirname(__file__), 'utils', 'textfsm_templates')

    def _create_temp_file(self, content, extension, name=None):
        # create a temp file with option name, defaults to random UUID
        # e.g. _create_temp_file(config, "pol", name="AS6500-POLICY-IN")
        
        tmp_dir = tempfile.gettempdir()

        if not name:
            rand_fname = str(uuid.uuid4()) + "." + extension
            filename = os.path.join(tmp_dir, rand_fname)
        else:
            filename = os.path.join(tmp_dir, name + "." + extension)

        with open(filename, 'wt') as fobj:
            fobj.write(content)
            fobj.close()

        return filename

    def _transfer_file_scp(self, source_file, destination_file):
        scp_conn = SCPConn(self.device)
        scp_conn.scp_transfer_file(source_file,destination_file)


    def load_merge_candidate(self, filename=None, config=None):
        # SCP config snippet to device.
        if filename and config:
            raise ValueError("Cannot simultaneously set file and config")

        temp_file = self._create_temp_file(config, "xsf")

        self._transfer_file_scp(filename, temp_file)

        output = self.cli(["run script " + temp_file])

        # TODO: Cleanup the random files on the device.

        return bool(output)

    def compare_config(self):
        diff = self.cli(['run script conf_diff'])
        return diff

    def commit_config(self):
        output = self.device.send_command("save\ry\r")
        return " successfully." in output

    def load_policy_template(self, policy_name, template_source, **template_vars):
        # for Extreme:
        # if template_path is None, then it loads to running config. Otherwise it assume an absolute filesystem location.
        # e.g. /usr/local/cfg

        if isinstance(template_source, py23_compat.string_types):
            # Load and render template to string.
            configuration = jinja2.Template(template_source).render(**template_vars)

            policy_file = self._create_temp_file(configuration, "pol", name=policy_name)

            # transfer to device.
            self._transfer_file_scp(policy_file, policy_name + ".pol")

            # Check the policy
            check_command = "check policy " + policy_name
            check_output = self.cli([check_command])

            if "successful" not in check_output[check_command]:
                raise ValueError
            else:
                return configuration
        else:
            raise NotImplementedError






