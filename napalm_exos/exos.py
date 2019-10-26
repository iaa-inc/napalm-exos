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
from napalm.base.helpers import textfsm_extractor

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
        structured = self._get_and_parse_output('show ports transceiver information detail')
        optics = {}

        for item in structured:
            if not item['channel'] or item['channel'] == '1':  # First / only channel
                optics[item['port_number']] = {}
                optics[item['port_number']]['physical_channels'] = {}
                optics[item['port_number']]['physical_channels']['channel'] = []
            
            channel = {
                "index": int(item['channel']) - 1 if item['channel'] else 0,
                "state": {
                    "input_power": {
                        "instant": float(item['rx_power_dbm'].strip('*').strip('-inf') or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    },
                    "output_power": {
                        "instant": float(item['tx_power_dbm'].strip('*').strip('-inf') or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    },
                    "laser_bias_current": {
                        "instant": float(item['tx_current_ma'].strip('*').strip('-inf') or '0.0'),
                        "avg": 0.0,
                        "min": 0.0,
                        "max": 0.0
                    }
                }
            }
            optics[item['port_number']]['physical_channels']['channel'].append(channel)

        return optics

    def cli(self, commands):

        output = {}

        for cmd in commands:
            cmd_output = self.device.send_command(cmd)
            output[cmd] = cmd_output

        return output

    #TODO: Get Arp Table
    def get_arp_table(self):
        pass

    def get_bgp_config(self, group=u'', neighbor=u''):
        pass
    
    def get_bgp_neighbors(self):
        pass

    def get_bgp_neighbors_detail(self, neighbor_address=u''):
        pass

    def get_environment(self):
        pass

    def get_facts(self):
        pass

    def get_firewall_policies(self):
        pass

    def get_interfaces(self):
        pass

    def get_interfaces_counters(self):
        pass

    def get_interfaces_ip(self):
        pass

    def get_ipv6_neighbors_table(self):
        pass

    def get_lldp_neighbors(self):
        lldp_neighbors = self._get_and_parse_output(
            'show lldp neighbors')
        return lldp_neighbors

    def get_lldp_neighbors_detail(self, interface=u''):
        pass

    def get_mac_address_table(self):
        pass

    def get_network_instances(self, name=u''):
        pass

    def get_ntp_peers(self):
        pass

    def get_ntp_servers(self):
        pass

    def get_ntp_stats(self):
        pass

    def get_probes_config(self):
        pass

    def get_probes_results(self):
        pass

    def get_route_to(self, destination=u'', protocol=u''):
        pass

    def get_snmp_information(self):
        pass

    def get_users(self):
        pass

    # OSPF
    def get_ospf(self):
        ospf_config = self._get_and_parse_output(
            'show ospf')

        return self._key_textfsm_data(ospf_config, '', override_key='global')

    def get_ospf_interfaces(self):
        ospf_interfaces = self._get_and_parse_output(
            'show ospf interfaces detail')

        return self._key_textfsm_data(ospf_interfaces, 'vlan')

    def get_ospf_neighbors(self):
        ospf_neighbors = self._get_and_parse_output(
            'show ospf neighbor detail')

        return self._key_textfsm_data(ospf_neighbors, 'neighbor')

    # MPLS
    def get_mpls_interfaces(self):
        mpls_interfaces = self._get_and_parse_output(
            'show mpls interface detail')

        return self._key_textfsm_data(mpls_interfaces, 'vlan')

    # MPLS / LDP
    def get_mpls_ldp_peers(self):
        ldp_peers = self._get_and_parse_output(
            'show mpls ldp peer')

        return self._key_textfsm_data(ldp_peers, 'peer')
    
    # MPLS / RSVP
    def get_mpls_rsvp_neighbors(self):
        rsvp_neighbors = self._get_and_parse_output(
            'show mpls rsvp-te neighbor detail')

        return self._key_textfsm_data(rsvp_neighbors, 'neighbor_addr')
    
    # MPLS / VPLS
    def get_mpls_l2vpn_vpls(self):
        output = self.device.send_command("show l2vpn vpls detail")
        # extract vpls entries
        vpls = textfsm_extractor(self, 'show_l2vpn_vpls_detail', output)
        # extract peers
        peers = textfsm_extractor(self, 'show_l2vpn_vpls_detail_peer', output)
        # combine the above, matching on vpn_id
        for v in vpls:
            p = list(filter(lambda x: x['vpn_id'] == v['vpn_id'], peers))
            v['peers'] = p

        return vpls

    def get_mpls_l2vpn_vpws(self):
        output = self.device.send_command("show l2vpn vpws detail")
        # extract vpws entries
        vpws = textfsm_extractor(self, 'show_l2vpn_vpws_detail', output)
        # extract peers
        peers = textfsm_extractor(self, 'show_l2vpn_vpws_detail_peer', output)
        # combine the above, matching on vpn_id
        for v in vpws:
            p = list(filter(lambda x: x['vpn_id'] == v['vpn_id'], peers))
            v['peers'] = p

        return vpws

    def get_mpls_l2vpn_summary(self):
        pass

    def ping(self, destination, source=u'', ttl=255,
          timeout=2, size=100, count=5, vrf=u''):
          pass
    def traceroute(self, sdestination, source=u'', ttl=255, timeout=2, vrf=u''):
        pass


    def _get_and_parse_output(self, command):
        output = self.device.send_command(command)
        #TODO: handle file not found, parse error, blank result?
        structured = textfsm_extractor(self, command.replace(' ', '_'), output)
        return structured

    def _key_textfsm_data(self, textfsm_data, key, override_key=""):
        data = {}

        for item in textfsm_data:
            new_key = ""
            if override_key: #nasty hack for reasons
                new_key = override_key
            else:
                new_key = item[key]
                del item[key]
            data[new_key] = item
        return data

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






