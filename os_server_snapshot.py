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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.openstack import (
    openstack_cloud_from_module, openstack_module_kwargs,
    openstack_full_argument_spec )
    
def _exit_hostvars(module, cloud, server, changed=True):
    hostvars = cloud.get_openstack_vars(server)
    module.exit_json(
        changed=changed, server=server, id=server.id, openstack=hostvars)
        
def _parse_meta(meta):
    if isinstance(meta, str):
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

    module.params['meta'] = _parse_meta(module.params['meta'])
    
    meta = module.params['meta']
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
