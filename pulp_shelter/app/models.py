"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""

from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, ContentArtifact, Remote, Publisher

logger = getLogger(__name__)


class ShelterContent(Content):
    """
    The "shelter" content type.

    Define fields you need for your new content type and
    specify uniqueness constraint to identify unit of this type.

    For example::

        field1 = models.TextField()
        field2 = models.IntegerField()
        field3 = models.CharField()

        class Meta:
            unique_together = (field1, field2)
    """

    TYPE = 'shelter'


class ShelterPublisher(Publisher):
    """
    A Publisher for ShelterContent.

    Define any additional fields for your new publisher if needed.
    """

    TYPE = 'shelter'


class ShelterRemote(Remote):
    """
    A Remote for ShelterContent.

    Define any additional fields for your new importer if needed.
    """

    TYPE = 'shelter'
