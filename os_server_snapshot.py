#!/usr/bin/python
# coding: utf-8 -*-

# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
# Copyright (c) 2013, Benno Joy <benno@ansible.com>
# Copyright (c) 2013, John Dewey <john@dewey.ws>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION='''
---
module: os_serve_snapshot
short_description: Create snapshots of Instances in OpenStack
extends_documentation_fragment: openstack
description:
    - Create snapshots of an instance in OpenStack.
options:
    name:
      description:
         - Name that has to be given to the Snapshot.
      required: True
    server:
      description:
         - The name or id of the instance to be snapshotted.
      required: True
    wait:
      description:
         - If the module should wait for the snapshot to be created.
      type: bool
      default: 'yes'
    timeout:
      description:
         - The amount of time the module should wait for the instance to get
          into active state.
      default: 180
    meta:
      description:
         - 'A list of key value pairs that should be provided as a metadata to
           the new instance or a string containing a list of key-value pairs.
           Eg:  meta: "key1=value1,key2=value2"'
'''
EXAMPLES = '''
- name: Create a snapshot of an instance.
  os_server_snapshot:
       auth:
         auth_url: https://identity.example.com
         username: admin
         password: admin
         project_name: admin
       name: Snapshot-1
       server: vm1
       timeout: 200
       meta:
         group: vm1-snaps
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import (
    openstack_cloud_from_module, openstack_module_kwargs,
    openstack_full_argument_spec )
    
def _parse_meta(meta):
    if isinstance(meta, str):
        print('True')
        print('Entered Loop')
        metas = {}
        for kv_str in meta.split(","):
            k, v = kv_str.split("=")
            metas[k] = v
        return metas
    if not meta:
        return {}
    return meta

def _create_server_snapshot(module, cloud):
    server = module.params['server']
	
    if server:
        server_dict = cloud.get_server(server)
        if not server_dict:
            module.fail_json(msg="Could not find server %s" % server)

    meta  = _parse_meta(module.params['meta'])
    
    server_snapshot = cloud.create_image_snapshot(
    	name=module.params['name'],
    	server=module.params['server'],
        wait=module.params['wait'],
        timeout=module.params['timeout'],
        **meta
    )

    module.exit_json(changed=True, result='Snapshot created')


def main():

    argument_spec = openstack_full_argument_spec(
        name=dict(required=True),
        server=dict(required=True),
        wait=dict(default=True, type='bool'),
	timeout=dict(default=180, type='int'),
        meta=dict(default=None, type='raw'),
    )
    
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)

    sdk, cloud = openstack_cloud_from_module(module)
    
    try:
        _create_server_snapshot(module, cloud)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)


if __name__ == '__main__':
    main()
