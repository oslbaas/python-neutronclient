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

import argparse
import logging

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _

def _verify_and_parse_session_persistence(parsed_args):
    persistence = None
    if parsed_args.session_persistence:
        parts = parsed_args.session_persistence.split(':')
        if not len(parts) == 2:
           raise Exception('Incorrect --session-persistence format.'
                         ' Format is <TYPE>:<VALUE>')
        persistence = {'type': parts[0], 'cookie': parts[1]}
    return persistence


class ListPool(neutronV20.ListCommand):
    """List pools that belong to a given tenant."""

    resource = 'pool'
    shadow_resource = 'lbaas_pool'
    log = logging.getLogger(__name__ + '.ListPool')
    list_columns = ['id', 'name', 'provider', 'lb_method', 'protocol',
                    'admin_state_up', 'status']
    pagination_support = True
    sorting_support = True


class ShowPool(neutronV20.ShowCommand):
    """Show information of a given pool."""

    resource = 'pool'
    shadow_resource = 'lbaas_pool'
    log = logging.getLogger(__name__ + '.ShowPool')

    def cleanup_data(self, data):
        member_info = []
        for member in data['pool']['members']:
            member_info.append(member['id'])
        data['pool']['members'] = member_info
        return data


class CreatePool(neutronV20.CreateCommand):
    """Create a pool."""

    resource = 'pool'
    shadow_resource = 'lbaas_pool'
    log = logging.getLogger(__name__ + '.CreatePool')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state', action='store_false',
            help=_('Set admin state up to false'))
        parser.add_argument(
            '--description',
            help=_('Description of the pool'))
        parser.add_argument(
            '--healthmonitor-id',
            help=_('ID of the health monitor to use'))
        parser.add_argument(
            'name', metavar='NAME',
            help=_('The name of the pool'))
        parser.add_argument(
            '--session-persistence', metavar='TYPE',
            help=_('The type of session persistence to use.'))
        parser.add_argument(
            '--lb-algorithm',
            required=True, metavar='LB_ALGORITHM',
            choices=['ROUND_ROBIN', 'LEAST_CONNECTIONS', 'SOURCE_IP'],
            help=_('The algorithm used to distribute load between the members '
                   'of the pool'))
        parser.add_argument(
            '--protocol',
            required=True, metavar='PROTOCOL',
            choices=['HTTP', 'HTTPS', 'TCP'],
            help=_('Protocol for balancing'))

    def args2body(self, parsed_args):
        _persistence = _verify_and_parse_session_persistence(parsed_args)
        body = {
            self.resource: {
                'name': parsed_args.name,
                'admin_state_up': parsed_args.admin_state,
                'protocol': parsed_args.protocol,
                'lb_algorithm': parsed_args.lb_algorithm,
                'session_persistence ': _persistence
            },
        }
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['description', 'healthmonitor_id'])
        return body


class UpdatePool(neutronV20.UpdateCommand):
    """Update a given pool."""

    resource = 'pool'
    shadow_resource = 'lbaas_pool'
    log = logging.getLogger(__name__ + '.UpdatePool')


class DeletePool(neutronV20.DeleteCommand):
    """Delete a given pool."""

    resource = 'pool'
    shadow_resource = 'lbaas_pool'
    log = logging.getLogger(__name__ + '.DeletePool')
