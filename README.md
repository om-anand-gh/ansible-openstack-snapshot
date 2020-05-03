# ansible-openstack-snapshot
RHOSC task 1

Pre Requisites: Setup ansible-collection-openstack and phython interprtor for localhost

1) wget https://galaxy.ansible.com/download/openstack-cloud-0.0.1-dev85.tar.gz

2) ansible-galaxy collection install openstack-cloud-0.0.1-dev85.tar.gz

3) pip install openstacksdk


Note: Theres an implicit localhost problem one encounters when running modules with python script. Ansible has mentioned their solution([link](https://docs.ansible.com/ansible/latest/inventory/implicit_localhost.html)). I wasn't able to make it work  properly so I made another node just to run those modules.

Lastly paste the oy file in your ansible modules dir (/home/user/.local/lib//home/ansible/.local/lib/python2.7/site-packages/ansible/modules/cloud/openstack/) or you create a dir called libary in your working directory and place the file in there. (The playbooks have to be one level up the library directory)

Example usage:<br>

- hosts: ws <br>
  tasks: <br>
  - name: 'Create Snapshot' <br>
    os_server_snapshot:<br>
        auth:<br>
            auth_url: http://192.168.56.20/identity<br>
            username: 'admin'<br>
            password: 'secret'<br>
            project_name: 'demo'<br>
            project_id: 350e9ee3b6fb46b58e5bed9d1c498531<br>
            user_domain_name: 'Default'<br>
        name: 'snapshot-4'<br>
        server: 'cf50b65b-46c3-45dc-a2c6-e3506ea8e810'<br>
        wait: True<br>

