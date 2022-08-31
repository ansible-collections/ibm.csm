#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_copyset_manage
short_description: Allows customers to create or delete copy sets on CSM sessions
description:
  - Returns the result of the command for the session specified
version_added: "1.0.0"
author: Randy Blea (@blearandy)
options:
  name:
    description:
      - The name for the session.
    type: str
    required: true
  role_order:
    description:
      - List of the roles depicting the order of the volumes input for each copy set.
      - Ignored when state is absent
    type: str  
  state:
    description:
      - Indicates whether to create or delete the copy sets.
    type: str
    default: present
    choices:
      - present
      - absent
  copysets:
    description:
      - List of all copy sets in the session to be managed.  A copy set is a list of one or more volumes.
    type: str
    required: true
  
  force:
    description:
      - If true the copy set will be removed from the session even if there are errors on the hardware
      - Only valid when state is absent
    type: bool
    default: False
    
  keeponhw:
    description:
      - If true, the base hardware relationship will remain on the hardware but the copy set will be removed from the session
      - Only valid when state is absent
    type: bool
    default: False
    
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Create two copy sets
  ibm.csm.ibm_csm_copyset_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'mysessname'
    state: 'present'
    role_order: "['H1', 'H2']"
    copysets: "[['DS8000:2107.KTLM1:VOL:0001','DS8000:2107.KTLM1:VOL:0101'],
                ['DS8000:2107.GXZ91:VOL:D004','DS8000:2107.GXZ91:VOL:D005']]"

- name: Delete two copy sets
  ibm.csm.ibm_csm_copyset_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'mysessname'
    state: 'absent'
    copysets: "['DS8000:2107.KTLM1:VOL:0001','DS8000:2107.GXZ91:VOL:D004']"
    
- name: Force delete two copy sets from the session
  ibm.csm.ibm_csm_copyset_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'mysessname'
    state: 'absent'
    copysets: "['DS8000:2107.KTLM1:VOL:0001','DS8000:2107.GXZ91:VOL:D004']"
    force: True
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec, ABSENT, PRESENT
from ansible.module_utils._text import to_native
import json


class CopysetManager(CSMClientBase):
    def _create_copysets(self):
        create_result = self.session_client.add_copysets(self.params['name'], self.params['copysets'],
                                                         self.params['role_order'])

        # were the copy sets created
        json_result = create_result.json()
        if json_result['msg'].endswith('E'):
            # set the call to failed if there is any E message
            # This does not handle true idempotency as a single volume in the copy set might be in another session
            # Use the force = True boolean to force idempotency
            self._handle_error("Failed to create the copy sets."
                               "ERR: {error}".format(error=to_native(json_result['msgTranslated'])),
                               json_result)

        else:
            self.changed = True

        return json_result

    def _delete_copysets(self):
        delete_result = self.session_client.remove_copysets(self.params['name'], self.params['copysets'],
                                                            self.params['force'], self.params['keeponhw'])

        json_result = delete_result.json()
        if json_result['msg'].endswith('E'):
            # set the call to failed if there is any E message
            self._handle_error("Failed to delete session {name}. ERR: {error}"
                               .format(name=self.params['name'],
                                       error=to_native(json_result['msgTranslated'])), json_result)

        else:
            self.changed = True

        return json_result

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

    def manage_copysets(self):
        if self.params['state'] == PRESENT:
            return self._create_copysets()

        if self.params['state'] == ABSENT:
            return self._delete_copysets()


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(name=dict(type='str', required=True),
                         role_order=dict(type='str'),
                         state=dict(type='str', default=PRESENT, choices=[ABSENT, PRESENT]),
                         copysets=dict(type='str'),
                         force=dict(type='bool', default=False),
                         keeponhw=dict(type='bool', default=False))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    copyset_manager = CopysetManager(module)

    try:
        result = copyset_manager.manage_copysets()
        if copyset_manager.failed:
            module.fail_json(changed=copyset_manager.changed, result=result)
        else:
            module.exit_json(changed=copyset_manager.changed, result=result)
    except Exception as e:
        copyset_manager.module.fail_json(msg="Module failed. Error [%s]." % to_native(e))


if __name__ == '__main__':
    main()
