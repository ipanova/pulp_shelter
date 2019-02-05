"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""

from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, ContentArtifact, Remote, Publisher

logger = getLogger(__name__)


class Animal(Content):
    """
    The "animal" content type.

    Define fields you need for your new content type and
    specify uniqueness constraint to identify unit of this type.

    For example::

        field1 = models.TextField()
        field2 = models.IntegerField()
        field3 = models.CharField()

        class Meta:
            unique_together = (field1, field2)
    """
    TYPE = 'animal'

    MALE = 'male'
    FEMALE = 'female'
    HERMAPHRODITE = 'hermaphrodite'
    UNKNOWN = 'unknown'

    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
        (HERMAPHRODITE, HERMAPHRODITE),
        (UNKNOWN, UNKNOWN)
    )

    species = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    name = 	models.CharField(max_length=255)
    age = models.IntegerField()
    sex	= models.ChoiceField(choices = GENDER_CHOICES, default=UNKNOWN)
    weight = models.FloatField()
    bio = models.TextField()
    shelter = models.CharField(max_length=255)
    reserved = models.BooleanField(default=False)
    picture	= models.CharField(max_length=255, unique=True)

    class Meta:
        unique_together = (species, breed, name, shelter)


class ShelterPublisher(Publisher):
    """
    A Publisher for Animal.

    Define any additional fields for your new publisher if needed.
    """

    TYPE = 'shelter'


class ShelterRemote(Remote):
    """
    A Remote for Animal.

    Define any additional fields for your new importer if needed.
    """

    TYPE = 'shelter'
