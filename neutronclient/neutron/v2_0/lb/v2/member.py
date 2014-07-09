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


class ListMember(neutronV20.ListCommand):
    """List members that belong to a given tenant."""

    resource = 'member'
    log = logging.getLogger(__name__ + '.ListMember')
    list_columns = [
        'id', 'address', 'protocol_port', 'weight',
        'subnet_id', 'admin_state_up', 'status'
    ]
    pagination_support = True
    sorting_support = True


class ShowMember(neutronV20.ShowCommand):
    """Show information of a given member."""

    resource = 'member'
    log = logging.getLogger(__name__ + '.ShowMember')


class CreateMember(neutronV20.CreateCommand):
    """Create a member."""

    resource = 'member'
    log = logging.getLogger(__name__ + '.CreateMember')

    def add_known_arguments(self, parser):
        parser.add_argument(
            'pool_id', metavar='POOL',
            help=_('ID of the pool that this member belongs to'))
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false'))
        parser.add_argument(
            '--weight',
            help=_('Weight of member in the pool (default:1, [0..256])'))
        parser.add_argument(
            '--subnet-id',
            help=_('Subnet ID for the member'))
        parser.add_argument(
            '--address',
            required=True,
            help=_('IP address of the pool member in the pool. '))
        parser.add_argument(
            '--protocol-port',
            required=True,
            help=_('Port on which the pool member listens for requests or '
                   'connections. '))

    def args2body(self, parsed_args):
        _pool_id = neutronV20.find_resourceid_by_name_or_id(
            self.get_client(), 'pool', parsed_args.pool_id)
        body = {
            self.resource: {
                'pool_id': _pool_id,
                'admin_state_up': parsed_args.admin_state,
                'protocol_port': parsed_args.protocol_port,
                'address': parsed_args.address,
            },
        }
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['weight', 'subnet_id'])
        return body


class UpdateMember(neutronV20.UpdateCommand):
    """Update a given member."""

    resource = 'member'
    log = logging.getLogger(__name__ + '.UpdateMember')


class DeleteMember(neutronV20.DeleteCommand):
    """Delete a given member."""

    resource = 'member'
    log = logging.getLogger(__name__ + '.DeleteMember')
