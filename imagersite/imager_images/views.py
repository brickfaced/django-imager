from django.shortcuts import render, redirect
from .models import Photo, Album


def photos_view(request):
    photo = Photo.objects.all().filter(published='PUBLIC')
    photos = {
        'photos': photo
    }
    if photos:
        return render(request, 'imager_images/images.html', photos)


def albums_view(request):
    album = Album.objects.all().filter(published='PUBLIC')
    albums = {
        'albums': album
    }
    return render(request, 'imager_images/album.html', albums)



