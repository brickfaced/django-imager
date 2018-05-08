from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album, User
from imager_profile.models import ImagerProfile
from django.urls import reverse


def photos_view(request):
    
    photo = Photo.objects.all().filter(published='PUBLIC')
    photos = {
        'photos': photo
    }
    if photos:
        return render(request, 'imager_images/photos.html', photos)


def albums_view(request):
    album = Album.objects.all().filter(published='PUBLIC')
    albums = {
        'albums': album
    }
    return render(request, 'imager_images/albums.html', albums)


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
    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)
        context = {
            'photo': {'thumb': photo, 'link': reverse('photos')}
        }
        return render(request, 'imager_images/photo.html', context)
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': [{'cover': album.cover, 'link': reverse('album',
                    args=[album.id])} for album in albums],
        'photos': [{'thumb': photo, 'link': reverse('photos', args=[photo.id])} for photo in photos]
    }
    return render(request, 'imager_images/photo.html', context)


def _album_with_cover(photos, cover):
    if cover is not None:
        return set(photos) | {cover}
    return photos


def album_view(request, album_id=None):
    """Album View."""
    username = request.user.get_username()
    owner = True
    if username == '':
        return redirect('home')

    profile = get_object_or_404(User, username=username)
    albums = Album.objects.filter(published='PUBLIC')
    photos = Photo.objects.filter(published='PUBLIC')

    context = {
        'profile': profile,
        'albums': albums,
        'photos': photos,
    }
    if album_id:
        album = get_object_or_404(Album, id=album_id)
        context["photos"] = _album_with_cover(Photo.objects.filter(album__id=album.id).filter(published='PUBLIC'), album.cover)
        context["album"] = album
        return render(request, 'imager_images/album.html', context)
    return render(request, 'imager_images/album.html', context)
