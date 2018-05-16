from rest_framework import generics
from .serializers import PhotoSerializer
from imager_images.models import Photo


class PhotoListApi(generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.all()
