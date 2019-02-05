"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from pulpcore.plugin import viewsets as core
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositoryPublishURLSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.models import ContentArtifact

from . import models, serializers, tasks


class AnimalFilter(core.ContentFilter):
    """
    FilterSet for Animal.
    """

    class Meta:
        model = models.Animal
        fields = [
            'species', 'breed', 'shelter'
        ]


class AnimalViewSet(core.ContentViewSet):
    """
    A ViewSet for Animal.

    Define endpoint name which will appear in the API endpoint for this content type.
    For example::
        http://pulp.example.com/pulp/api/v3/content/shelter/units/

    Also specify queryset and serializer for ShelterContent.
    """

    endpoint_name = 'animal'
    queryset = models.Animal.objects.all()
    serializer_class = serializers.AnimalSerializer
    filterset_class = AnimalFilter

    @transaction.atomic
    def create(self, request):
        """
        Perform bookkeeping when saving Content.

        "Artifacts" need to be popped off and saved indpendently, as they are not actually part
        of the Content model.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _artifact = serializer.validated_data.pop('_artifact')
        content = serializer.save()

        if content.pk:
            ContentArtifact.objects.create(
                artifact=artifact,
                content=content,
                relative_path=content.relative_path
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ShelterRemoteFilter(core.RemoteFilter):
    """
    A FilterSet for ShelterRemote.
    """

    class Meta:
        model = models.ShelterRemote
        fields = [
            # ...
        ]


class ShelterRemoteViewSet(core.RemoteViewSet):
    """
    A ViewSet for ShelterRemote.

    Similar to the ShelterContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = 'shelter'
    queryset = models.ShelterRemote.objects.all()
    serializer_class = serializers.ShelterRemoteSerializer

    # This decorator is necessary since a sync operation is asyncrounous and returns
    # the id and href of the sync task.
    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to sync content",
        responses={202: AsyncOperationResponseSerializer}
    )
    @detail_route(methods=('post',), serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Synchronizes a repository. The ``repository`` field has to be provided.
        """
        remote = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={'request': request})

        # Validate synchronously to return 400 errors.
        serializer.is_valid(raise_exception=True)
        repository = serializer.validated_data.get('repository')
        mirror = serializer.validated_data.get('mirror', True)
        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={
                'remote_pk': remote.pk,
                'repository_pk': repository.pk,
                'mirror': mirror
            }
        )
        return core.OperationPostponedResponse(result, request)


class ShelterPublisherViewSet(core.PublisherViewSet):
    """
    A ViewSet for ShelterPublisher.

    Similar to the ShelterContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = 'shelter'
    queryset = models.ShelterPublisher.objects.all()
    serializer_class = serializers.ShelterPublisherSerializer

    # This decorator is necessary since a publish operation is asyncrounous and returns
    # the id and href of the publish task.
    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer}
    )
    @detail_route(methods=('post',), serializer_class=RepositoryPublishURLSerializer)
    def publish(self, request, pk):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        publisher = self.get_object()
        serializer = RepositoryPublishURLSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get('repository_version')

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository, publisher],
            kwargs={
                'publisher_pk': str(publisher.pk),
                'repository_version_pk': str(repository_version.pk)
            }
        )
        return core.OperationPostponedResponse(result, request)
