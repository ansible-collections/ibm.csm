# -*- coding: utf-8 -*-

# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    # Parameters for IBM CSM modules
    DOCUMENTATION = r'''
options:
  hostname:
    description:
    - The hostname or IP address of the CSM Server.
    required: true
    type: str
  username:
    description:
    - The username for the CSM server.
    required: true
    type: str
  password:
    description:
    - The password for the username on the CSM server.
    required: true
    type: str
  port:
    description:
    - The port number for the connection to the CSM server.
    type: int
    default: 9559
  call_properties
    description:
    - List of changeable options when creating a connection to the cSM server.
    type: dict
requirements:
  - pyCSM >= 1.0.0
  - python >= 3.6
'''
