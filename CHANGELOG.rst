==================================================
IBM CSM Ansible collection changelog Release Notes
==================================================

.. contents:: Topics


v1.1.0
======

Release Summary
---------------

Modernization release adding ansible-core 2.15+ support, token authentication
documentation, ``wait_for_state`` for session commands, ``cancel`` and
``delete`` actions for scheduled tasks, and several bug fixes.

Minor Changes
-------------

- Add sanity ignore files for ansible-core 2.16 and 2.17 to match the updated CI test matrix.
- Bump minimum required ansible-core version from 2.9.10 to 2.15.0.
- Bump minimum required pyCSM version from 1.0.1 to 1.0.11.
- Replace the deprecated ``ansible.module_utils.six`` compatibility shims with their Python standard library equivalents. ``ansible.module_utils.six`` is deprecated in ansible-core 2.21 and is scheduled for removal in 2.24.
- Update CI test matrix to cover ansible-core 2.15, 2.16, 2.17, and devel. Versions 2.10 through 2.14 have reached end-of-life and are removed.
- ibm_csm_client - Remove stale ``#JJW`` development comments and fix associated pep8 style violations (E261, E262) introduced with the token authentication feature.
- ibm_csm_scheduled_task_action - Add ``cancel`` and ``delete`` choices to the ``action`` option, allowing a running task to be cancelled or a scheduled task to be permanently deleted.
- ibm_csm_scheduled_task_action - Remove trailing whitespace (W293/W291).
- ibm_csm_session_action - Add ``wait_for_state`` and ``wait_minutes`` options. When ``wait_for_state`` is specified the module blocks after issuing the session command until the session reaches the given state or the timeout is exceeded (default 10 minutes).

Bugfixes
--------

- csm_client_fragment - Document the ``token`` parameter and mark ``password`` as optional (required only when ``token`` is not provided). Fixes ``undocumented-parameter``, ``parameter-type-not-in-doc``, and ``doc-required-mismatch`` sanity failures introduced by the token authentication feature.
- ibm_csm_session_manage - Fix idempotency bug where deleting a session that does not exist (IWNR1024E) incorrectly reported ``changed`` as true. The module now correctly returns ``changed`` as false for a no-op delete.
- meta/runtime.yml - Add missing ``action_groups`` declaration for ``ibm_csm_client``. Without this the ``group/ibm.csm.ibm_csm_client`` ``module_defaults`` shorthand used in integration tests (and by end users) raised an unresolvable group error.

v1.0.0
======

Release Summary
---------------

This is the first official release of the ``ibm.csm`` collection.
This changelog contains all changes to the modules and plugins in this collection
that have been made since the pre-release.

New Modules
-----------

- ibm_csm_active_standby_action - Allows customers to set the server as a standby, issue a takeover, or remove the associated server
- ibm_csm_copyset_manage - Allows customers to create or delete copy sets on CSM sessions
- ibm_csm_info - Retrieves current environment information from CSM server
- ibm_csm_run_any_rest_call - Allows customers to run, CSM REST call that may not be supported by other modules.
- ibm_csm_scheduled_task_action - Allows customers to run, enable or disable a CSM scheduled task
- ibm_csm_session_action - Allows customers to issue commands to sessions on the CSM server
- ibm_csm_session_manage - Allows customers to create, delete or modify CSM sessions

v0.1.0
======

Release Summary
---------------

This is the pre-release of the ``ibm.csm`` collection.
