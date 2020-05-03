# ansible-openstack-snapshot
RHOSC task 1

Pre Requisites: Setup ansible-collection-openstack and phython interprtor for localhost

1) wget https://galaxy.ansible.com/download/openstack-cloud-0.0.1-dev85.tar.gz

2) ansible-galaxy collection install openstack-cloud-0.0.1-dev85.tar.gz

3) pip install openstacksdk


Note: Theres an implicit localhost problem one encounters when running modules with python script. Ansible has mentioned their solution([link](https://docs.ansible.com/ansible/latest/inventory/implicit_localhost.html)). I wasn't able to make it work  properly so I made another node just to run those modules.

Lastly paste the oy file in your ansible modules dir (/home/user/.local/lib//home/ansible/.local/lib/python2.7/site-packages/ansible/modules/cloud/openstack/) or you create a dir called libary in your working directory and place the file in there. (The playbooks have to be one level up the library directory)

Example usage:<br>
```
- hosts: ws 
  tasks: 
  - name: 'Create Snapshot'
    os_server_snapshot:
        auth:
            auth_url: http://192.168.56.20/identity
            username: 'admin'
            password: 'secret'
            project_name: 'demo'
            project_id: 350e9ee3b6fb46b58e5bed9d1c498531
            user_domain_name: 'Default'
        name: 'snapshot-4'
        server: 'cf50b65b-46c3-45dc-a2c6-e3506ea8e810'
        wait: True

```

Work to be done:<br>
1)Import function from os_server module.<br>
2) Testing of module<br>
