#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_run_any_rest_call
short_description: Allows customers to run, CSM REST call that may not be supported by other modules.
description:
  - Returns the result of the requested action against a CSM REST task.
version_added: "1.0.0"
author: Dominic Blea (@dblea00)
options:
  url:
    description:
      - url for the csm server and the rest call the user wants to run
    required: true
    type: str
  data:
    description:
      - Dictionary of variables used in the body of a REST call. {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
    required: true
    type: dict
  headers:
    description:
      - Dictionary of variables used in the headers of a REST call except for the token. {"Accept-Language": properties["language"]}
    type: dict
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Run rest delete
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    url: https://localhost:9234/CSM/web/sessions/test_session
    header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest get
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    url: https://localhost:9234/CSM/web/system/logpackages
    header: header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest put
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    url: https://localhost:9234/CSM/web/sessions/byvolgroup
    data: {"volgroup": test session,
        "type": snap,
        "description": example test session}
    header: header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest post
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    url: https://localhost:9234/CSM/web/storagedevices/12
    data: {"location": New York}
    header: header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec


class RestCallManager(CSMClientBase):
    def _delete(self):
        return self.system_client.rest_delete(self.params['url'], self.params['data'], self.params['headers'])

    def _post(self):
        return self.session_client.run_scheduled_task_at_time(self.params['url'],
                                                              self.params['data'], self.params['headers'])

    def _put(self):
        return self.session_client.enable_scheduled_task(self.params['url'],
                                                         self.params['data'], self.params['headers'])

    def _get(self):
        return self.session_client.enable_scheduled_task_at_time(self.params['url'],
                                                                 self.params['data'], self.params['headers'])



def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(url=dict(type='str', required=True),
                         data=dict(type='dict', required=True),
                         headers=dict(type='dict'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rest_call_manager = RestCallManager(module)

    result = rest_call_manager.perform_task_action()

    module.exit_json(changed=rest_call_manager.changed, result=result.json())


if __name__ == '__main__':
    main()
