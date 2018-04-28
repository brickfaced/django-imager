from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album
from imager_profile.models import ImagerProfile


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


def library_view(request, username=None):
    owner = False

    if not username:
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')

    profile = get_object_or_404(ImagerProfile, user__username=username)
    album = Album.objects.filter(user__username=username)
    photos = Photo.objects.filter(album__user__username=username)

    if not owner:
        photos = Photo.objects.filter(published='PUBLIC')
        album = Album.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'album': album,
        'photos': photos
    }

    return render(request, 'imager_images/library.html', context)


def photo_view(request, photo_id=None):
    owner = False
    import pdb; pdb.set_trace()
    if not username:
        username = request.user.get_username()
        owner = True
        if username == '':
            return redirect('home')

    profile = get_object_or_404(ImagerProfile, user__username=username)
    album = Album.objects.filter(user__username=username)
    photos = Photo.objects.filter(album__user__username=username)

    if not owner:
        photos = Photo.objects.filter(published='PUBLIC')
        album = Album.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'album': album,
        'photos': photos
    }

    return render(request, 'imager_images/library.html', context)



