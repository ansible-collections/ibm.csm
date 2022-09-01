#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_active_standby_action
short_description: Allows customers to set the server as a standby, issue a takeover, or remove the associated server
description:
  - Returns the result of the requested action against a CSM server
version_added: "1.0.0"
author: Randy Blea (@blearandy)
options:
  csm_server:
    description:
      - The name of the CSM serer this is or wil be the active or standby.
    type: str
  action:
    description:
      - The action to run. ('set_server_as_standby', 'takeover', 'remove')
    required: true
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Set server {{ csm_host }} as a standby to serverA
  ibm.csm.ibm_csm_active_standby_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    csm_server: 'serverA'
    action: 'set_server_as_standby'

- name: Issue a takeover to make {{ csm_host }} an active server
  ibm.csm.ibm_csm_active_standby_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    action: 'takeover'

- name: Remove serverB as a standby to {{ csm_host }}
  ibm.csm.ibm_csm_active_standby_action:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    csm_server: 'serverB'
    action: 'remove'
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec
from ansible.module_utils._text import to_native
import json


class ActiveStandbyManager(CSMClientBase):

    def _set_server_as_standby(self):
        return self.system_client.set_server_as_standby(self.params['csm_server'])

    def _takeover(self):
        return self.system_client.takeover_standby_server()

    def _remove(self):
        return self.system_client.remove_active_or_standby_server(self.params['csm_server'])

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

    def perform_active_standby_action(self):
        if self.params['action'] == 'set_server_as_standby':
            result = self._set_server_as_standby()
        elif self.params['action'] == 'takeover':
            result = self._takeover()
        elif self.params['action'] == 'remove':
            result = self._remove()

        json_result = result.json()
        if json_result['msg'].endswith('E'):
            # set the call to failed if there is any E message
            self._handle_error("Failed the task command. ERR: {error}".format(
                error=to_native(json_result['msgTranslated'])), json_result)

        return json_result


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(csm_server=dict(type='str'),
                         action=dict(type='str', required=True,
                                     choices=['set_server_as_standby', 'takeover', 'remove']))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    active_standby_manager = ActiveStandbyManager(module)

    try:
        result = active_standby_manager.perform_active_standby_action()
        if active_standby_manager.failed:
            module.fail_json(changed=active_standby_manager.changed, result=result)
        else:
            module.exit_json(changed=active_standby_manager.changed, result=result)
    except Exception as e:
        active_standby_manager.module.fail_json(msg="Module failed. Error [%s]." % to_native(e))


if __name__ == '__main__':
    main()
