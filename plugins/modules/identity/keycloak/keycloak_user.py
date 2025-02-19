#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, Adam Goossens <adam.goossens@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: keycloak_user

short_description: Allows administration of Keycloak users via Keycloak API

description:
    - This module allows you to add, remove or modify Keycloak users via the Keycloak REST API.
      It requires access to the REST API via OpenID Connect; the user connecting and the client being
      used must have the requisite access rights. In a default Keycloak installation, admin-cli
      and an admin user would work, as would a separate client definition with the scope tailored
      to your needs and a user having the expected roles.

    - The names of module options are snake_cased versions of the camelCase ones found in the
      Keycloak API and its documentation at U(https://www.keycloak.org/docs-api/8.0/rest-api/index.html).

    - Attributes are multi-valued in the Keycloak API. All attributes are lists of individual values and will
      be returned that way by this module. You may pass single values for attributes when calling the module,
      and this will be translated into a list suitable for the API.

    - When updating a user, where possible provide the user ID to the module. This removes a lookup
      to the API to translate the name into the user ID.


options:
    state:
        description:
            - State of the user.
            - On C(present), the user will be created if it does not yet exist, or updated with the parameters you provide.
            - On C(absent), the user will be removed if it exists.
        default: 'present'
        type: str
        choices:
            - present
            - absent
    enabled:
      description: whether the user is enabled or not
      type: bool
      default: true

    name:
        type: str
        description:
            - Name of the user.
            - This parameter is required only when creating or updating the user.

    realm:
        type: str
        description:
            - They Keycloak realm under which this user resides.
        default: 'master'
    id:
        type: str
        description:
            - The unique identifier for this user.
            - This parameter is not required for updating or deleting a user but
              providing it will reduce the number of API calls required.
    first_name:
      type: str
      description:
          - First name of the user.
    last_name:
      type: str
      description:
          - Last name of the user.
    credentials:
      type: list
      description: user credentials configuration.
      elements: dict
      suboptions:
        type:
          description:
            - Type of credential e.g password.
          type: str
        value:
          description:
            - Value of the credential.
          type: str
        userLabel:
          description:
            - User-defined Label for the credential.
          type: str
        temporary:
          description:
            - Whether the password is temporary or not.
          type: bool
          default: false
    email:
      type: str
      description: Email for the user.

    email_verified:
      type: bool
      description: Set whether the email is verified or not.
      default: True

    required_actions:
      type: list
      description: A list of actions that will be applied on the user
      elements: str

    attributes:
        type: dict
        description:
            - A dict of key/value pairs to set as custom attributes for the user.
            - Values may be single values (e.g. a string) or a list of strings.

notes:
    - Presently, the I(realmRoles), I(clientRoles) and I(access) attributes returned by the Keycloak API
      are read-only for users. This limitation will be removed in a later version of this module.

author:
    - Dishant Pandya (@drpdishant)
    - Mahek Katariya (@MahekKatariya)

extends_documentation_fragment:
- community.general.keycloak
"""

EXAMPLES = """
- name: Create a Keycloak user, authentication with credentials
  community.general.keycloak_user:
    name: drstrange
    realm: midgard
    state: present
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
  delegate_to: localhost

- name: Create a Keycloak user, authentication with token
  community.general.keycloak_user:
    name: drstrange
    realm: MyCustomRealm
    state: present
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    token: TOKEN
  delegate_to: localhost

- name: Delete a keycloak user
  community.general.keycloak_user:
    id: '9d59aa76-2755-48c6-b1af-beb70a82c3cd'
    state: absent
    realm: MyCustomRealm
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
  delegate_to: localhost

- name: Delete a Keycloak user based on name
  community.general.keycloak_user:
    name: drstrange
    state: absent
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
  delegate_to: localhost

- name: Update the name of a Keycloak user
  community.general.keycloak_user:
    id: '9d59aa76-2755-48c6-b1af-beb70a82c3cd'
    username: bruce
    state: present
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
  delegate_to: localhost

- name: Create a keycloak user with some custom attributes
  community.general.keycloak_user:
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
    name: drstrange
    attributes:
        attrib1: value1
        attrib2: value2
        attrib3:
            - with
            - numerous
            - individual
            - list
            - items
  delegate_to: localhost
- name: Create/Update a user with password, full name and email (all params)
  community.general.keycloak_user:
    name: drstrange
    realm: midgard
    state: present
    first_name: Stephen
    last_name: Strane
    email: drstrange@marvel.com
    email_verified: True
    enabled: True
    auth_client_id: admin-cli
    auth_keycloak_url: https://auth.example.com/auth
    auth_realm: master
    auth_username: USERNAME
    auth_password: PASSWORD
    credentials:
    - type: password
      value:  holmes@sher.lock
      temporary: False
  delegate_to: localhost
"""

RETURN = """
msg:
    description: Message as to what action was taken.
    returned: always
    type: str

end_state:
    description: Representation of the user after module execution (sample is truncated).
    returned: on success
    type: dict
    contains:
        id:
          description: GUID that identifies the user.
          type: str
          returned: always
          sample: 23f38145-3195-462c-97e7-97041ccea73e
        firstName:
          description: First name of the user
          type: str
          sample: Stephen
        lastName:
          description: Last name of the user
          type: str
          sample: Strange
        username:
          description: Name of the user.
          type: str
          returned: always
          sample: drstrange
        attributes:
          description: Attributes applied to this user.
          type: dict
          returned: always
          sample:
            attr1: ["val1", "val2", "val3"]
        access:
          description: A dict describing the accesses you have to this user based on the credentials used.
          type: dict
          returned: always
          sample:
            manage: true
            manageMembership: true
            view: true

user:
  description:
    - Representation of the user after module execution.
    - Deprecated return value, it will be removed in community.general 6.0.0. Please use the return value I(end_state) instead.
  returned: always
  type: dict
  contains:
    id:
      description: GUID that identifies the user.
      type: str
      returned: always
      sample: 23f38145-3195-462c-97e7-97041ccea73e
    firstName:
      description: First name of the user
      type: str
      sample: Stephen
    lastName:
      description: Last name of the user
      type: str
      sample: Strange
    username:
      description: Name of the user.
      type: str
      returned: always
      sample: drstrange
    attributes:
      description: Attributes applied to this user.
      type: dict
      returned: always
      sample:
        attr1: ["val1", "val2", "val3"]
    access:
      description: A dict describing the accesses you have to this user based on the credentials used.
      type: dict
      returned: always
      sample:
        manage: true
        manageMembership: true
        view: true

"""

from ansible_collections.community.general.plugins.module_utils.identity.keycloak.keycloak import (
    KeycloakAPI,
    camel,
    keycloak_argument_spec,
    get_token,
    KeycloakError,
)
from ansible.module_utils.basic import AnsibleModule


def main():
    """
    Module execution

    :return:
    """
    argument_spec = keycloak_argument_spec()

    meta_args = dict(
        state=dict(default="present", choices=["present", "absent"]),
        realm=dict(default="master"),
        id=dict(type="str"),
        name=dict(type="str"),
        attributes=dict(type="dict"),
        email=dict(type="str"),
        enabled=dict(type="bool", default=True),
        first_name=dict(type="str"),
        last_name=dict(type="str"),
        required_actions=dict(type="list", elements="str"),
        credentials=dict(
            type="list",
            elements="dict",
            options=dict(
                type=dict(type="str"),
                value=dict(type="str", no_log=True),
                temporary=dict(type="bool", default=False),
                userLabel=dict(type="str"),
            ),
        ),
        email_verified=dict(type="bool", default=True),
    )

    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=(
            [
                ["id", "name"],
                ["token", "auth_realm", "auth_username", "auth_password"],
            ]
        ),
        required_together=([["auth_realm", "auth_username", "auth_password"]]),
    )

    result = dict(changed=False, msg="", diff={}, user="")

    # Obtain access token, initialize API
    try:
        connection_header = get_token(module.params)
    except KeycloakError as e:
        module.fail_json(msg=str(e))

    kc = KeycloakAPI(module, connection_header)

    realm = module.params.get("realm")
    state = module.params.get("state")
    uid = module.params.get("id")
    username = module.params.get("name")
    attributes = module.params.get("attributes")

    # attributes in Keycloak have their values returned as lists
    # via the API. attributes is a dict, so we'll transparently convert
    # the values to lists.
    if attributes is not None:
        for key, val in module.params["attributes"].items():
            module.params["attributes"][key] = (
                [val] if not isinstance(val, list) else val
            )

    # Filter and map the parameters names that apply to the user
    user_params = [
        x
        for x in module.params
        if x not in list(keycloak_argument_spec().keys()) + ["state", "realm"]
        and module.params.get(x) is not None
    ]

    # See if it already exists in Keycloak
    if uid is None:
        before_user = kc.get_user_by_name(username, realm=realm)
    else:
        before_user = kc.get_user_by_userid(uid, realm=realm)

    if before_user is None:
        before_user = {}

    # Build a proposed changeset from parameters given to this module
    changeset = {}

    for param in user_params:
        new_param_value = module.params.get(param)
        old_value = before_user[param] if param in before_user else None
        if param == "name":
            changeset[camel("username")] = new_param_value
        elif param == "user_groups":
            changeset[camel("groups")] = new_param_value
        elif new_param_value != old_value:
            changeset[camel(param)] = new_param_value

    # Prepare the desired values using the existing values (non-existence results in a dict that is save to use as a basis)
    desired_user = before_user.copy()
    desired_user.update(changeset)

    # Cater for when it doesn't exist (an empty dict)
    if not before_user:
        if state == "absent":
            # Do nothing and exit
            if module._diff:
                result["diff"] = dict(before="", after="")
            result["changed"] = False
            result["end_state"] = {}
            result["user"] = result["end_state"]
            result["msg"] = "user does not exist; doing nothing."
            module.exit_json(**result)

        # Process a creation

        if username is None:
            module.fail_json(msg="name must be specified when creating a new user")

        if module._diff:
            result["diff"] = dict(before="", after=desired_user)

        if module.check_mode:
            module.exit_json(**result)

        # create it
        kc.create_user(desired_user, realm=realm)
        after_user = kc.get_user_by_name(username, realm)
        result["end_state"] = after_user
        result["user"] = result["end_state"]

        result["msg"] = "user {name} has been created with ID {id}".format(
            name=after_user["username"], id=after_user["id"]
        )
        result["changed"] = True
        module.exit_json(**result)

    else:
        if state == "present":
            # Process an update

            # no changes
            if desired_user == before_user:
                result["changed"] = False
                result["end_state"] = desired_user
                result["user"] = result["end_state"]
                result["msg"] = "No changes required to user {name}.".format(
                    name=before_user["username"]
                )
                module.exit_json(**result)

            # doing an update
            result["changed"] = True

            if module._diff:
                result["diff"] = dict(before=before_user, after=desired_user)

            if module.check_mode:
                module.exit_json(**result)

            # do the update
            kc.update_user(desired_user, realm=realm)

            after_user = kc.get_user_by_userid(desired_user["id"], realm=realm)

            result["end_state"] = after_user
            result["user"] = result["end_state"]

            result["msg"] = "user {id} has been updated".format(id=after_user["id"])
            module.exit_json(**result)

        else:
            # Process a deletion (because state was not 'present')
            result["changed"] = True

            if module._diff:
                result["diff"] = dict(before=before_user, after="")

            if module.check_mode:
                module.exit_json(**result)

            # delete it
            uid = before_user["id"]
            kc.delete_user(userid=uid, realm=realm)

            result["end_state"] = {}
            result["user"] = result["end_state"]

            result["msg"] = "user {name} has been deleted".format(
                name=before_user["username"]
            )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
