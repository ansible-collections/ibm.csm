#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_session_action
short_description: Allows customers to issue commands to sessions on the CSM server
description:
  - Returns the result of the requested action against a CSM server
version_added: "1.0.0"
author: Randy Blea (@blearandy)
options:
  name:
    description:
      - The name of the CSM session the command will be issued to.
    type: str
    required: true
  command:
    description:
      - The command to issue to the session
    required: true
    type: str
  backup_id:
    description:
      - The backup ID or snapshot ID required for some commands to Safeguarded Copy or Snapshot sessions
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Issue a start command to a session
  ibm.csm.ibm_csm_session_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'sessionA'
    command: 'Start H1->H2'

- name: Recover a Safeguarded Copy session to a given backup
  ibm.csm.ibm_csm_session_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'mysgcsess'
    command: 'Recover Backup'
    backup_id: '1662577200'
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec
from ansible.module_utils._text import to_native
import json


class SessionCommandManager(CSMClientBase):

    def _run_session_command(self):
        return self.session_client.run_session_command(self.params['name'], self.params['command'])

    def _run_backup_command(self):
        return self.session_client.run_backup_command(self.params['name'], "H1", self.params['backup_id'],
                                                      self.params['command'])

    def _handle_error(self, msg, server_result=None):
        result = {'msg': msg}
        self.failed = True
        if server_result is None:
            server_result = {'result': "No server result returned"}
        self.module.fail_json(
            msg=result['msg'],
            server_result={'server_result': server_result}
        )
        return json.dumps(result, indent=4)

    def perform_session_command_action(self):
        if self.params['backup_id'] is None:
            result = self._run_session_command()
        else:
            result = self._run_backup_command()

        json_result = result.json()
        if json_result['msg'].endswith('E'):
            # set the call to failed if there is any E message
            self._handle_error("Failed the task command. ERR: {error}".format(
                error=to_native(json_result['msgTranslated'])), json_result)

        return json_result


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(name=dict(type='str', required=True),
                         command=dict(type='str', required=True),
                         backup_id=dict(type='str'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    session_command_manager = SessionCommandManager(module)

    try:
        result = session_command_manager.perform_session_command_action()
        if session_command_manager.failed:
            module.fail_json(changed=session_command_manager.changed, result=result)
        else:
            module.exit_json(changed=session_command_manager.changed, result=result)
    except Exception as e:
        session_command_manager.module.fail_json(msg="Module failed. Error [%s]." % to_native(e))


if __name__ == '__main__':
    main()
