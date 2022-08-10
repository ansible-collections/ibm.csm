#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ibm_csm_info
short_description: Retrieves current environment information from CSM server
description:
  - Returns a list of specified CSM Server object(s) including Sessions,
    Task Schedules, Copysets, Hardware, CSM System and Authorization.
version_added: "1.0.0"
author: Tom Zito (@twzito)
options:
  backup_id:
    description:
      - The ID number of the backup. (example - 1659891600)
    type: int
  count:
    description:
      - The number of messages to return.
    type: int
  device_id:
    description:
      - The ID of the storage system. The cluster name on a FlashSystem. (example - lbsfs5200A)
    type: str
  device_type:
    description:
      - The type of storage device (example - ds8000 or svc).
    type: str
  gather_subset:
    choices:
      - all
      - copyset_list
      - copyset_pair_list
      - hardware_device_list
      - hardware_path_list
      - hardware_svchosts_list
      - hardware_volume_list_by_wwn
      - hardware_volume_list_by_system
      - scheduled_task_list
      - session_backup_detail
      - session_command_list
      - session_detail
      - session_list
      - session_list_short
      - session_option_list
      - session_recovered_backup_detail
      - session_recovered_backup_list
      - session_rolepair_list
      - session_snapshot_clone_detail
      - session_snapshot_clone_list
      - session_snapshot_detail
      - system_log_event_list
      - system_log_packages_list
      - system_session_supported_list
      - system_version_list
    default: all
    description:
      - List of string variables to specify the CSM objects to retrieve info for.
      - all - list all objects that have their required options satisfied.
      - copyset_list - Lists copysets for a given session.  The 'name' option is required.
      - copyset_pair_list - List the pairs for the session in a given role pair.
                            The 'name' and 'rolepair' options are required.
      - hardware_device_list - Lists all the storagedevices of a given type.
                               The 'device_type' option is required.
      - hardware_path_list - List all logical paths on a given DS8000 storage system.
                             The 'system_id' option will limit results to a single DS8000.
      - hardware_svchosts_list - List the hosts defined on the SVC based storage system.
                                 The 'device_id' option is required.
      - hardware_volume_list_by_wwn - List volumes for a given WWN.
                                      The 'wwn_name' option is required.
      - hardware_volume_list_by_system - List volumes for a given storage system.
                                         The 'system_name' option is required.
      - scheduled_task_list - list of scheduled tasks defined on the server.
      - session_backup_detail - Detailed information for a given backup in a session.
                                The 'name', 'role' and 'backup_id' options are required.
      - session_command_list - List of available commands for a session based on the session
                               current state.  The 'name' option is required.
      - session_detail - Detailed information for a session.
                         The 'name' option is required.
      - session_list - Overview summary for sessions managed by the server.
      - session_list_short - Minimal overview summary for sessions managed by the server.
      - session_option_list - Gets the options for the given session. The results returned will vary
                              depending on the session type.
                              The 'name' option is required.
      - session_recovered_backup_detail - Pair information for a recovered backup on a session.
                                          The 'name' and 'backup_id' options are required.
      - session_recovered_backup_list - Lists all recovered backups for Spec V Safeguarded Copy
                                        session.
                                        The 'name' option is required.
      - session_rolepair_list - Summary for a given role pair in a session.
                                The 'name' and 'rolepair' options are required.
      - session_snapshot_clone_detail - Pair details for the thin clone of the specified snapshot.
                                        The 'name' and 'snapshot' options are required.
      - session_snapshot_clone_list - List clones for snapshots in Spec V Safeguarded Copy session.
                                      The 'name' option is required.
      - session_snapshot_detail - Detailed information for a given snapshot in a session.
                                  The 'name', 'role' and 'snapshot' options are required.
      - system_log_event_list - List the most recent log events.
                                The 'count' option is required.  The 'name' option is optional.
      - system_log_packages_list - List the log packages and their location on the server.
      - system_session_supported_list - List the supported session types.
      - system_version_list - The version of the server being called.
      - system_volume_count_list - List the volume usage on the server.
    elements: str
    type: list
  name:
    description:
      - The name of the session. (example - SGC_DB2_LBSFS5200A)
    type: str
  role:
    description:
      - The name of the role where the backup or snapshot resides. (example - H1 or H2)
    type: str
  rolepair:
    description:
      - The name of the role pair. (example - H1-B1 or H1-R1)
    type: str
  snapshot:
    description:
      - The name of the session snapshot.  (example - snapshot0)
    type: str
  system_id:
    description:
      - The ID of the DS8000 storage system. (example - 2107.DYR51)
    type: str
  system_name:
    description:
      - The name of the storage system. (example - 2107.DYR51 for DS8000 or lbsfs5200A for FlashSystem)
    type: str
  wwn_name:
    description:
      - The WWN, full or partial, to search for. (example - 6005076812810039f8000000000000)
    type: str
notes:
  - Supports C(check_mode).
extends_documentation_fragment: ibm.csm.csm_client_fragment.documentation
'''

EXAMPLES = r'''
- name: Retreive all information that does not require additional options.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset: all

- name: Retreive a short list of sessions and the scheduled tasks.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset:
      - session_list_short
      - scheduled_task_list

- name: Retreive the options and available commands for session EXAMPLE_SESSION.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset:
      - session_command_list
      - session_option_list
    name: EXAMPLE_SESSION

- name: Retreive full info for all sessions and a recovered backup list for session EXAMPLE_SESSION.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset:
      - session_list
      - session_recovered_backup_list
    name: EXAMPLE_SESSION

- name: Retreive full backup information for session EXAMPLE_SESSION, role H1 and backup 1659891600.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset: session_backup_detail
    name: EXAMPLE_SESSION
    role: H1
    backup_id: 1659891600

- name: Retrieve info for WWNs 6005076812810039f800000000000000 - 6005076812810039f8000000000000FF.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset: hardware_volume_list_by_wwn
    wwn: 6005076812810039f8000000000000

- name: Retrieve snapshot and snapshot clone information for a session.
  ibm.csm.ibm_csm_info:
    hostname: "{{ csm_host }}"
    username: "{{ csm_username }}"
    password: "{{ csm_password }}"
    gather_subset:
      - session_snapshot_clone_list
      - session_snapshot_clone_detail
      - session_snapshot_detail
    role: H1
    name: Test_FC2_LBSFS5200A
    snapshot: snapshot0
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.csm.plugins.module_utils.ibm_csm_client import CSMClientBase, csm_argument_spec
from ansible.module_utils._text import to_native
import json


class CSMGatherInfo(CSMClientBase):

    def subset_opt_error(self, subset, option):
        error_msg = "Subset {} failed.  Required parameters and values:".format(subset)
        for key, value in option.items():
            error_msg += "  {}={}".format(key, value)
        self.module.fail_json(msg=error_msg)

    def get_copyset_list(self):
        kwargs = dict(name=self.params['name'])
        try:
            return json.loads(self.session_client.get_copysets(**kwargs).text)
        except ValueError:
            self.subset_opt_error("copyset_list", kwargs)

    def get_copyset_pair_list(self):
        kwargs = dict(name=self.params['name'],
                      rolepair=self.params['rolepair'])
        return json.loads(self.session_client.get_pair_info(**kwargs).text)

    def get_hardware_device_list(self):
        kwargs = dict(device_type=self.params['device_type'])
        return json.loads(self.hardware_client.get_devices(**kwargs).text)

    def get_hardware_path_list(self):
        if self.module.params['system_id'] and len(self.module.params['system_id']) > 0:
            try:
                kwargs = dict(system_id=self.params['system_id'])
                return json.loads(self.hardware_client.get_path_on_storage_system(**kwargs).text)
            except ValueError:
                self.subset_opt_error("hardware_path_list", kwargs)
        else:
            return json.loads(self.hardware_client.get_paths().text)

    def get_hardware_svchosts_list(self):
        kwargs = dict(device_id=self.params['device_id'])
        return json.loads(self.hardware_client.get_svchosts(**kwargs).text)

    def get_hardware_volume_list_by_system(self):
        kwargs = dict(system_name=self.params['system_name'])
        return json.loads(self.hardware_client.get_volumes(**kwargs).text)

    def get_hardware_volume_list_by_wwn(self):
        kwargs = dict(wwn_name=self.params['wwn_name'])
        return json.loads(self.hardware_client.get_volumes_by_wwn(**kwargs).text)

    def get_scheduled_task_list(self):
        return json.loads(self.session_client.get_scheduled_tasks().text)

    def get_session_backup_detail(self):
        kwargs = dict(name=self.params['name'],
                      role=self.params['role'],
                      backup_id=self.params['backup_id'])
        try:
            return json.loads(self.session_client.get_backup_details(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_backup_detail", kwargs)

    def get_session_command_list(self):
        kwargs = dict(name=self.params['name'])
        return json.loads(self.session_client.get_available_commands(**kwargs).text)

    def get_session_detail(self):
        kwargs = dict(name=self.params['name'])
        return json.loads(self.session_client.get_session_info(**kwargs).text)

    def get_session_list(self):
        return json.loads(self.session_client.get_session_overviews().text)

    def get_session_list_short(self):
        return json.loads(self.session_client.get_session_overviews_short().text)

    def get_session_option_list(self):
        kwargs = dict(name=self.params['name'])
        try:
            return json.loads(self.session_client.get_session_options(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_option_list", kwargs)

    def get_session_recovered_backup_detail(self):
        kwargs = dict(name=self.params['name'],
                      backup_id=self.params['backup_id'])
        return json.loads(self.session_client.get_recovered_backup_details(**kwargs).text)

    def get_session_recovered_backup_list(self):
        kwargs = dict(name=self.params['name'])
        return json.loads(self.session_client.get_recovered_backups(**kwargs).text)

    def get_session_rolepair_list(self):
        kwargs = dict(name=self.params['name'],
                      rolepair=self.params['rolepair'])
        try:
            return json.loads(self.session_client.get_rolepair_info(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_rolepair_list", kwargs)

    def get_session_snapshot_clone_detail(self):
        kwargs = dict(name=self.params['name'],
                      snapshot_name=self.params['snapshot'])
        try:
            return json.loads(self.session_client.get_snapshot_clone_details_by_name(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_snapshot_clone_detail", kwargs)

    def get_session_snapshot_clone_list(self):
        kwargs = dict(name=self.params['name'])
        try:
            return json.loads(self.session_client.get_snapshot_clones(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_snapshot_clone_list", kwargs)

    def get_session_snapshot_detail(self):
        kwargs = dict(name=self.params['name'],
                      role=self.params['role'],
                      snapshot_name=self.params['snapshot'])
        try:
            return json.loads(self.session_client.get_snapshot_details_by_name(**kwargs).text)
        except ValueError:
            self.subset_opt_error("session_snapshot_detail", kwargs)

    def get_system_log_event_list(self):
        kwargs = {}
        if self.module.params['count'] and self.module.params['count'] > 0:
            kwargs['count'] = self.module.params['count']
        if self.module.params['name'] and len(self.module.params['name']) > 0:
            kwargs['name'] = self.module.params['name']
        return json.loads(self.system_client.get_log_events(**kwargs).text)

    def get_system_log_packages_list(self):
        return json.loads(self.system_client.get_log_pkgs().text)

    def get_system_session_supported_list(self):
        return json.loads(self.system_client.get_session_types().text)

    def get_system_version_list(self):
        return json.loads(self.system_client.get_server_version().text)

    def get_system_volume_count_list(self):
        return json.loads(self.system_client.get_volume_counts().text)

    def run_query(self):

        # Queries that do not require arguments

        no_opts = ['hardware_path_list', 'scheduled_task_list', 'session_list',
                   'session_list_short', 'system_log_event_list', 'system_log_packages_list',
                   'system_session_supported_list', 'system_version_list',
                   'system_volume_count_list']

        subset = self.module.params['gather_subset']
        if len(subset) == 0 or 'all' in subset:
            subset = no_opts

            # Add the other queries for 'all' if we have the options needed for them.

            if self.module.params['name'] and len(self.module.params['name']) > 0:
                subset.append('copyset_list')
                subset.append('session_command_list')
                subset.append('session_detail')
                subset.append('session_option_list')
                subset.append('session_recovered_backup_list')
                subset.append('session_snapshot_clone_list')

                if self.module.params['rolepair'] and len(self.module.params['rolepair']) > 0:
                    subset.append('copyset_pair_list')
                    subset.append('session_rolepair_list')

                if self.module.params['backup_id'] and self.module.params['backup_id'] > 0:
                    subset.append('session_recovered_backup_detail')

                    if self.module.params['role'] and len(self.module.params['role']) > 0:
                        subset.append('session_backup_detail')

                if self.module.params['snapshot'] and len(self.module.params['snapshot']) > 0:
                    subset.append('session_snapshot_clone_detail')

                    if self.module.params['role'] and len(self.module.params['role']) > 0:
                        subset.append('session_snapshot_detail')

            if self.module.params['device_type'] and len(self.module.params['device_type']) > 0:
                subset.append('hardware_device_list')

            if self.module.params['device_id'] and len(self.module.params['device_id']) > 0:
                subset.append('hardware_svchosts_list')

            if self.module.params['system_name'] and len(self.module.params['system_name']) > 0:
                subset.append('hardware_volume_list_by_system')

            if self.module.params['wwn_name'] and len(self.module.params['wwn_name']) > 0:
                subset.append('hardware_volume_list_by_wwn')

        query_result = {}
        query_result['changed'] = False

        if 'copyset_list' in subset:
            query_result['copyset_list'] = self.get_copyset_list()
        if 'copyset_pair_list' in subset:
            query_result['copyset_pair_list'] = self.get_copyset_pair_list()
        if 'hardware_device_list' in subset:
            query_result['hardware_device_list'] = self.get_hardware_device_list()
        if 'hardware_path_list' in subset:
            query_result['hardware_path_list'] = self.get_hardware_path_list()
        if 'hardware_svchosts_list' in subset:
            query_result['hardware_svchosts_list'] = self.get_hardware_svchosts_list()
        if 'hardware_volume_list_by_system' in subset:
            query_result['hardware_volume_list_by_system'] = self.get_hardware_volume_list_by_system()
        if 'hardware_volume_list_by_wwn' in subset:
            query_result['hardware_volume_list_by_wwn'] = self.get_hardware_volume_list_by_wwn()
        if 'scheduled_task_list' in subset:
            query_result['scheduled_task_list'] = self.get_scheduled_task_list()
        if 'session_backup_detail' in subset:
            query_result['session_backup_detail'] = self.get_session_backup_detail()
        if 'session_command_list' in subset:
            query_result['session_command_list'] = self.get_session_command_list()
        if 'session_detail' in subset:
            query_result['session_detail'] = self.get_session_detail()
        if 'session_list' in subset:
            query_result['session_list'] = self.get_session_list()
        if 'session_list_short' in subset:
            query_result['session_list_short'] = self.get_session_list_short()
        if 'session_option_list' in subset:
            query_result['session_option_list'] = self.get_session_option_list()
        if 'session_recovered_backup_detail' in subset:
            query_result['session_recovered_backup_detail'] = self.get_session_recovered_backup_detail()
        if 'session_recovered_backup_list' in subset:
            query_result['session_recovered_backup_list'] = self.get_session_recovered_backup_list()
        if 'session_rolepair_list' in subset:
            query_result['session_rolepair'] = self.get_session_rolepair_list()
        if 'session_snapshot_clone_detail' in subset:
            query_result['session_snapshot_clone_detail'] = self.get_session_snapshot_clone_detail()
        if 'session_snapshot_clone_list' in subset:
            query_result['session_snapshot_clone_list'] = self.get_session_snapshot_clone_list()
        if 'session_snapshot_detail' in subset:
            query_result['session_snapshot_detail'] = self.get_session_snapshot_detail()
        if 'system_log_event_list' in subset:
            query_result['system_log_event_list'] = self.get_system_log_event_list()
        if 'system_log_packages_list' in subset:
            query_result['system_log_packages_list'] = self.get_system_log_packages_list()
        if 'system_session_supported_list' in subset:
            query_result['system_session_supported_list'] = self.get_system_session_supported_list()
        if 'system_version_list' in subset:
            query_result['system_version'] = self.get_system_version_list()
        if 'system_volume_count_list' in subset:
            query_result['system_volume_count_list'] = self.get_system_volume_count_list()

        self.module.exit_json(**query_result)


def main():
    argument_spec = csm_argument_spec()
    argument_spec.update(
        backup_id=dict(type='int'),
        count=dict(type='int'),
        device_id=dict(type='str'),
        device_type=dict(type='str'),
        gather_subset=dict(type='list', elements='str', required=False,
                           default=['all'],
                           choices=['all',
                                    'copyset_list',
                                    'copyset_pair_list',
                                    'hardware_device_list',
                                    'hardware_path_list',
                                    'hardware_svchosts_list',
                                    'hardware_volume_list_by_wwn',
                                    'hardware_volume_list_by_system',
                                    'scheduled_task_list',
                                    'session_backup_detail',
                                    'session_command_list',
                                    'session_detail',
                                    'session_list',
                                    'session_list_short',
                                    'session_option_list',
                                    'session_recovered_backup_detail',
                                    'session_recovered_backup_list',
                                    'session_rolepair_list',
                                    'session_snapshot_clone_detail',
                                    'session_snapshot_clone_list',
                                    'session_snapshot_detail',
                                    'system_log_event_list',
                                    'system_log_packages_list',
                                    'system_session_supported_list',
                                    'system_version_list',
                                    'system_volume_count_list']),
        name=dict(type='str'),
        role=dict(type='str'),
        rolepair=dict(type='str'),
        snapshot=dict(type='str'),
        system_id=dict(type='str'),
        system_name=dict(type='str'),
        wwn_name=dict(type='str')
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    gather_info = CSMGatherInfo(module)

    try:
        gather_info.run_query()
    except Exception as e:
        gather_info.module.fail_json(msg="Module failed. Error [%s]." % to_native(e))

if __name__ == '__main__':
    main()
