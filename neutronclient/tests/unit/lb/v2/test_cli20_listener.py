# Copyright 2014 Blue Box Group, Inc.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Craig Tracey <craigtracey@gmail.com>
#

import sys

from neutronclient.neutron.v2_0.lb.v2 import listener
from neutronclient.tests.unit import test_cli20


class CLITestV20LbListenerJSON(test_cli20.CLITestV20Base):

    def test_create_listener_with_mandatory_params(self):
        """lbaas-listener-create with mandatory params only."""
        resource = 'lbaas_listener'
        cmd = listener.CreateListener(test_cli20.MyApp(sys.stdout), None)
        my_id = 'my-id'
        default_pool_id = 'default-pool-id'
        protocol = 'TCP'
        protocol_port = '80'
        args = ['--protocol', protocol, '--protocol-port', protocol_port,
                '--default-pool-id', default_pool_id]
        position_names = ['protocol', 'protocol_port',
                          'default_pool_id', 'admin_state_up']
        position_values = [protocol, protocol_port, default_pool_id, True]
        self._test_create_resource(resource, cmd, '', my_id, args,
                                   position_names, position_values)

    def test_create_listener_with_all_params(self):
        """lbaas-listener-create with all params set."""
        resource = 'lbaas_listener'
        cmd = listener.CreateListener(test_cli20.MyApp(sys.stdout), None)
        my_id = 'my-id'
        protocol = 'TCP'
        protocol_port = '80'
        default_pool_id = 'lbaas-pool-id'
        args = ['--admin-state-down', '--default-pool-id', default_pool_id,
                '--protocol', protocol, '--protocol-port', protocol_port]
        position_names = ['admin_state_up', 'default_pool_id',
                          'protocol', 'protocol_port']
        position_values = [False, default_pool_id, protocol, protocol_port]
        self._test_create_resource(resource, cmd, '', my_id, args,
                                   position_names, position_values)

    def test_list_listeners(self):
        """lbaas-listener-list."""
        resources = 'lbaas_listeners'
        cmd = listener.ListListener(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, True)

    def test_list_listeners_pagination(self):
        """lbaas-listener-list with pagination."""
        resources = 'lbaas_listeners'
        cmd = listener.ListListener(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources_with_pagination(resources, cmd)

    def test_list_listeners_sort(self):
        """lbaas-listener-list --sort-key id --sort-key asc."""
        resources = 'lbaas_listeners'
        cmd = listener.ListListener(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, True)

    def test_list_listeners_limit(self):
        """lbaas-listener-list -P."""
        resources = 'lbaas_listeners'
        cmd = listener.ListListener(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_show_listener_id(self):
        """lbaas-listener-show test_id."""
        resource = 'lbaas_listener'
        cmd = listener.ShowListener(test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id, args, ['id'])

    def test_show_listener_id_name(self):
        """lbaas-listener-show."""
        resource = 'lbaas_listener'
        cmd = listener.ShowListener(test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_update_listener(self):
        """lbaas-listener-update myid --name newname."""
        resource = 'lbaas_listener'
        cmd = listener.UpdateListener(test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'newname'],
                                   {'name': 'newname', })

    def test_delete_listener(self):
        """lbaas-listener-delete my-id."""
        resource = 'lbaas_listener'
        cmd = listener.DeleteListener(test_cli20.MyApp(sys.stdout), None)
        my_id = 'my-id'
        args = [my_id]
        self._test_delete_resource(resource, cmd, my_id, args)


class CLITestV20LbListenerXML(CLITestV20LbListenerJSON):
    format = 'xml'
