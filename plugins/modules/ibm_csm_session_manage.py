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
    volume_group: 'rgroup1'
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


class SessionManager(CSMClientBase):
    def _create_or_update_session(self):
        query_result = self.session_client.get_session_info(self.params['name']).json()
        if query_result['msg'] == 'IWNR1502E':
            return self.session_client.create_session(self.params['name'], self.params['type'],
                                                      self.params['description'])
        else:
            return self.session_client.modify_session_description(self.params['name'], self.params['description'])

    def _create_session_by_volume_group(self):
        return self.session_client.create_session_by_volgroup_name(self.params['volume_group'], self.params['type'],
                                                                   self.params['description'])

    def _delete_session(self):
        return self.session_client.delete_session(self.params['name'])

    def manage_session(self):
        if self.params['state'] == 'present':
            if self.params['name'] is None:
                return self._create_session_by_volume_group()
            else:
                return self._create_or_update_session()
        if self.params['state'] == 'absent':
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
                                                        'MMPracticeOneSiteSVC'
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

    result = session_manager.manage_session()

    module.exit_json(changed=session_manager.changed, result=result.json())


if __name__ == '__main__':
    main()
