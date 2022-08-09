#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_scheduled_task_action
short_description: Allows customers to run, enable or disable a CSM scheduled task
description:
  - Returns the result of the requested action against a CSM scheduled task.
version_added: "1.0.0"
author: Randy Blea (@blearandy)
options:
  id:
    description:
      - The id for the task to issue the action against
    required: true
    type: str
  action:
    description:
      - The action to run against the scheduled task  ('run', 'enable', 'disable')
    required: true
    type: str
  synchronous:
    description:
      - Valid when action is 'run'.  If True, won't return from call until task has completed the run.
    type: bool
    default: False
  at_time:
    description:
      - Specify this value to run the task at a certain time.  Leave off to run now. Format of yyyy-MM-dd'T'HH-mm
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Run the task immediately
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: scheduled_task_id
    action: 'run'
    
- name: Run the task immediately and do not return until complete
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: scheduled_task_id
    action: 'run'
    synchronous: True

- name: Run the task at the specified time
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: scheduled_task_id
    action: 'run'
    at_time: '2022-08-09T17-15'
    
- name: Enable the task now
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: 2
    action: 'enable'
    
- name: Enable the task at the specified time
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: 2
    action: 'enable'
    at_time: '2022-08-09T17-30'
    
- name: Disable the task 
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: 2
    action: 'disable'
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec


class ScheduledTaskManager(CSMClientBase):
    def _run_task_now(self):
        if self.params['synchronous']:
            return self.session_client.run_scheduled_task(self.params['id'], True)
        else:
            return self.session_client.run_scheduled_task(self.params['id'], False)

    def _run_task_at_time(self):
        return self.session_client.run_scheduled_task_at_time(self.params['id'], self.params['at_time'])

    def _enable_task(self):
        return self.session_client.enable_scheduled_task(self.params['id'])

    def _enable_task_at_time(self):
        return self.session_client.enable_scheduled_task_at_time(self.params['id'], self.params['at_time'])

    def _disable_task(self):
        return self.session_client.disable_scheduled_task(self.params['id'])

    def perform_task_action(self):
        if self.params['action'] == 'run':
            if self.params['at_time'] is None:
                return self._run_task_now()
            else:
                return self._run_task_at_time()
        if self.params['action'] == 'enable':
            if self.params['at_time'] is None:
                return self._enable_task()
            else:
                return self._enable_task_at_time()
        if self.params['action'] == 'disable':
            return self._disable_task()



def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(id=dict(type='str'), action=dict(type='str'),
                         synchronous=dict(type='bool'), at_time=dict(type='str'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    scheduled_task_manager = ScheduledTaskManager(module)

    result = scheduled_task_manager.perform_task_action()

    module.exit_json(changed=scheduled_task_manager.changed, result=result.json())


if __name__ == '__main__':
    main()
