"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""
from rest_framework import serializers

from pulpcore.plugin import serializers as platform

from . import models


# FIXME: SingleArtifactContentSerializer might not be the right choice for you.
# If your content type has no artifacts per content unit, use "NoArtifactContentSerializer".
# If your content type has many artifacts per content unit, use "MultipleArtifactContentSerializer"
# If you change this, make sure to do so on "fields" below, also.
# Make sure your choice here matches up with the create() method of your viewset.
class AnimalSerializer(platform.SingleArtifactContentSerializer):
    """
    A Serializer for Animal.

    Add serializers for the new fields defined in ShelterContent and
    add those fields to the Meta class keeping fields from the parent class as well.

    For example::

    field1 = serializers.TextField()
    field2 = serializers.IntegerField()
    field3 = serializers.CharField()

    class Meta:
        fields = platform.SingleArtifactContentSerializer.Meta.fields + (
            'field1', 'field2', 'field3'
        )
        model = models.ShelterContent
    """
    species = serializers.CharField(
        help_text="Species of an animal in a shelter"
    )
    breed = serializers.CharField(
        help_text="Breed of an animal in a shelter"
    )
    name = serializers.CharField(
        help_text="Name of an animal in a shelter"
    )
    shelter = serializers.CharField(
        help_text="Name of a shelter the animal is currently in or a name of the last shelter "
                  "in case it was adopted"
    )
    age = serializers.IntegerField(
        help_text="Age of an animal when it arrived to a shelter",
        required=False
    )
    sex = serializers.ChoiceField(
        help_text="Gender of an animal",
        choices=models.Animal.GENDER_CHOICES,
        default=models.Animal.UNKNOWN
    )
    weight = serializers.FloatField(
        help_text="Weight of an animal upon arrival to a shelter",
        required=False
    )
    bio = serializers.CharField(
        help_text="All information available about an animal",
        default='',
    )
    reserved = serializers.BooleanField(
        help_text="A flag to show if an animal is reserved for adoption",
        default=False,
    )
    picture = serializers.CharField(
        help_text="Relative path to an animal's picture in a repository"
    )

    class Meta:
        fields = platform.SingleArtifactContentSerializer.Meta.fields + ('species', 'breed',
                                                                         'name', 'age', 'sex',
                                                                         'weight', 'bio',
                                                                         'shelter', 'reserved',
                                                                         'picture')
        model = models.Animal


class ShelterRemoteSerializer(platform.RemoteSerializer):
    """
    A Serializer for ShelterRemote.

    Add any new fields if defined on ShelterRemote.
    Similar to the example above, in ShelterContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.RemoteSerializer.Meta.validators + [myValidator1, myValidator2]
    """

    class Meta:
        fields = platform.RemoteSerializer.Meta.fields
        model = models.ShelterRemote


class ShelterPublisherSerializer(platform.PublisherSerializer):
    """
    A Serializer for ShelterPublisher.

    Add any new fields if defined on ShelterPublisher.
    Similar to the example above, in ShelterContentSerializer.
    Additional validators can be added to the parent validators list

    For example::

    class Meta:
        validators = platform.PublisherSerializer.Meta.validators + [myValidator1, myValidator2]
    """

    manifest_file = serializers.CharField(
        help_text='Name of the shelter manifest, the full path will be url/manifest',
        required=False,
        default='shelter_manifest.json'
    )

    class Meta:
        fields = platform.PublisherSerializer.Meta.fields + ('manifest_file',)
        model = models.ShelterPublisher
