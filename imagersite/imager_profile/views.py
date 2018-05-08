from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Photo, Album
from .models import ImagerProfile


def profile_view(request, username=None):
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

    return render(request, 'imager_profile/user.html', context)