import json
import logging
import os

from gettext import gettext as _

from django.core.files import File

from pulpcore.plugin.models import (
    RepositoryVersion,
    Publication,
    PublishedArtifact,
    PublishedMetadata,
    RemoteArtifact
)
from pulpcore.plugin.tasking import WorkingDirectory

from pulp_shelter.app.models import ShelterPublisher, Animal


log = logging.getLogger(__name__)


def publish(publisher_pk, repository_version_pk):
    """
    Use provided publisher to create a Publication based on a RepositoryVersion.

    Args:
        publisher_pk (str): Use the publish settings provided by this publisher.
        repository_version_pk (str): Create a publication from this repository version.
    """
    publisher = ShelterPublisher.objects.get(pk=publisher_pk)
    repository_version = RepositoryVersion.objects.get(pk=repository_version_pk)

    log.info(_('Publishing: repository={repo}, version={ver}, publisher={pub}').format(
        repo=repository_version.repository.name,
        ver=repository_version.number,
        pub=publisher.name
    ))
    with WorkingDirectory():
        with Publication.create(repository_version, publisher) as publication:

            shelter_data = populate(publication)
            with open(publisher.manifest_file, 'w') as fp:
                fp.write(json.dumps(shelter_data))
            metadata = PublishedMetadata(
                relative_path=os.path.basename(publisher.manifest_file),
                publication=publication,
                file=File(open(publisher.manifest_file, 'rb')))
            metadata.save()

    log.info(_('Publication: {publication} created').format(publication=publication.pk))


def populate(publication):
    """
    Populate a publication.
    Create published artifacts and return data for shelter_manifest
    Args:
        publication (pulpcore.plugin.models.Publication): A Publication to populate.
    Returns:
        Entry: data for shelter_manifest
    """
    shelter_data = []
    for content in Animal.objects.filter(pk__in=publication.repository_version.content):
        for content_artifact in content.contentartifact_set.all():
            published_artifact = PublishedArtifact(
                relative_path=content_artifact.relative_path,
                publication=publication,
                content_artifact=content_artifact)
            published_artifact.save()
            pet = {
		      'name': content.name,
		      'species': content.species,
		      'age': content.age,
		      'weight': content.weight,
                      'bio': content.bio,
                      'shelter': content.shelter,
                      'sex': content.sex,
                      'reserved': content.reserved,
                      'breed': content.breed,
                      'picture': content.picture
		}
        shelter_data.append(pet)
    return shelter_data
