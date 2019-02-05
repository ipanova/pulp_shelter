from gettext import gettext as _
import json
import logging
import os

from urllib.parse import urlparse, urlunparse

from pulpcore.plugin.models import Artifact, ProgressBar, Remote, Repository
from pulpcore.plugin.stages import (
    DeclarativeArtifact,
    DeclarativeContent,
    DeclarativeVersion,
    Stage
)

from pulp_shelter.app.models import Animal, ShelterRemote


log = logging.getLogger(__name__)


def synchronize(remote_pk, repository_pk, mirror):
    """
    Sync content from the remote repository.

    Create a new version of the repository that is synchronized with the remote.

    Args:
        remote_pk (str): The remote PK.
        repository_pk (str): The repository PK.
        mirror (bool): True for mirror mode, False for additive.

    Raises:
        ValueError: If the remote does not specify a URL to sync

    """
    remote = ShelterRemote.objects.get(pk=remote_pk)
    repository = Repository.objects.get(pk=repository_pk)

    if not remote.url:
        raise ValueError(_('A remote must have a url specified to synchronize.'))

    # Interpret policy to download Artifacts or not
    download_artifacts = (remote.policy == Remote.IMMEDIATE)
    first_stage = ShelterFirstStage(remote)
    DeclarativeVersion(
        first_stage, repository,
        mirror=mirror, download_artifacts=download_artifacts
    ).create()


class ShelterFirstStage(Stage):
    """
    The first stage of a pulp_shelter sync pipeline.
    """

    def __init__(self, remote):
        """
        The first stage of a pulp_shelter sync pipeline.

        Args:
            remote (FileRemote): The remote data to be used when syncing

        """
        super().__init__()
        self.remote = remote

    async def run(self):
        """
        Build and emit `DeclarativeContent` from the Manifest data.

        Args:
            in_q (asyncio.Queue): Unused because the first stage doesn't read from an input queue.
            out_q (asyncio.Queue): The out_q to send `DeclarativeContent` objects to

        """
        with ProgressBar(message='Downloading Metadata') as pb:
            parsed_url = urlparse(self.remote.url)
            root_dir = os.path.dirname(parsed_url.path)
            downloader = self.remote.get_downloader(url=self.remote.url)
            result = await downloader.run()
            pb.increment()

        with ProgressBar(message='Parsing Metadata') as pb:
            for entry in self.read_my_metadata_file_somehow(result.path):
                path = os.path.join(root_dir, entry['picture'])
                url = urlunparse(parsed_url._replace(path=path))
                unit = Animal(**entry)  # make the content unit in memory-only
                artifact = Artifact()  # make Artifact in memory-only
                da =  DeclarativeArtifact(artifact, url, entry['picture'], self.remote)
                dc = DeclarativeContent(content=unit, d_artifacts=[da])
                pb.increment()
                await self.put(dc)

    def read_my_metadata_file_somehow(self, path):
        """
        Parse the metadata for shelter Content type.

        Args:
            path: Path to the metadata file
        """
        with open(path) as f:
            return json.loads(f.read())