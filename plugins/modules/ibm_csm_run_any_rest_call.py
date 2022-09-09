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
  path_resource:
    description:
      - path_resource is the part of the request url that determines the resource for the rest call to run.
    required: true
    type: str
  action:
    description:
      - The action to run against the scheduled task  ('put', 'post', 'get', 'delete')
    required: true
    type: str
  data:
    description:
      - Dictionary of variables used in the body of a REST call. {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
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
    path_resource: sessions/test_session
    action: delete
    header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest get
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    path_resource: system/logpackages
    action: get
    header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest put
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    path_resource: sessions/byvolgroup
    action: put
    data: {"volgroup": test session,
        "type": snap,
        "description": example test session}
    header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}

- name: Run rest post
  ibm.csm.ibm_csm_run_any_rest_call:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    path_resource: storagedevices/12
    action: post
    data: {"location": New York}
    header: {"Accept-Language": en-US,
        "X-Auth-Token": token,
        "Content-Type": "application/x-www-form-urlencoded"}
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec


class RestCallManager(CSMClientBase):
    def _delete(self):
        return self.system_client.rest_delete(self._build_url(),
                                              self.params['data'], self.params['headers'])

    def _post(self):
        return self.system_client.rest_post(self._build_url(),
                                            self.params['data'], self.params['headers'])

    def _put(self):
        return self.system_client.rest_put(self._build_url(),
                                           self.params['data'], self.params['headers'])

    def _get(self):
        return self.system_client.rest_get(self._build_url(),
                                           self.params['data'], self.params['headers'])

    def perform_rest_action(self):
        if self.params['action'] == 'delete':
            return self._delete()
        if self.params['action'] == 'put':
            return self._put()
        if self.params['action'] == 'post':
            return self._post()
        if self.params['action'] == 'get':
            return self._get()

    def _build_url(self):
        return 'https://' + self.params['hostname'] + ':/CSM/web/' + self.params['path_resource']

def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(path_resource=dict(type='str', required=True),
                         action=dict(type='str', required=True),
                         data=dict(type='dict'),
                         headers=dict(type='dict'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    rest_call_manager = RestCallManager(module)

    result = rest_call_manager.perform_rest_action()

    module.exit_json(changed=rest_call_manager.changed, result=result.json())


if __name__ == '__main__':
    main()
