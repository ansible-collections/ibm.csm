# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

'''Python versions supported: >= 3.10'''

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import abc
import traceback

from ansible.module_utils import six
from ansible.module_utils.basic import missing_required_lib

PYCSM_IMP_ERR = None
try:
    from pyCSM.clients.session_client import sessionClient
    from pyCSM.clients.hardware_client import hardwareClient
    from pyCSM.clients.system_client import systemClient

    HAS_PYCSM = True
except ImportError:
    PYCSM_IMP_ERR = traceback.format_exc()
    HAS_PYCSM = False

PRESENT = 'present'
ABSENT = 'absent'

properties = {
    "language": "en-US",
    "verify": False,
    # "cert": None
}


@six.add_metaclass(abc.ABCMeta)
class CSMClientBase(object):
    def __init__(self, module):

        if not HAS_PYCSM:
            module.fail_json(msg=missing_required_lib('pyCSM'), exception=PYCSM_IMP_ERR)

        self.module = module
        self.params = module.params
        self.hostname = module.params['hostname']
        self.username = module.params['username']
        self.password = module.params['password']
        self.port = module.params['port']
        self.call_properties = module.params['call_properties']

        self.session_client = self.connect_to_session_api()
        self.hardware_client = self.connect_to_hw_api()
        self.system_client = self.connect_to_system_api()
        self.changed = False
        self.failed = False

    def connect_to_session_api(self):

        session_client = sessionClient(server_address=self.hostname, server_port=self.port, username=self.username,
                                       password=self.password)
        session_client.change_properties(self.call_properties)

        return session_client

    def connect_to_hw_api(self):

        hw_client = hardwareClient(server_address=self.hostname, server_port=self.port, username=self.username,
                                   password=self.password)
        hw_client.change_properties(self.call_properties)

        return hw_client

    def connect_to_system_api(self):

        system_client = systemClient(server_address=self.hostname, server_port=self.port, username=self.username,
                                     password=self.password)
        system_client.change_properties(self.call_properties)

        return system_client


def csm_argument_spec():
    return dict(
        hostname=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', no_log=True, required=True),
        port=dict(type='int', required=False, default=9559),
        call_properties=dict(type='dict', required=False, default=properties)
    )
