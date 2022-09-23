#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_session_manage
short_description: Allows customers to create, delete or modify CSM sessions
description:
  - Returns the result of the command for the session specified
version_added: "1.0.0"
author: Randy Blea (@blearandy)
options:
  name:
    description:
      - The name for the session.
      - Required when volume_group is not specified.
    type: str
  description:
    description:
      - The description to set when the session is created or modified.
    type: str
  type:
    description:
      - The type of the session that will be created.
      - Required when creating the session.
    type: str
    choices:
      - ESESizer
      - FC
      - Snapshot
      - SGC
      - SGCSVC
      - SnapshotSVC
      - Migration
      - MMBasic
      - MM
      - MMPracticeOneSite
      - MMPracticeOneSiteSVC
      - MMCVSVC
      - GMBasic
      - GMBasicSVC
      - GM
      - GMSVC
      - GMPracticeOneSiteSVC
      - GMPracticeOneSite
      - GMPracticeTwoSite
      - GMCVSVC
      - GMTwoSite
      - GMTwoSiteWithSite3
      - MGM
      - MGMPRacticeOneSite
      - MT_MM_MM
      - MT_MM_GM
      - MT_MM_GMPractice
      - MT_MM_GM_Site3GM
      - MT_MM_GM_4Site
      - MT_MM_MM_4Site
  state:
    description:
      - Specify the state of the session. This indicates whether the session should exist and not the replication state.
    type: str
    default: present
    choices:
      - present
      - absent
  volume_group:
    description:
      - The name of a hardware volume group that will be tied to the session
      - Required when name is not specified.
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Create a Three Site MM-GM session
  ibm.csm.ibm_csm_session_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'my_three_site_sess'
    description: 'this session manages my replication across three sites'
    type: 'MT_MM_GM'
    state: 'present'

- name: Delete my three site session
  ibm.csm.ibm_csm_session_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'my_three_site_sess'
    state: 'absent'

- name: Create a Spectrum Virtualize Snapshot session from a volume group
  ibm.csm.ibm_csm_session_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    state: 'present'
    volume_group: 'SPECTRUM-VIRTUALIZE:VOLGROUP:FAB3-DEV13:rgroup_01'
    type: 'SnapshotSVC'

- name: Update the description for a session
  ibm.csm.ibm_csm_session_manage:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    name: 'my_three_site_sess'
    state: 'present'
    description: 'this session manages replication to Los Angeles and New York'
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec, ABSENT, PRESENT
from ansible.module_utils._text import to_native
import json


class SessionManager(CSMClientBase):
    def _create_or_update_session(self):
        if self.params['type'] is not None:
            create_result = self.session_client.create_session(self.params['name'], self.params['type'],
                                                               self.params['description'])
        elif self.params['description'] is not None:
            create_result = self.session_client.modify_session_description(self.params['name'],
                                                                           self.params['description'])
        else:
            return self._handle_error("Failed to create the session {name} or modify the description. "
                                      "Type is required when creating the session and description "
                                      "is required when modifying the session. "
                                      .format(name=self.params['name']))

        # was the session created or modified
        json_result = create_result.json()
        if json_result['msg'].endswith('E') and json_result['msg'] != 'IWNR1019E':
            # set the call to failed if there is any E message other than IWNR1019E (already exists)
            self._handle_error("Failed to create the session {name} or modify the description. "
                               "ERR: {error}".format(name=self.params['name'],
                                                     error=to_native(json_result['msgTranslated'])),
                               json_result)

        else:
            self.changed = True

        return json_result

    def _create_session_by_volume_group(self):
        create_result = self.session_client.create_session_by_volgroup_name(self.params['volume_group'],
                                                                            self.params['type'],
                                                                            self.params['description'])

        json_result = create_result.json()
        if json_result['msg'].endswith('E') and json_result['msg'] != 'IWNR1019E':
            # set the call to failed if there is any E message other than IWNR1019E (already exists)
            self._handle_error("Failed to create the session {name}. ERR: {error}".format(
                name=self.params['name'], error=to_native(json_result['msgTranslated'])), json_result)
        else:
            self.changed = True

        return json_result

    def _delete_session(self):
        delete_result = self.session_client.delete_session(self.params['name'])

        json_result = delete_result.json()
        if json_result['msg'].endswith('E') and json_result['msg'] != 'IWNR1024E':
            # set the call to failed if there is any E message
            self._handle_error("Failed to delete session {name}. ERR: {error}"
                               .format(name=self.params['name'],
                                       error=to_native(json_result['msgTranslated'])), json_result)

        else:
            self.changed = True

        return json_result

    def _handle_error(self, msg, server_result=None):
        create_result = {'msg': msg}
        self.failed = True
        if server_result is None:
            server_result = {'result': "No server result returned"}
        self.module.fail_json(
            msg=create_result['msg'],
            server_result={'server_result': server_result}
        )
        return json.dumps(create_result, indent=4)

    def manage_session(self):
        if self.params['state'] == PRESENT:
            if self.params['name'] is None:
                return self._create_session_by_volume_group()
            else:
                return self._create_or_update_session()

        if self.params['state'] == ABSENT:
            return self._delete_session()


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(name=dict(type='str'),
                         description=dict(type='str'),
                         type=dict(type='str', choices=['ESESizer',
                                                        'FC',
                                                        'Snapshot',
                                                        'SGC',
                                                        'SGCSVC',
                                                        'SnapshotSVC',
                                                        'Migration',
                                                        'MMBasic',
                                                        'MM',
                                                        'MMPracticeOneSite',
                                                        'MMPracticeOneSiteSVC',
                                                        'MMCVSVC',
                                                        'GMBasic',
                                                        'GMBasicSVC',
                                                        'GM',
                                                        'GMSVC',
                                                        'GMPracticeOneSiteSVC',
                                                        'GMPracticeOneSite',
                                                        'GMPracticeTwoSite',
                                                        'GMCVSVC',
                                                        'GMTwoSite',
                                                        'GMTwoSiteWithSite3',
                                                        'MGM',
                                                        'MGMPRacticeOneSite',
                                                        'MT_MM_MM',
                                                        'MT_MM_GM',
                                                        'MT_MM_GMPractice',
                                                        'MT_MM_GM_Site3GM',
                                                        'MT_MM_GM_4Site',
                                                        'MT_MM_MM_4Site']),
                         state=dict(type='str', default=PRESENT, choices=[ABSENT, PRESENT]),
                         volume_group=dict(type='str'))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    session_manager = SessionManager(module)

    try:
        result = session_manager.manage_session()
        if session_manager.failed:
            module.fail_json(changed=session_manager.changed, result=result)
        else:
            module.exit_json(changed=session_manager.changed, result=result)
    except Exception as e:
        session_manager.module.fail_json(msg="Module failed. Error [%s]." % to_native(e))


if __name__ == '__main__':
    main()
