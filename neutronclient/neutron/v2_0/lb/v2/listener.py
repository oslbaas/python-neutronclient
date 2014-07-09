# Copyright 2014 Blue Box Group, Inc.
# All Rights Reserved
#
# Author: Craig Tracey <craigtracey@gmail.com>
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

import logging

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _


class ListListener(neutronV20.ListCommand):
    """List listeners that belong to a given tenant."""

    resource = 'listener'
    log = logging.getLogger(__name__ + '.ListListener')
    list_columns = ['id', 'default_pool_id', 'protocol',
                    'protocol_port', 'admin_state_up', 'status']
    pagination_support = True
    sorting_support = True


class ShowListener(neutronV20.ShowCommand):
    """Show information of a given listener."""

    resource = 'listener'
    log = logging.getLogger(__name__ + '.ShowListener')


class CreateListener(neutronV20.CreateCommand):
    """Create a listener."""

    resource = 'listener'
    log = logging.getLogger(__name__ + '.CreateListener')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false'))
        parser.add_argument(
            '--loadbalancer-id',
            dest='loadbalancer_id',
            metavar='LOADBALANCER', required=True,
            help=_('ID of the load balancer'))
        parser.add_argument(
            '--protocol',
            required=True,
            choices=['TCP', 'UDP', 'HTTP', 'HTTPS'],
            help=_('Protocol for the listener'))
        parser.add_argument(
            '--protocol-port',
            dest='protocol_port', required=True,
            metavar='PORT',
            help=_('Protocol port for the listener'))
        parser.add_argument(
            '--default-pool-id',
            dest='default_pool_id', metavar='POOL',
            required=True, help=_('The default pool ID to use'))

    def args2body(self, parsed_args):
        body = {
            self.resource: {
                'default_pool_id': parsed_args.default_pool_id,
                'protocol': parsed_args.protocol,
                'protocol_port': parsed_args.protocol_port,
                'admin_state_up': parsed_args.admin_state,
		        'loadbalancer_id': parsed_args.loadbalancer_id
            },
        }
#        neutronV20.update_dict(parsed_args, body[self.resource],
#                               ['loadbalancer_id'])
        return body


class UpdateListener(neutronV20.UpdateCommand):
    """Update a given listener."""

    resource = 'listener'
    log = logging.getLogger(__name__ + '.UpdateListener')
    allow_names = False


class DeleteListener(neutronV20.DeleteCommand):
    """Delete a given listener."""

    resource = 'listener'
    log = logging.getLogger(__name__ + '.DeleteListener')
