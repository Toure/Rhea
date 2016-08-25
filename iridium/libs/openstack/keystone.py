__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

"""
Keystone module which will be responsible for authentication and base keystone commands.
"""

import os
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone_client
from iridium.core.logger import glob_logger
from iridium.config.config import Config
from iridium.config.config import CONF as IRIDIUM_CONF

CFG = Config()


class KeystoneBase(Config):
    def __init__(self):
        super().__init__()
        self.keystone_obj = self.create_keystone()

    def keystone_retrieve(self, version: str= 'v3', read_export: bool = False, **kwargs: dict) -> dict:
        """
        Simple function to retrieve configuration information from
        the global environment, if no kwargs is passed in, the necessary
        information is retrieved from the environment (ie, as when you source
        keystonerc_admin)
        :type read_export: bool
        :param version sets the version of ReST protocol to implement. (ie. "/v2.0", "/v3")
        kwargs:
           auth_url location to contact the keystone server.
           username usename to authenticate against keystone server.
           password password for username.
           project_name (version 3) or tenant_name (version 2) project credential for user.
           user_domain_name domain for username only valid for version 3 protocol.
           project_domain_name domain for specified project onnly valid for version 3.
        :rtype : dict
        :return: A dictionary that can be used with keystone client.
        """
        coll = self.dump_config(IRIDIUM_CONF)
        creds_coll = self.lookup(config_dict=coll, search_key=version)

        # TODO version control for keystone auth version, v2 will be gone in the future
        # make sure to add logic to encourage v3 usage.

        if not kwargs and read_export:
            glob_logger.info("Reading Environmental variables..")
            creds = {
                "username": os.environ.get("OS_USERNAME"),
                "password": os.environ.get("OS_PASSWORD"),
                "auth_url": os.environ.get("OS_AUTH_URL"),
                "tenant_name": os.environ.get("OS_TENANT_NAME")
                }

        # Here we use built-in config file.
        if not kwargs:
            creds = {k: v for k, v in creds_coll.items()
                     if v is not None}
        # Else we allow override of built-in dictionary.
        elif kwargs:
            creds = {k: v for k, v in kwargs.items()
                     if v is not None}

        glob_logger.debug("Using keystone creds: {}".format(creds))

        return creds

    def create_keystone(self, version: str= 'v3', **kwargs: dict) -> object:
        """Creates the keystone object

        :param version of protocol to communicate with Keystone over, the two options are
        v2 or v3 which are translated into /v2.0 and /v3 respectfully.

        kwargs:
           auth_url location to contact the keystone server.
           username usename to authenticate against keystone server.
           password password for username.
           project_name (version 3) or tenant_name (version 2) project credential for user.
           user_domain_name domain for username only valid for version 3 protocol.
           project_domain_name domain for specified project only valid for version 3.

        """
        # TODO additional checks for valid object creation.
        creds = self.keystone_retrieve(version, **kwargs)
        authentication_obj = v3.Password(**creds)
        keystone_session = session.Session(auth=authentication_obj)
        keystone = keystone_client.Client(session=keystone_session)

        return keystone

    def get_endpoint(self, name, end_type="publicURL"):
        return self.keystone_obj.service_catalog.url_for(service_type=name,
                                                              endpoint_type=end_type)

    def create_tenant(self, name, **kwargs):
        tenant = self.keystone_obj.tenants.create(name, **kwargs)
        return tenant

    def create_user(self, tenant_id, name, **kwargs):
        user = self.keystone_obj.users.create(name, tenant_id=tenant_id, **kwargs)
        return user

    def create_project(self, name, **kwargs):
        pass

