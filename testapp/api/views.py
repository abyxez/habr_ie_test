from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import (ComicDetailSerializer, ComicSerializer,
                             RatingSerializer)
from comics.models import Comic, Rating


class ComicViewSet(ReadOnlyModelViewSet):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    detail_serializer_class = ComicDetailSerializer

    @action(
        methods=[
            "get",
        ],
        detail=True,
        permission_classes=[],
    )
    def rating(self, request, pk=None):
        comic_obj = get_object_or_404(Comic, id=pk)
        data = self.detail_serializer_class(comic_obj).data
        return Response(data, status=HTTP_200_OK)


class RatingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
