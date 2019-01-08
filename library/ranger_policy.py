#!/usr/bin/python

# Copyright: (c) 2019, Eric Deleforterie <https://github.com/EricDele>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ranger_policy

short_description: This is a module for managing ranger policies

version_added: "2.5"

description:
    - "This is a module for managing Hortonworks Ranger policies"

options:
    admin_url:
        description:
            - This is the ranger url <http(s)://ranger_server:port>
        required: false
        default: https://localhost:6082
    ranger_user:
        description:
            - This is the user used to login in ranger
        required: true
    ranger_user_password:
        description:
            - This is the user password used to login in ranger
        required: true
    policy_type:
        description:
            - If C(hbase), will create a HBASE policy
            - If C(hdfs), will create a HDFS policy
            - If C(hive), will create a HIVE policy
            - If C(kafka), will create a KAFKA policy
            - If C(knox), will create a KNOX policy
            - If C(yarn), will create a YARN policy
        required: true
        choices: [hbase, hdfs, hive, kafka, knox, yarn]
    state:
        description:
            - C(present)
            - C(absent)
        default: present
    service_name:
        description:
            - This is the service name of the policy
        required: true
    policy_name:
        description:
            - This is the policy name
        required: true
    description:
        description:
            - This is the description of the policy
        required: false
    resources:
        description:
            - This is the resources affected by the policy
        required: true
    accesses:
        description:
            - This is the permissions applied by the policy on the resources
        required: true
    users:
        description:
            - This is the array of the users concerned by the policy
        required: false
    groups:
        description:
            - This is the array of the groups concerned by the policy
        required: false
    delegate_admin:
        description:
            - This is the delegate admin of the policy
        required: false
        default: false
    is_recursive:
        description:
            - This is the recursivity of the policy
        required: false
        default: false
    is_enabled:
        description:
            - This is the enable of the policy
        required: false
        default: true
    is_audit_enabled:
        description:
            - This is the audit enable of the policy
        required: false
        default: true

extends_documentation_fragment: bigdata

author:
    - Eric Deleforterie (@https://github.com/EricDele)
'''

EXAMPLES = '''
# Create a policy
- name: Create a hdfs policy
  ranger_policy:
    admin_url: "http://127.0.0.1:6080"
    ranger_user: "raj_ops"
    ranger_user_password: "raj_ops"
    policy_type: "hdfs"
    service_name: "Sandbox_hadoop"
    policy_name: "lake_test"
    description: "Policy test"
    resources:
        - /lake/test
        - /lake/data
    accesses: "rwx"
    users: 
        - it1

'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import generic_urlparse, urlparse
from ansible.module_utils.api import Api
from ansible.module_utils.ranger import RangerApi


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        admin_url=dict(type='str', required=False, deafult='https://localhost:6082'),
        ranger_user=dict(type='str', required=True),
        ranger_user_password=dict(type='str', required=True),
        policy_type=dict(choices=['hbase', 'hdfs', 'hive', 'kafka', 'knox', 'yarn'], required=True, default=None),
        service_name=dict(type='str', required=True),
        policy_name=dict(type='str', required=True),
        state=dict(type='str', required=False, default='present'),
        description=dict(type='str', required=False),
        resources=dict(type='list', required=False),
        accesses=dict(type='str', required=False),
        users=dict(type='list', required=False),
        groups=dict(type='list', required=False),
        delegate_admin=dict(type='bool', required=False, default=False),
        is_recursive=dict(type='bool', required=False, default=False),
        is_enabled=dict(type='bool', required=False, default=True),
        is_audit_enabled=dict(type='bool', required=False, default=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    urlParts = generic_urlparse(urlparse(module.params['admin_url']))
    rangerApi = RangerApi(urlParts['scheme'], urlParts['hostname'], str(urlParts['port']), "basic")
    rangerApi.setCredentialsBasic(module.params['ranger_user'], module.params['ranger_user_password'])
    if(module.params['state'] == "present"):
        rangerApi.postApplyPolicy(policyTemplateType = module.params['policy_type'],
                                  serviceName = module.params['service_name'],
                                  policyName = module.params['policy_name'],
                                  description = module.params['description'],
                                  resources = module.params['resources'],
                                  isRecursive = module.params['is_recursive'],
                                  users = module.params['users'],
                                  groups = module.params['groups'],
                                  accesses = module.params['accesses'])
    if(module.params['state'] == "absent"):
        rangerApi.deleteDeletePolicyByServiceAndPolicyName(module.params['service_name'], module.params['policy_name'])
    
    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    # TODO
    # if module.params['new']:
    #     result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # TODO
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
