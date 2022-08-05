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
    type: str
  action:
    description:
      - The action to run against the scheduled task  ('run', 'enable', 'disable')
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment:
  - ibm.csm.ibm_csm_client.documentation
'''

EXAMPLES = r'''
- name: Run the backup task immediately
  ibm.csm.ibm_csm_scheduled_task_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    id: scheduled_task_id
    action: 'run'
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec


class ScheduledTaskManager(CSMClientBase):
    def run_action_now(self):
        if self.params['action'] == 'run':
            kwargs = dict(
                taskid=self.params['id'],
                synchronous=self.params[False]
            )
            return self.session_client.run_scheduled_task(**kwargs)


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(id=dict(type='str'), action=dict(type='str'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    scheduled_task_manager = ScheduledTaskManager(module)

    result = scheduled_task_manager.run_action_now()

    module.exit_json(changed=scheduled_task_manager.changed, result=result)


if __name__ == '__main__':
    main()
