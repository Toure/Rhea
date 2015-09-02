__author__ = "Toure Dunnon"
__license__ = "Apache License 2.0"
__version__ = "0.1"
__email__ = "toure@redhat.com"
__status__ = "Alpha"

from cinderclient import client
from libs.openstack import keystone


class CinderBase(object):
    """
    CinderBase class is used for standard commands which can be issued to cinder.
    example: create or delete a volume -- cinder create --name=test_volume 10
    """
    def __init__(self, version, **kwargs):
        """

        :return: cinder auth object.
        """
        cinder_auth = keystone.get_keystone_init(**kwargs)
        self.cinder_cl = client.Client(version, cinder_auth)

    def list_zone(self):
        """

        :param cinder_cl:
        :return:
        """
        return self.cinder_cl.availability_zones.list()

    def backup_create(self, volume_id, container=None, name=None, description=None,
                      incremental=False, force=False):
        """
        Create a backup of cinder volume.
        :param cinder_cl:
        :param volume_id: The ID of the volume to backup.
        :param container: The name of the backup service container.
        :param name: The name of the backup.
        :param description: The description of the backup.
        :param incremental: Incremental backup.
        :param force: If True, allows an in-use volume to be backed up.
        :rtype: :class:`VolumeBackup`
        """
        return self.cinder_cl.create(volume_id, container=container, name=name,
                                     description=description, incremental=incremental, force=force)

    def backup_delete(self, volume):
        """
        Deletes specified volume.
        :param cinder_cl:
        :param volume:
        :return:
        """
        self.cinder_cl.delete(volume)

    def backup_list(self, detailed=True, search_opts=None):
        """

        :param cinder_cl:
        :param detailed:
        :param search_opts:
        :return: list of volumes.
        """
        return self.cinder_cl.list(detailed=detailed, search_opts=search_opts)

    def backup_export(self, backup_id):
        """
        Export volume backup metadata record.
        :param cinder_cl:
        :param backup_id:
        :return:
        """
        return self.cinder_cl.export_record(backup_id)

    def backup_import(self, backup_service, backup_url):
        """

        :param cinder_cl:
        :param backup_service:
        :param backup_url:
        :return:
        """
        self.cinder_cl.import_record(backup_service, backup_url)

    def vol_create(self, size, consistencygroup_id=None, snapshot_id=None, source_volid=None,
                   name=None, description=None, volume_type=None, user_id=None, project_id=None,
                   availability_zone=None, metadata=None, imageRef=None, scheduler_hints=None,
                   source_replica=None, multiattach=False):
        """
        Create a volume.

        :param size: Size of volume in GB
        :param consistencygroup_id: ID of the consistencygroup
        :param snapshot_id: ID of the snapshot
        :param name: Name of the volume
        :param description: Description of the volume
        :param volume_type: Type of volume
        :param user_id: User id derived from context
        :param project_id: Project id derived from context
        :param availability_zone: Availability Zone to use
        :param metadata: Optional metadata to set on volume creation
        :param imageRef: reference to an image stored in glance
        :param source_volid: ID of source volume to clone from
        :param source_replica: ID of source volume to clone replica
        :param scheduler_hints: (optional extension) arbitrary key-value pairs
                            specified by the client to help boot an instance
        :param multiattach: Allow the volume to be attached to more than
                            one instance
        :rtype: :class:`Volume`
        """
        self.cinder_cl.create(size, consistencygroup_id=consistencygroup_id, snapshot_id=snapshot_id,
                       source_volid=source_volid, name=name, description=description, volume_type=volume_type,
                       user_id=user_id, project_id=project_id, availability_zone=availability_zone, metadata=metadata,
                       imageRef=imageRef, scheduler_hints=scheduler_hints, source_replica=source_replica,
                       multiattach=multiattach)


    def vol_delete(self, volume_id):
        """

        :return:
        """
        self.cinder_cl.delete(volume_id)

    def vol_extend(self, volume, size):
        """

        :param volume:
        :param size:
        :return:
        """
        self.cinder_cl.extend(volume, size)


    def vol_list(self):
        """

        :return:
        """
        self.cinder_cl.list()


    def vol_rename(self):
        pass

    def snapshot_create(self):
        pass

    def snapeshot_delete(self):
        pass

    def snapshot_list(self):
        pass
